from fast_bitrix24 import Bitrix
from pprint import pprint

WEBHOOK_URL = "https://rocketcars.bitrix24.ru/rest/1978/a5wanv92ux3qsw3w/"
bx = Bitrix(WEBHOOK_URL)


def get_all_stages(entity_type_id):
    """
    Получает ВСЕ стадии смарт-процесса, включая все воронки
    """
    try:
        # 1. Сначала получаем все категории (воронки)
        categories = bx.get_all(
            'crm.category.list',
            params={'entityTypeId': entity_type_id}
        )

        # 2. Для каждой категории получаем стадии
        all_stages = []
        for category in categories:
            stages = bx.get_all(
                'crm.item.stage.list',
                params={
                    'entityTypeId': entity_type_id,
                    'categoryId': category['id']
                }
            )
            all_stages.extend(stages)

        return all_stages

    except Exception as e:
        print(f"Ошибка: {e}")
        return []


# Пример использования
all_stages = get_all_stages('135')  # ID вашего смарт-процесса
pprint(all_stages)