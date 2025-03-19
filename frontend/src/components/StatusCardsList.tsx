import React, {FC} from 'react';
import {IStatus} from "../interfaces";
import StatusCard from "./StatusCard";
import './main.sass'

interface StatusCardsListProps {
    statuses: IStatus[]
}

const StatusCardsList:FC<StatusCardsListProps> = ({statuses}) => {
    return (
        <div className={'status_cards_container'}>
            {statuses.map((status) => <StatusCard
                index={status.index}
                statusName={status.statusName}
                information={status.information}
                date={status.date}
                is_active={status.is_active} />
                )}
        </div>
    );
};

export default StatusCardsList;