import { createContext, useState, useEffect } from 'react';
import toast from 'react-hot-toast';

export const UserContext = createContext();

const UserProvider = ({ children }) => {
    const [user, setUser] = useState(null);

    const login = (user) => {
        setUser(user);
    };

    const logout = () => {
        try {
            fetch('/logout', { method: 'DELETE' })
                .then((res) => {
                    if (res.status === 204) {
                        setUser(null);
                        toast.success("You've been logged out!");
                    } else {
                        toast.error('Something went wrong while logging out. Please try again.');
                    }
                })
                .catch((err) => {
                    throw err;
                });
        } catch (err) {
            throw err;
        }
    };

    // Fetch user on mount to check if already authenticated
    useEffect(() => {
        fetch('/me')
            .then((resp) => {
                if (resp.ok) {
                    resp.json().then((data) => {
                        setUser(data); // Assuming 'data' contains user information
                    });
                } else {
                    setUser(null); // Not logged in
                    toast.error('Please log in');
                }
            })
            .catch((error) => {
                console.error('Error fetching user:', error);
                toast.error('Failed to fetch user information.');
            });
    }, []);

    return (
        <UserContext.Provider value={{ user, login, logout }}>
            {children}
        </UserContext.Provider>
    );
};

export default UserProvider;
