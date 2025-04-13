import React, {useEffect, useState} from 'react';
import './App.css';
import Header from "./components/Header";
import Footer from "./components/Footer";
import AppRouter from "./components/router/AppRouter";
import {BrowserRouter as Router} from 'react-router-dom';
import {useAppSelector} from "./hooks/redux-hooks";
import LoadingPage from "./pages/LoadingPage";

function App() {
    const status = useAppSelector(state => state.car.status);
    const [loadingProgress, setLoadingProgress] = useState(0);
    const [loading, setLoading] = useState(true)

    useEffect(() => {
        if (status === 'loading') {
            const totalDuration = 5000; // 5 секунд
            const intervalDuration = 100; // Каждые 500 мс обновляем прогресс
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
                setLoading(false)
            }, totalDuration);

            return () => {
                clearInterval(interval);
                clearTimeout(timeout);
            };
        }
    }, [status]);
    return (
        <Router>
            {(status !== 'loading')
                ?
                <div className="App">
                    <Header/>
                    <Footer/>
                    <AppRouter/>
                </div>
                :
                <LoadingPage progress={loadingProgress}/>}
        </Router>
    );
}

export default App;
