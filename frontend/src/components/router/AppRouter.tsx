import React from 'react';
import {Route, Routes} from "react-router-dom";
import LogInPage from "../../pages/LogInPage";
import MainPage from "../../pages/MainPage";

const AppRouter = () => {
    return (
        <Routes>
            <Route path={'/'} element={<LogInPage />} />
            <Route path={'/main'} element={<MainPage />} />
        </Routes>
    );
};

export default AppRouter;