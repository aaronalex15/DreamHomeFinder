import React from "react";
import RegistrationForm from "./RegistrationForm"; // Assuming RegistrationForm component

const Home = () => {
  return (
    <div className="homepage-container">
      <div className="image-container">
        <img src="homepage.png" alt="family in front of home" />
      </div>
      <RegistrationForm /> Assuming this component handles registration
    </div>
  );
};

export default Home;
