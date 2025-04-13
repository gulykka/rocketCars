import React from 'react';

// Определяем интерфейс для пропсов
interface LoadingPageProps {
    progress: number; // Пропс progress должен быть числом
}

const LoadingPage: React.FC<LoadingPageProps> = ({ progress }) => {
    return (
        <div className="loading_page_container">
            <img
                style={{width: '120px', height: '120px'}}
                 src={'logo.png'} alt={''}/>
            <div className="loading_bar">
                <div className="progress_line" style={{ width: `calc(${progress}% - 10px)` }}>l</div>
                <p className={'progress'}>{progress}% </p>
            </div>

        </div>
    );
};

export default LoadingPage;
