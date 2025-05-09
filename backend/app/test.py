from fast_bitrix24 import Bitrix
import json

# Настройки подключения
WEBHOOK_URL = ""
ENTITY_TYPE_ID = '135'  # ID смарт-процесса

# Инициализация клиента Bitrix24
bx = Bitrix(WEBHOOK_URL)


def get_car_info_by_vin(vin: str) -> dict:
    """Получение информации об автомобиле по VIN"""
    result = {
        'smart_process_items': None,
        'deal_data': None,
        'contact_data': None
    }

    try:
        # 1. Получаем элементы смарт-процесса по VIN
        print(f"Поиск автомобиля с VIN: {vin}...")
        smart_items = bx.get_all(
            'crm.item.list',
            {
                'entityTypeId': ENTITY_TYPE_ID,
                'filter': {'ufCrm8Vin': vin},
                'select': ['*', 'ufCrm8FotoAvto', 'ufCrm8MarkaTc', 'ufCrm8DataVipuska', ]
            }
        )
        result['smart_process_items'] = smart_items
        print(result)

        return result

    except Exception as e:
        print(f"Ошибка при поиске по VIN: {str(e)}")
        return result


def get_cars_by_client_lastname(lastname: str) -> list:
    """Поиск автомобилей по фамилии клиента"""
    result = []

    try:
        # 1. Ищем контакт по фамилии
        print(f"Поиск контактов с фамилией: {lastname}...")
        contacts = bx.get_all(
            'crm.contact.list',
            {
                'filter': {'LAST_NAME': lastname, 'ACTIVE': 'Y'},
                'select': ['*', 'ID', 'NAME', 'LAST_NAME', 'SECOND_NAME', 'PHONE', 'EMAIL']
            }
        )
        print(contacts)
        for contact in contacts:
            contact_id = contact['ID']
            client_name = f"{contact.get('LAST_NAME', '')} {contact.get('NAME', '')} {contact.get('SECOND_NAME', '')}".strip()

            # 2. Ищем сделки контакта
            deals = bx.get_all(
                'crm.deal.list',
                {
                    'filter': {'UF_CRM_1716620414': f"C_{contact_id}"},
                    'select': ['ID', 'STAGE_ID', 'STAGE_NAME', 'TITLE']
                }
            )
            print("DEALS", deals)
            for deal in deals:
                # 3. Ищем элементы смарт-процесса для сделки
                smart_items = bx.get_all(
                    'crm.item.list',
                    {
                        'entityTypeId': ENTITY_TYPE_ID,
                        'filter': {'parentId2': deal['ID']},
                        'select': ['id', 'stageId', 'ufCrm8Vin', 'ufCrm8FotoAvto', 'ufCrm8MarkaAvto',
                                   'ufCrm8GodVypuska']
                    }
                )

                for item in smart_items:
                    # Обработка фото автомобиля
                    photos = []
                    photo_data = item.get('ufCrm8FotoAvto')
                    if isinstance(photo_data, list):
                        photos = [p.get('downloadUrl') for p in photo_data if p.get('downloadUrl')]
                    elif isinstance(photo_data, dict) and photo_data.get('downloadUrl'):
                        photos = [photo_data.get('downloadUrl')]

                    # Формируем результат
                    car_info = {
                        'client_info': {
                            'id': contact_id,
                            'name': client_name,
                            'phone': contact.get('PHONE', [{}])[0].get('VALUE', '') if contact.get('PHONE') else '',
                            'email': contact.get('EMAIL', [{}])[0].get('VALUE', '') if contact.get('EMAIL') else ''
                        },
                        'car_info': {
                            'brand': item.get('ufCrm8MarkaAvto'),
                            'vin': item.get('ufCrm8Vin'),
                            'year': item.get('ufCrm8GodVypuska'),
                            'photos': photos,
                            'stage_id': item.get('stageId')
                        },
                        'deal_info': {
                            'id': deal['ID'],
                            'status': deal.get('STAGE_NAME', deal.get('STAGE_ID'))
                        }
                    }
                    result.append(car_info)

        return result

    except Exception as e:
        print(f"Ошибка при поиске по фамилии: {str(e)}")
        return result


def save_to_json(data, filename):
    """Сохранение данных в JSON файл"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Данные сохранены в файл: {filename}")


# Пример использования
if __name__ == "__main__":
    # Поиск по VIN
    vin_data = get_car_info_by_vin("1234567890")
    save_to_json(vin_data, 'car_info_by_vin.json')

    # Поиск по фамилии
    lastname = "Файзулина"
    lastname_data = get_cars_by_client_lastname(lastname)
    save_to_json(lastname_data, f'cars_by_lastname_{lastname}.json')

    # Вывод результатов поиска по фамилии
    print(f"\nНайдено {len(lastname_data)} автомобилей для клиентов с фамилией '{lastname}':")
    for i, car in enumerate(lastname_data, 1):
        print(f"\nАвтомобиль #{i}:")
        print(f"Клиент: {car['client_info']['name']}")
        print(f"Телефон: {car['client_info']['phone']}")
        print(f"Email: {car['client_info']['email']}")
        print(f"Марка: {car['car_info']['brand']}")
        print(f"VIN: {car['car_info']['vin']}")
        print(f"Год выпуска: {car['car_info']['year']}")
        print(f"Статус сделки: {car['deal_info']['status']}")
        print(f"Фото: {len(car['car_info']['photos'])} шт.")
