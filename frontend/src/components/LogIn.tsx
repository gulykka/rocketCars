import React from 'react';
import './components.sass'
import FormSignIn from "./FormSignIn";

const LogIn = () => {
    return (
        <div className={'login_container'}>
            <img src={'logo.png'} alt={''} className={'img_logo'}/>
            <label className={'title'}>Где мой автомобиль?</label>
            <FormSignIn />
        </div>
    );
};

export default LogIn;