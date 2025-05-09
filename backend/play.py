import json
import asyncio
from dotenv import load_dotenv
from fast_bitrix24 import Bitrix
import os

load_dotenv()
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

ENTITY_TYPE_ID = '135'
bx = Bitrix(WEBHOOK_URL)

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
        '5. На стоянке': ['DT135_12:UC_LHM1NV', 'DT135_12:UC_4WLJGM']
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


async def get_car_info_by_vin(vin: str, lastname: str) -> dict:
    result = {
        'car_data': None,
        'person_data': None,
        'stage_info': None,
        'tracking_info': None,
        'stage_history': None  # Добавляем поле для истории
    }

    # Добавляем ufCrm8StageHistory в select
    smart_items = await bx.get_all(
        'crm.item.list',
        {
            'entityTypeId': ENTITY_TYPE_ID,
            'filter': {'ufCrm8Vin': vin},
            'select': ['*', 'ufCrm8FotoAvto', 'ufCrm8MarkaTc',
                       'ufCrm8DataVipuska', 'stageId', 'ufCrm8StageHistory']
        }
    )

    if not smart_items:
        return result

    # Добавляем историю стадий в результат
    stage_history = smart_items[0].get('ufCrm8StageHistory')
    if stage_history:
        result['stage_history'] = stage_history

    result['car_data'] = {
        "vin": smart_items[0].get('ufCrm8Vin', 'Нет данных'),
        "photo": smart_items[0].get('ufCrm8FotoAvto', 'Нет данных'),
        "car_make": smart_items[0].get('ufCrm8MarkaTc', 'Нет данных'),
        "model": smart_items[0].get('ufCrm8ModelTc', 'Нет данных'),
        "car_release_date": smart_items[0].get('ufCrm8DataVipuska', 'Нет данных'),
    }

    stage_id = smart_items[0].get('stageId')
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

    # Данные контакта
    client_id = smart_items[0].get('contactId')
    contacts = await bx.get_all(
        'crm.contact.list',
        {
            'filter': {'ID': client_id, 'ACTIVE': 'Y'},
            'select': ['*', 'ID', 'NAME', 'LAST_NAME', 'SECOND_NAME', 'PHONE', 'EMAIL']
        }
    )
    for contact in contacts:
        if contact["LAST_NAME"].lower() == lastname.lower():
            result["person_data"] = {
                "LAST_NAME": contact.get("LAST_NAME", "Нет данных").capitalize(),
                "NAME": contact.get("NAME", "Нет данных").capitalize(),
            }
        break
    return result
