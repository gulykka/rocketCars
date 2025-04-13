import React, { FC, useEffect, useState } from 'react';
import ShadowWindow from "./ShadowWindow";
import 'react-slideshow-image/dist/styles.css';
import { useAppSelector } from "../hooks/redux-hooks";
import { CarData, CarPhoto } from "../store/types/carTypes";

const CarCard: FC = () => {
    const car = useAppSelector(state => state.car.data?.car_data) as CarData;
    const status = useAppSelector(state => state.car.status);
    const [chosenPhoto, setChosenPhoto] = useState(0);
    const [visibleImageWindow, setVisibleImageWindow] = useState(false);

    // useEffect(() => {
    //     if (status === 'succeeded') {
    //         console.log("Данные о машине загружены:", car);
    //     }
    // }, [status]); // Добавляем car в зависимости


    return (
        <div className={'car_information_container'}>
            <div className={'information_car_container'}>
                <span className={'name_car'}>{car?.car_make}</span>
                <div>
                    <span className={'VIN'}>VIN</span>
                    <span className={'VIN_info'}> {car?.vin}</span>
                </div>
                <span className={'VIN_info'}>Год выпуска {car?.car_release_date}</span>
            </div>
            <div className={'photos_car_container'}>
                {car?.photo?.length > 0 ? (
                    car.photo.map((ph: CarPhoto, index: number) => (
                        <img
                            key={index}
                            onClick={() => {
                                setVisibleImageWindow(true);
                                setChosenPhoto(index);
                            }}
                            className={'photo_car'}
                            src={`${ph.urlMachine}`}
                            alt={`Фото автомобиля ${car.car_make}`}
                            onError={() => console.error(`Ошибка загрузки изображения: ${ph.urlMachine}`)} // Лог ошибок
                        />

                    ))
                ) : (
                    <div>Нет доступных фотографий.</div> // Сообщение, если фотографий нет
                )}
            </div>
            {visibleImageWindow && (
                <ShadowWindow
                    selectedIndex={chosenPhoto}
                    imageSrc={car.photo}
                    onClose={() => setVisibleImageWindow(false)}
                />
            )}
        </div>
    );
};

export default CarCard;

