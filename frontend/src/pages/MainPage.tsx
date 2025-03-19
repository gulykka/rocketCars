import React from 'react';
import './pages.sass'
import '../components/main.sass'
import {ICar, IStatus} from "../interfaces";
import StatusCardsList from "../components/StatusCardsList";
import CarCard from "../components/CarCard";


const MainPage = () => {

    const cards:IStatus[] = [
        {
            index: '1',
            statusName: 'На оплате',
            information: 'Ваш автомобиль куплен и направляется \n' +
                'на стоянку в приграничном городе в Китае',
            is_active: false,
            date: '01.01.2025'
        },
        {
            index: '2',
            statusName: 'На стоянке в Китае',
            information: 'Ваш автомобиль прибыл на стоянку \n' +
                'в приграничном городе в Китае',
            is_active: false,
            date: '06.01.2025'
        },
        {
            index: '3',
            statusName: 'Доставка в РФ',
            information: 'Ваш автомобиль погружен и отправляется в Россию',
            is_active: true,
            date: '10.01.2025'
        }
    ]

    const car:ICar = {
        name: 'Changan UNI-T',
        VIN: 'LS5A3DKE8PA701334',
        year_release: '2023',
        photos: ['photo_1.jpg', 'photo_2.jpg', 'photo_3.jpg']
    }

    return (
        <div className={'main_page_container'}>
            <StatusCardsList statuses={cards.reverse()} />
            <CarCard car={car} />
        </div>
    );
};

export default MainPage;