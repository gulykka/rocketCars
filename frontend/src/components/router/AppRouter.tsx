import React from 'react';
import {Route, Routes} from "react-router-dom";
import LogInPage from "../../pages/LogInPage";
import MainPage from "../../pages/MainPage";
import PrivateRouter from "./PrivateRouter";
import NotFoundPage from "../../pages/NotFoundPage";

const AppRouter = () => {
    return (
        <Routes>
            <Route path={'/'} element={<LogInPage />} />
            <Route path={'/main'} element={<PrivateRouter element={<MainPage />} /> } />
            <Route path={'*'} element={<NotFoundPage />} />
        </Routes>
    );
};

export default AppRouter;