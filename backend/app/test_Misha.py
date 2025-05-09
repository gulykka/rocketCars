from fast_bitrix24 import Bitrix
import json

# Настройки подключения
WEBHOOK_URL = ""  # Замените на ваш вебхук
FIELD_CODE = 'ufCrm8Vin'  # Код поля с ВИН авто
FIELD_VALUE = '1234567890'  # Нужный VIN
ENTITY_TYPE_ID = '135'  # ID смарт-процесса

# Инициализация клиента Bitrix24
bx = Bitrix(WEBHOOK_URL)

# Словарь для хранения всех данных
all_data = {
    'smart_process_items': None,
    'deal_data': None,
    'contact_data': None
}

try:
    # 1. Получаем элементы смарт-процесса по VIN
    print("Получаем информацию по авто...")
    smart_process_items = bx.get_all(
        'crm.item.list',
        {
            'entityTypeId': ENTITY_TYPE_ID,
            'filter': {FIELD_CODE: FIELD_VALUE},
            'select': ['*']
        }
    )
    all_data['smart_process_items'] = smart_process_items

    print("Информация по авто:")
    print(json.dumps(smart_process_items, indent=2, ensure_ascii=False))

    if smart_process_items:
        # 2. Получаем данные сделки
        deal_id = smart_process_items[0]['parentId2']
        print(f"\nПолучаем информацию по сделке ID: {deal_id}...")
        deal_data = bx.get_by_ID(
            'crm.deal.get',
            [deal_id]
        )[0]
        all_data['deal_data'] = deal_data

        print("Информация по сделке:")
        print(json.dumps(deal_data, indent=2, ensure_ascii=False))

        # 3. Получаем данные контакта
        client_id = deal_data.get('UF_CRM_1716620414', '')
        if client_id.startswith('C_'):
            client_id = client_id[2:]

        if client_id:
            print(f"\nПолучаем информацию по контакту ID: {client_id}...")
            contact_data = bx.get_by_ID(
                'crm.contact.get',
                [client_id]
            )[0]
            all_data['contact_data'] = contact_data

            print("Информация по контакту:")
            print(json.dumps(contact_data, indent=2, ensure_ascii=False))

    # Сохраняем все данные в JSON файл
    with open('bitrix_data.json', 'w', encoding='utf-8') as f:
        json.dump(all_data, f, indent=2, ensure_ascii=False)
    print("\nВсе данные сохранены в файл bitrix_data.json")

except Exception as e:
    print(f"Произошла ошибка: {str(e)}")
    # В случае ошибки также сохраняем то, что успели собрать
    with open('bitrix_data_partial.json', 'w', encoding='utf-8') as f:
        json.dump(all_data, f, indent=2, ensure_ascii=False)
    print("Частичные данные сохранены в bitrix_data_partial.json")


def get_data(lastname: str):
    try:
        # 1. Получаем элементы смарт-процесса по VIN
        print("Получаем информацию по авто...")
        smart_process_items = bx.get_all(
            'crm.item.list',
            {
                'entityTypeId': ENTITY_TYPE_ID,
                'filter': {FIELD_CODE: FIELD_VALUE},
                'select': ['*']
            }
        )
        all_data['smart_process_items'] = smart_process_items

        contact_data = bx.get_all(
            'crm.contact.list',
            {
                'filter': {'LAST_NAME': lastname}
            }
        )
    except Exception as e:
        return "Error"
