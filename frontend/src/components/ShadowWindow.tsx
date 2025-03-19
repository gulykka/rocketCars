import React, {FC, useEffect} from 'react';
import PhotoSlider from "./PhotoSlider";

interface ShadowWindowProps {
    onClose: () => void;
    imageSrc: string[];
}

const ShadowWindow: FC<ShadowWindowProps> = ({ imageSrc, onClose }) => {
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
                    <PhotoSlider images={imageSrc} />
                ) : (
                    <p>No images available</p>
                )}
            </div>
        </>
    );

};

export default ShadowWindow;