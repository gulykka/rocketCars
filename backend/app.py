from flask import Flask, render_template, request, redirect, url_for, session, flash
from fast_bitrix24 import Bitrix
from pprint import pprint
from play import *
from dotenv import load_dotenv
import json
import os
app = Flask(__name__)
app.secret_key = 'rocketCar'
load_dotenv()
WEBHOOK_URL = "https://rocketcars.bitrix24.ru/rest/1978/a5wanv92ux3qsw3w/"

ENTITY_TYPE_ID = '135'
bx = Bitrix(WEBHOOK_URL)


def load_stages_from_json(file_path='resp.json'):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def get_tracking_info(current_stage_id, all_stages):
    stage_groups = {
        '1. На оплате/на заводе': ['DT135_12:NEW'],
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

        tracking_data[group_name] = {
            'completed': is_completed,
            'current': is_current,
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


@app.route('/api/<lastname>/<vin>', methods=['GET', 'POST'])
def login(lastname, vin):
    # if request.method == 'GET':
    #     data = get_car_info_by_vin(vin)
    #
    #     return {'status_code': 405, 'data': data}

    if request.method == 'GET':
        last_name = lastname.strip()
        print(lastname, vin)

        try:
            # Получаем данные по VIN
            data = get_car_info_by_vin(vin, lastname)
            print(data)
            # Проверяем наличие данных
            if not data['person_data']:
                return {'status_code': 404, 'message': 'Автомобиль не найден'}

            # Проверяем фамилию
            db_last_name = data['person_data'].get('LAST_NAME', '').strip()
            print(db_last_name)
            if not db_last_name or db_last_name == "Нет данных":
                return {'status_code': 404, 'message': 'Данные о владельце отсутствуют'}

            if last_name.lower() != db_last_name.lower():
                return {'status_code': 403, 'message': 'Фамилия не совпадает'}

            # Успешная авторизация
            return {
                'status_code': 200,
                'message': 'Успешная авторизация',
                'data': data
            }

        except ValueError as e:
            return {'status_code': 404, 'message': str(e)}


if __name__ == '__main__':
    app.run(debug=True)
