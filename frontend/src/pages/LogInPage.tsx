import React, {useEffect} from 'react';
import LogIn from "../components/LogIn";
import './pages.sass'
import {useAppDispatch} from "../hooks/redux-hooks";
import {useNavigate} from "react-router-dom";
import {fetchGetCar} from "../store/slices/carSlice";

const LogInPage = () => {
    const dispatch = useAppDispatch();
    const navigation = useNavigate();

    useEffect(() => {
        const name = localStorage.getItem('carName');
        const VIN = localStorage.getItem('carVIN');
        if (name && VIN) {
            dispatch(fetchGetCar({ name, VIN }))
                .unwrap()
                .then(() => {
                    navigation('/main');
                })
                .catch(() => {
                    console.error('Ошибка при получении данных о машине');
                });
        }
    }, [dispatch]);
    return (
        <div className={'login_page_container'}>
            <LogIn />
        </div>
    );
};

export default LogInPage;