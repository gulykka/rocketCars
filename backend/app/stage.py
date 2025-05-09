# 1. Получаем элемент смарт-процесса
from fast_bitrix24 import Bitrix
import json

# Настройки подключения
WEBHOOK_URL = ""
ENTITY_TYPE_ID = '135'  # ID смарт-процесса

# Инициализация клиента Bitrix24
bx = Bitrix(WEBHOOK_URL)
smart_process_result = bx.get_all('crm.item.list', {
    'entityTypeId': '135',  # ID смарт-процесса
    'filter': {
        'ufCrm8Vin': '1234567890'  # Пример фильтра по VIN
    },
    'select': ['*', 'ufCrm8FotoAvto']  # Выбираем все поля + фото
})

# 2. Получаем stageId из результата
stage_id = smart_process_result[0]['stageId']

# 3. Получаем информацию о стадии
statuses = bx.get_all('crm.status.list', {
    'filter': {
        'ENTITY_ID': 'DYNAMIC_135_STAGE_12'  # Формат: DYNAMIC_<ID смарт-процесса>_STAGE_<ID воронки>
    }
})
print(statuses)
stage_info = next((status for status in statuses if status['STATUS_ID'] == stage_id), None)

if stage_info:
    print(f"Текущая стадия: {stage_info['NAME']} (Цвет: {stage_info['COLOR']})")
else:
    print(f"Стадия с ID {stage_id} не найдена.")

