import React, {FC} from 'react';

export interface IStatus {
    index: number
    statusName: string
    is_active: boolean
    description: string
    date: string
}


const StatusCard: FC<IStatus> = ({index, statusName, is_active, description, date}) => {
    return (
        <div className={'status_card_container'}>
            <div className={'image_container'}>
                {!is_active ?
                    <img
                        className={'status_image'}
                        src={'current_status_img.png'}
                        alt={''}/>
                    :
                    <img
                        className={'status_image'}
                        src={'copplete_status_img.png'}
                        alt={''}/>}
            </div>
            <div className={'container_grey'}>
                <div className={'information_container'}>
                    <span style={{fontWeight: 'bold', fontSize: '25px'}}>{statusName}</span>
                    <span style={{fontSize: '18px'}}>{description}</span>
                </div>
                {date &&
                    <span className={!is_active ? 'current_date' : 'date_container'}>
                    {date?.slice(0, 5)}
                </span>
                }
            </div>

        </div>
    );
};

export default StatusCard;