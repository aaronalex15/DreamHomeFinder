import { useNavigate } from 'react-router-dom';

const HomeCard = ({ id, title, location, photo }) => {
    const navigate = useNavigate();

    const handleNavigate = () => {
        navigate(`/homes/${id}`);
    };

    return (
        <div className='home-container' onClick={handleNavigate}>
            <div id='home-photo'>
                <img src={photo} alt={title} />
            </div>
            <div className="text-content">
                <h3 id='home-title'>{title}</h3>
                <div id='home-location'>
                    <span>{location}</span>
                </div>
            </div>
        </div>
    );
};

export default HomeCard;
