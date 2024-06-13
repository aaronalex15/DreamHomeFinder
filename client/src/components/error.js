import { useContext } from 'react';
import { useNavigate } from 'react-router-dom';
import { UserContext } from './UserContext';

const Error = () => {
    const { user } = useContext(UserContext);
    const navigate = useNavigate();

    const handleGoBack = () => {
        navigate(-1); // Navigate back in history
    };

    const handleGoHome = () => {
        navigate('/'); // Navigate to the home page
    };

    return (
        <article className='non-route'>
            {user ? (
                <p className='nav-error'>An error occurred. Please try again.</p>
            ) : (
                <p className='nav-error'>You must be logged in to view this page.</p>
            )}
            <button className='error-nav' onClick={handleGoBack}>Go Back</button>
            <button className='error-nav' onClick={handleGoHome}>Return Home</button>
        </article>
    );
};

export default Error;
