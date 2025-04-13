import React, {useEffect} from 'react';
import './pages.sass';
import '../components/main.sass';
import StatusCardsList from "../components/StatusCardsList";
import CarCard from "../components/CarCard";

const MainPage = () => {


    return (
        <div className={'main_page_container'}>
            <StatusCardsList />
            <CarCard />
        </div>
    );
};

export default MainPage;
