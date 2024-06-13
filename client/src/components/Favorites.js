import { useEffect, useState, useContext } from 'react';
import { UserContext } from './UserContext';
import { useNavigate } from 'react-router-dom';
import toast from 'react-hot-toast';
import FavoritesCard from './FavoritesCard'; // Assuming you have a component for displaying favorites

const Favorites = () => {
    const { user } = useContext(UserContext);
    const navigate = useNavigate();
    const [favorites, setFavorites] = useState([]);

    useEffect(() => {
        if (user) {
            fetch(`/users/${user.id}/favorites`) // Adjust endpoint according to your API
                .then((res) => {
                    if (res.ok) {
                        return res.json().then(setFavorites);
                    }
                    return res.json().then((errorObj) => toast.error(errorObj.Error));
                })
                .catch((error) => {
                    console.error('Failed to fetch favorites:', error);
                    toast.error('An unexpected error occurred.');
                });
        }
    }, [user]);

    const removeFavorite = (favoriteId) => {
        fetch(`/users/${user.id}/favorites/${favoriteId}`, { method: 'DELETE' })
            .then((res) => {
                if (res.ok) {
                    setFavorites((prevFavorites) => prevFavorites.filter((fav) => fav.id !== favoriteId));
                    toast.success('Favorite removed successfully.');
                } else {
                    return res.json().then((errorObj) => toast.error(errorObj.Error));
                }
            })
            .catch((error) => {
                console.error('Failed to remove favorite:', error);
                toast.error('Failed to remove favorite.');
            });
    };

    const mappedFavorites = favorites.map((favorite) => (
        <FavoritesCard
            key={favorite.id}
            id={favorite.id}
            title={favorite.title}
            description={favorite.description}
            image={favorite.image} // Adjust properties based on your favorite item structure
            onRemove={removeFavorite}
        />
    ));

    return user ? (
        <div className="main-container">
            <h3 className="stack">Your Favorites</h3>
            <div className="books-grid">
                {mappedFavorites.length > 0 ? (
                    mappedFavorites
                ) : (
                    <p>There are no favorites yet.</p>
                )}
            </div>
        </div>
    ) : (
        <>
            <div className="nav-error">You must be logged in to view this page.</div>
            <button className="error-nav" onClick={() => navigate('/')}>
                Go to Login
            </button>
        </>
    );
};

export default Favorites;
