import React, {useState} from 'react';

const FormSignIn = () => {
    const [visibleName, setVisibleName] = useState(false)
    const [name, setName] = useState('')
    const [visibleVIN, setVisibleVIN] = useState(false)
    const [VIN, setVIN] = useState('')

    return (
        <div className={'form_signin_container'}>
            <div className="input-container">
                <input
                    type="text"
                    id="myInput"
                    value={name}
                    onChange={event => setName(event.target.value)}
                    onFocus={() => setVisibleName(true)}
                    onBlur={() => setVisibleName(false)}
                    placeholder=" "/>
                <label className="placeholder" htmlFor="myInput">Введите ваше имя и фамилию</label>
                {((visibleName) || (name && !visibleName)) && <label className={'background'}>0</label>}
            </div>
            <div className="input-container">
                <input
                    type="text"
                    id="mySecondInput"
                    onFocus={() => setVisibleVIN(true)}
                    onBlur={() => setVisibleVIN(false)}
                    value={VIN}
                    onChange={event => setVIN(event.target.value)}
                    placeholder=" "/>
                <label className="placeholder" htmlFor="mySecondInput">Введите VIN</label>
                {((visibleVIN) || (VIN && !visibleVIN)) && <label className={'background_VIN'}>0</label>}
            </div>
            <button className={'button_signin'}>Проверить</button>
        </div>
    );
};

export default FormSignIn;