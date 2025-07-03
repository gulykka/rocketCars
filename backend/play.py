import json
import asyncio
from dotenv import load_dotenv
from fast_bitrix24 import Bitrix
import os

load_dotenv()
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

ENTITY_TYPE_ID = '135'

bx = Bitrix(WEBHOOK_URL)


def load_describtion_from_json(file_path='describtion.json'):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def load_stages_from_json(file_path='resp.json'):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def get_tracking_info(current_stage_id, all_stages):
    # Загружаем описания этапов
    descriptions = load_describtion_from_json()
    # Создаем словарь для быстрого доступа к описаниям по имени группы
    description_map = {f"{item['id']}. {item['name']}": item['description']
                       for item in descriptions}
    stage_groups = {
        '1. На оплате': ['DT135_12:NEW'],
        '2. На стоянке в Китае': ['DT135_12:PREPARATION'],
        '3. Доставка в РФ': ['DT135_12:UC_G2QLMW'],
        '4. На СВХ': ['DT135_12:CLIENT', 'DT135_12:UC_QFS3CA',
                      'DT135_12:UC_UST2QE', 'DT135_12:UC_37UMS1'],
        '5. На стоянке': ['DT135_12:UC_LHM1NV', 'DT135_12:UC_4WLJGM', 'DT135_12:SUCCESS']
    }

    current_stage = next((s for s in all_stages if s['STATUS_ID'] == current_stage_id), None)
    if not current_stage:
        return {}

    current_sort = int(current_stage['SORT'])

    tracking_data = {}

    for group_name, status_ids in stage_groups.items():
        group_stages = [s for s in all_stages if s['STATUS_ID'] in status_ids]
        if not group_stages:
            continue

        max_sort_in_group = max(int(s['SORT']) for s in group_stages)
        is_completed = max_sort_in_group < current_sort
        is_current = any(s['STATUS_ID'] == current_stage_id for s in group_stages)

        # Добавляем описание из description_map
        description = description_map.get(group_name, "")

        tracking_data[group_name] = {
            'completed': is_completed,
            'current': is_current,
            'description': description,
            'stages': []
        }
        for stage in sorted(group_stages, key=lambda x: int(x['SORT'])):
            stage_sort = int(stage['SORT'])
            tracking_data[group_name]['stages'].append({
                'name': stage['NAME'],
                'status_id': stage['STATUS_ID'],
                'color': stage['COLOR'],
                'completed': stage_sort < current_sort,
                'current': stage['STATUS_ID'] == current_stage_id
            })

    return {k: v for k, v in tracking_data.items()
            if v['completed'] or v['current']}


def generate_vin_variants(raw_vin):
    # 1. Очистка от пробелов
    vin_clean = raw_vin.replace(' ', '')

    variants = [
        vin_clean,  # "XXXXXXXXXXXXXXXXXX"
        vin_clean + ' ',  # "XXXXXXXXXXXXXXXXXX "
        ' ' + vin_clean,  # " XXXXXXXXXXXXXXXXXX"
    ]

    # 4. Пробел перед последними 4 символами
    if len(vin_clean) >= 4:
        spaced = vin_clean[:-4] + ' ' + vin_clean[-4:]
        variants.append(spaced)  # "XXXXXXXXXXXXXXXX XX"

    return variants


async def get_car_info_by_vin(vin: str, lastname: str) -> dict:
    result = {
        'car_data': None,
        'person_data': None,
        'stage_info': None,
        'tracking_info': None,
        'stage_history': None
    }

    # 1. Чистим VIN
    vin_variants: list = generate_vin_variants(vin)
    # 2. Запрашиваем только нужный элемент по VIN
    for variant in vin_variants:
        smart_items = await bx.get_all(
            'crm.item.list',
            {
                'entityTypeId': ENTITY_TYPE_ID,
                'filter': {'ufCrm8Vin': variant},
                'select': ['*', 'ufCrm8...']
            }
        )
        if smart_items:
            break

    if not smart_items:
        return result  # Ничего не найдено

    smart_item = smart_items[0]  # Берём первый (единственный) найденный элемент

    # 3. Сохраняем данные об автомобиле
    result['car_data'] = {
        "vin": smart_item.get('ufCrm8Vin', 'Нет данных'),
        "photo": smart_item.get('ufCrm8FotoAvto', 'Нет данных'),
        "car_make": smart_item.get('ufCrm8MarkaTc', 'Нет данных'),
        "model": smart_item.get('ufCrm8ModelTc', 'Нет данных'),
        "car_release_date": smart_item.get('ufCrm8DataVipuska', 'Нет данных'),
    }

    # 4. Добавляем историю стадий
    stage_history = smart_item.get('ufCrm8StageHistory')
    if stage_history:
        result['stage_history'] = stage_history

    # 5. Получаем текущую стадию
    stage_id = smart_item.get('stageId')
    print(stage_id)
    if stage_id:
        all_stages = load_stages_from_json()
        current_stage = next((s for s in all_stages if s['STATUS_ID'] == stage_id), None)
        if current_stage:
            result['stage_info'] = {
                'id': stage_id,
                'name': current_stage['NAME'],
                'color': current_stage['COLOR']
            }
            result['tracking_info'] = get_tracking_info(stage_id, all_stages)

    # 6. Получаем ID сделки
    deal_id = smart_item.get('parentId2')
    print(deal_id)
    if not deal_id:
        return result

    # 6. Получаем сделку
    deal_result = await bx.call('crm.deal.get', {'id': deal_id})
    deal_data = next(iter(deal_result.values()))  # например, 'order0000000000'

    # Теперь получаем UF_CRM_1716620414 правильно
    client_id = deal_data.get('UF_CRM_1716620414')

    print("UF_CRM_1716620414:", client_id)

    if not client_id:
        print("Поле UF_CRM_1716620414 пустое")
        return result

    # 7. Удаляем префикс C_, если есть
    if isinstance(client_id, str) and client_id.startswith('C_'):
        client_id = client_id[2:]

    # Проверка, что client_id — это число
    if not (isinstance(client_id, str) and client_id.isdigit()):
        print(f"client_id не является числом: {client_id}")
        return result

    # 8. Получаем контакт
    try:
        contact_result = await bx.call('crm.contact.get', {'id': int(client_id)})
        print("CONTACT_RESULT  ", contact_result)
    except Exception as e:
        print("Ошибка при получении контакта:", str(e))
        return result

    if not contact_result:
        print("Контакт не найден или доступ запрещён")
        return result

    # 9. Проверяем совпадение фамилии
    contact_data = next(iter(contact_result.values())) if contact_result else {}

    # Теперь получаем фамилию и имя
    last_name = contact_data.get('LAST_NAME', '').strip().lower()
    first_name = contact_data.get('NAME', '').strip().capitalize()

    if last_name == lastname.lower():
        result["person_data"] = {
            "LAST_NAME": last_name.capitalize(),
            "NAME": first_name
        }

    return result
#
# data = asyncio.run(get_car_info_by_vin("LBV31DU00NS300349", "Фанкин"))
# print(data)
