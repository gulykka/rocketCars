import React from 'react';
import Slider from 'react-slick';
import {CarPhoto} from "../store/types/carTypes";

interface PhotoSliderProps {
    images: CarPhoto[]
    selectedIndex: number
}

// Определите типы для пропсов стрелок
type ArrowProps = React.ComponentProps<'button'>;

const CustomPrevArrow: React.FC<ArrowProps> = (props) => {
    return (
        <button {...props} style={{ background: 'transparent', border: 'none', cursor: 'pointer' }}>
            <img src="arrow-left.png" alt="Previous" style={{ width: '50px', height: '50px'}} />
        </button>
    );
};

const CustomNextArrow: React.FC<ArrowProps> = (props) => {
    return (
        <button {...props} style={{ background: 'transparent', border: 'none', cursor: 'pointer' }}>
            <img src="arrow-right.png" alt="Next" style={{ width: '50px', height: '50px'}} />
        </button>
    );
};

const PhotoSlider: React.FC<PhotoSliderProps> = ({ images, selectedIndex }) => {
    const settings = {
        dots: true,
        infinite: true,
        slidesToShow: 1,
        slidesToScroll: 1,
        autoplay: false,
        arrows: true,
        initialSlide: selectedIndex,
        prevArrow: <CustomPrevArrow />,
        nextArrow: <CustomNextArrow />,
    };

    return (
        <Slider {...settings} className={'slider'}>
            {images.map((image, index) => (
                <div key={index}>
                    <img src={image.urlMachine} alt={`Slide ${index}`} style={{ width: '100%', height: 'auto' }} />
                </div>
            ))}
        </Slider>
    );
};

export default PhotoSlider;
