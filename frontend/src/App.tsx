import React, { useEffect, useState } from 'react';
import './App.css';
import Header from "./components/Header";
import Footer from "./components/Footer";
import AppRouter from "./components/router/AppRouter";
import { BrowserRouter as Router } from 'react-router-dom';
import { useAppSelector } from "./hooks/redux-hooks";
import LoadingPage from "./pages/LoadingPage";

function App() {
    const status = useAppSelector(state => state.car.status);

    return (
        <Router>
            {(status !== 'loading')
                ?
                <div className="App">
                    <Header />
                    <Footer />
                    <AppRouter />
                </div>
                :
                <LoadingPage />}
        </Router>
    );
}

export default App;
