import { useContext } from 'react';
import { useNavigate } from 'react-router-dom';
import { UserContext } from './UserContext';

const FavoritesCard = ({ id, title, description, image, onRemove }) => {
    const navigate = useNavigate();
    const { user } = useContext(UserContext);

    const handleNavigate = () => {
        navigate(`/home/${id}`); // Update the route to match your home finder app
    };

    const handleRemove = (e) => {
        e.stopPropagation(); // Prevent navigation when clicking on the remove button
        onRemove(id); // Assuming this function removes the favorite by ID
    };

    return (
        <div className='home-card' onClick={handleNavigate} style={{ position: 'relative' }}>
            <button className='delete-button' onClick={handleRemove}>X</button>
            <div className='home-image'>
                <img src={image} alt={title} />
            </div>
            <div className='home-details'>
                <h3 className='home-title'>{title}</h3>
                <p className='home-description'>{description}</p>
            </div>
        </div>
    );
};

export default FavoritesCard;
