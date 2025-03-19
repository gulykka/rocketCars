import React, {FC, useState} from 'react';
import {ICar} from "../interfaces";
import ShadowWindow from "./ShadowWindow";
import 'react-slideshow-image/dist/styles.css'

interface CarCardProps {
    car: ICar
}

const CarCard:FC<CarCardProps> = ({car}) => {

    const [visibleImageWindow, setVisibleImageWindow] = useState(false)

    return (
        <div className={'car_information_container'}>
            <div className={'information_car_container'}>
                <span className={'name_car'}>{car.name}</span>
                <div>
                    <span className={'VIN'}>VIN</span>
                    <span className={'VIN_info'}> {car.VIN}</span>
                </div>
                <span className={'VIN_info'} >Год выпуска {car.year_release}</span>
            </div>
            <div className={'photos_car_container'}>
                {car.photos.map((img) =>
                <img
                    onClick={() => setVisibleImageWindow(true)}
                    className={'photo_car'}
                    src={img}
                    alt={''}/>
                )}
            </div>
            {visibleImageWindow && (
                <ShadowWindow
                    imageSrc={car.photos}
                    onClose={() => setVisibleImageWindow(false)}/>
            )}
        </div>
    );
};

export default CarCard;