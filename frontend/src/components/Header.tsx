import React from 'react';
import {useAppDispatch, useAppSelector} from "../hooks/redux-hooks";
import {signOut} from "../store/slices/carSlice";

const Header = () => {
    const dispatch = useAppDispatch();
    const isAuth = useAppSelector(state => state.car.isAuth)


    return (
        <header>
            {isAuth && <img className={'img_logo_mini'} src={'logo.png'} alt={''}/>}
            <div className={'buttons_container'}>
                {isAuth &&
                    <button
                        onClick={() => dispatch(signOut())}
                        title={'Выйти'}
                        className={'home_button'}>
                        <img
                            className={'out_button_img'}
                            src={'signout_button.png'}
                            alt={'Выйти'}/>
                    </button>
                }
                {isAuth &&
                    <button
                        title={'Главная страница'}
                        className={'home_button'}>
                        <img
                            className={'home_button_img'}
                            src={'home_button.png'}
                            alt={'Главная страница'}/>
                    </button>}
            </div>
        </header>
    );
};

export default Header;