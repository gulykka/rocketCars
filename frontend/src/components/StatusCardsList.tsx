import React, {FC} from 'react';
import StatusCard from "./StatusCard";
import './main.sass'
import {useAppSelector} from "../hooks/redux-hooks";
import {TrackingGroup} from "../store/types/carTypes";


const StatusCardsList = () => {

    const statuses = useAppSelector(state => state.car.data?.tracking_info)
    const statusesName = statuses ? Object.keys(statuses) : null
    const date = useAppSelector(state => state.car.data?.stage_history)

    return (
        <div className={'status_cards_container'}>
            {statusesName?.reverse().map((status, index) =>
                <StatusCard
                    description={statuses ? statuses[status].description : ''}
                    key={index}
                    index={index}
                    statusName={status}
                    date={date ? date[index] : ''}
                    is_active={statuses ? statuses[status].completed : false}/>
            )}

        </div>
    );
};

export default StatusCardsList;