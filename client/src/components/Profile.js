import ProfileEditForm from "./ProfileEditForm";
import { useContext } from "react";
import { UserContext } from "./UserContext";
import { useNavigate } from "react-router-dom";

const Profile = () => {
  const { user } = useContext(UserContext);
  const navigate = useNavigate();

  return user ? (
    <>
      <div id="edit-profile-title">
        <h3>Edit Your Profile</h3>
      </div>
      <ProfileEditForm />
    </>
  ) : (
    <>
      <div className="nav-error">You must be logged in to view this page.</div>
      <button className="error-nav" onClick={() => navigate("/")}>
        Go to Login
      </button>
    </>
  );
};

export default Profile;
