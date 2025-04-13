import React, {FC, useEffect} from 'react';
import PhotoSlider from "./PhotoSlider";
import {CarPhoto} from "../store/types/carTypes";

interface ShadowWindowProps {
    onClose: () => void
    imageSrc: CarPhoto[]
    selectedIndex: number
}

const ShadowWindow: FC<ShadowWindowProps> = ({ imageSrc, onClose, selectedIndex }) => {
    useEffect(() => {
        const handleKeyDown = (event: KeyboardEvent) => {
            if (event.key === 'Escape') {
                onClose();
            }
        };
        window.addEventListener('keydown', handleKeyDown);
        return () => {
            window.removeEventListener('keydown', handleKeyDown);
        };
    }, [onClose]);

    return (
        <>
            <div className="overlay" onClick={onClose} />
            <div className="shadow_window_img_container">
                {imageSrc.length > 0 ? (
                    <PhotoSlider
                        selectedIndex={selectedIndex}
                        images={imageSrc} />
                ) : (
                    <p>No images available</p>
                )}
            </div>
        </>
    );

};

export default ShadowWindow;