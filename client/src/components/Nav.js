import { useContext } from "react";
import { NavLink, useLocation } from "react-router-dom";
import { UserContext } from "./UserContext";

const Nav = () => {
  const { user, logout } = useContext(UserContext);
  const location = useLocation();

  return (
    <header>
      <img src="/text-logo.png" id="text-logo" alt="Your App Name" />
      <img src="/logo.png" id="logo" alt="Logo" />
      <nav>
        {/* Show links if there is a user logged in */}
        {user && (
          <>
            <NavLink to="/search" className="nav-link">
              Search Homes
            </NavLink>
            <NavLink to="/favorites" className="nav-link">
              Favorites
            </NavLink>
            <NavLink to="/user/profile" className="nav-link">
              Profile
            </NavLink>
            <NavLink to="/" className="nav-link" onClick={logout}>
              Logout
            </NavLink>
          </>
        )}
        {/* Show the Home link only if there is no user and we are not on the homepage */}
        {!user && location.pathname !== "/" && (
          <NavLink to="/" className="nav-link">
            Home
          </NavLink>
        )}
      </nav>
    </header>
  );
};

export default Nav;
