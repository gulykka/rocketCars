import React, { useEffect, useState } from 'react';
import {useAppSelector} from "../hooks/redux-hooks";

const LoadingPage: React.FC = () => {
    const status = useAppSelector(state => state.car.status);
    const [loadingProgress, setLoadingProgress] = useState(0);
    const [isLoading, setIsLoading] = useState(false); // Новое состояние для отслеживания загрузки
    const totalDuration = 5000; // 5 секунд
    const intervalDuration = 100; // Каждые 100 мс обновляем прогресс

    useEffect(() => {
        console.log(0)
        if (!isLoading) { // Проверяем, не запущена ли уже загрузка
            setIsLoading(true); // Устанавливаем, что загрузка началась
            const totalSteps = totalDuration / intervalDuration; // Количество шагов
            const progressIncrement = 100 / totalSteps; // Увеличение прогресса на каждом шаге

            const interval = setInterval(() => {
                setLoadingProgress(prev => {
                    if (prev < 100) {
                        return Math.min(prev + progressIncrement, 100);
                    } else {
                        clearInterval(interval);
                        return prev;
                    }
                });
            }, intervalDuration);

            const timeout = setTimeout(() => {
                clearInterval(interval);
                setLoadingProgress(100);
                setIsLoading(false)
            }, totalDuration);

            return () => {
                clearInterval(interval);
                clearTimeout(timeout);
            };
        }
    }, [totalDuration]); // Добавляем isLoading в зависимости

    return (
        <div className="loading_page_container">
            <img
                style={{ width: '120px', height: '120px' }}
                src={'logo.png'} alt="Loading logo" />
            <div className="loading_bar">
                <div className="progress_line" style={{ width: `calc(${loadingProgress}% - 10px)` }}>l</div>
                <p className={'progress'}>{loadingProgress}%</p>
            </div>
        </div>
    );
};

export default LoadingPage;

