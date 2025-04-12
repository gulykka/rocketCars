import React, { useState } from 'react';
import { useDispatch } from 'react-redux';


const FormSignIn = () => {
    const [visibleName, setVisibleName] = useState(false);
    const [name, setName] = useState('');
    const [visibleVIN, setVisibleVIN] = useState(false);
    const [VIN, setVIN] = useState('');
    const [carData, setCarData] = useState<any>(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const dispatch = useDispatch()

    const fetchData = async () => {
        if (!name || !VIN) {
            setError('Пожалуйста, заполните все поля');
            return;
        }

        setLoading(true);
        setError(null);

        try {
            const response = await fetch(`/api/${encodeURIComponent(name)}/${encodeURIComponent(VIN)}`, {
                headers: {
                    'Content-Type': 'application/json',
                },
            });

            if (!response.ok) {
                throw new Error(`Ошибка HTTP: ${response.status}`);
            }

            const data = await response.json();
            setCarData(data);
//             dispatch(login())
            console.log(data)
        } catch (err: any) {
            setError(err.message || 'Произошла ошибка при загрузке данных');
            console.error('Ошибка запроса:', err);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className={'form_signin_container'}>
            <div className="input-container">
                <input
                    type="text"
                    id="myInput"
                    value={name}
                    onChange={(event) => setName(event.target.value)}
                    onFocus={() => setVisibleName(true)}
                    onBlur={() => setVisibleName(false)}
                    placeholder=" "
                    disabled={loading}
                />
                <label className="placeholder" htmlFor="myInput">Введите вашу фамилию</label>
                {((visibleName) || (name && !visibleName)) && <label className={'background'}>0</label>}
            </div>
            <div className="input-container">
                <input
                    type="text"
                    id="mySecondInput"
                    onFocus={() => setVisibleVIN(true)}
                    onBlur={() => setVisibleVIN(false)}
                    value={VIN}
                    onChange={(event) => setVIN(event.target.value)}
                    placeholder=" "
                    disabled={loading}
                />
                <label className="placeholder" htmlFor="mySecondInput">Введите VIN</label>
                {((visibleVIN) || (VIN && !visibleVIN)) && <label className={'background_VIN'}>0</label>}
            </div>

            {error && <div className="error-message">{error}</div>}

            <button
                onClick={fetchData}
                className={'button_signin'}
                disabled={loading}
            >
                {loading ? 'Загрузка...' : 'Проверить'}
            </button>

            {carData && (
                <div className="car-data-container">
                    <h3>Данные автомобиля:</h3>
                    <pre>{JSON.stringify(carData, null, 2)}</pre>
                </div>
            )}
        </div>
    );
};

export default FormSignIn;