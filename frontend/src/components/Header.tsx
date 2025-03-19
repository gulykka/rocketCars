import React from 'react';

const Header = () => {

    const isAuth = true

    function signOut() {

    }

    return (
        <header>
            {isAuth && <img className={'img_logo_mini'} src={'logo.png'} alt={''}/>}
            <div className={'buttons_container'}>
                {isAuth &&
                    <button className={'home_button'}>
                        <img
                            onClick={signOut}
                            className={'out_button_img'}
                            src={'signout_button.png'}
                            alt={''}/>
                    </button>
                }
                <button className={'home_button'}>
                    <img
                        className={'home_button_img'}
                        src={'home_button.png'}
                        alt={''}/>
                </button>
            </div>
        </header>
    );
};

export default Header;