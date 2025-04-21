from fastapi import FastAPI, HTTPException, Path, status
from play import *
import json
from typing import Dict, Any

app = FastAPI()


def load_stages_from_json(file_path='resp.json') -> Dict[str, Any]:
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def get_tracking_info(current_stage_id: str, all_stages: Dict[str, Any]) -> Dict[str, Any]:
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


@app.get("/api/{lastname}/{vin}", response_model=Dict[str, Any])
async def get_car_info(
        lastname: str = Path(..., description="Фамилия владельца"),
        vin: str = Path(..., description="VIN номер автомобиля")
):
    last_name = lastname.strip()

    try:
        # Получаем данные по VIN
        data = await get_car_info_by_vin(vin, lastname)

        # Проверяем наличие данных
        if not data['person_data']:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Автомобиль не найден"
            )

        # Проверяем фамилию
        db_last_name = data['person_data'].get('LAST_NAME', '').strip()

        if not db_last_name or db_last_name == "Нет данных":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Данные о владельце отсутствуют"
            )

        if last_name.lower() != db_last_name.lower():
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Фамилия не совпадает"
            )

        # Успешный ответ
        return {
            "status_code": status.HTTP_200_OK,
            "message": "Успешная авторизация",
            "data": data
        }

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=5000)
