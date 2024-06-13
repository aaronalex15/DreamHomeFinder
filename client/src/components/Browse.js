import { useEffect, useState, useContext } from "react";
import toast from "react-hot-toast";
import HomeCard from "./HomeCard"; // Assuming you have a HomeCard component
import { UserContext } from "./UserContext";
import { useNavigate } from "react-router-dom";

const Browse = () => {
  const { user } = useContext(UserContext);
  const navigate = useNavigate();
  const [homes, setHomes] = useState([]);
  const [location, setLocation] = useState("");
  const [priceRange, setPriceRange] = useState("");
  const [bedrooms, setBedrooms] = useState("");

  const locations = [
    "Downtown",
    "Suburbs",
    "Countryside",
    "Beachfront",
    "Mountains",
    "Rural",
  ];
  const priceRanges = [
    "$100,000 - $200,000",
    "$200,000 - $300,000",
    "$300,000 - $400,000",
    "$400,000 - $500,000",
  ];
  const bedroomOptions = [
    "1 Bedroom",
    "2 Bedrooms",
    "3 Bedrooms",
    "4+ Bedrooms",
  ];

  useEffect(() => {
    const fetchHomes = () => {
      const queryParams = new URLSearchParams({
        ...(location && { location }),
        ...(priceRange && { price_range: priceRange }),
        ...(bedrooms && { bedrooms }),
      }).toString();

      fetch(`/homes?${queryParams}`)
        .then((res) => {
          if (res.ok) {
            return res.json().then(setHomes);
          }
          return res.json().then((errorObj) => toast.error(errorObj.Error));
        })
        .catch((err) => {
          toast.error("An unexpected error occurred.");
        });
    };

    fetchHomes();
  }, [location, priceRange, bedrooms]); // Refetch when filters change

  const handleLocationChange = (e) => setLocation(e.target.value);
  const handlePriceRangeChange = (e) => setPriceRange(e.target.value);
  const handleBedroomsChange = (e) => setBedrooms(e.target.value);

  const mappedHomes = homes.map((home) => (
    <HomeCard
      key={home.id}
      id={home.id}
      title={home.title} // Replace with appropriate property name for home title
      location={home.location} // Replace with appropriate property name for home location
      photo={home.photo} // Replace with appropriate property name for home photo
    />
  ));

  return user ? (
    <div className="main-container">
      <h3>Browse Homes</h3>
      <div className="filters">
        <select value={location} onChange={handleLocationChange}>
          <option value="">Select Location</option>
          {locations.map((location) => (
            <option key={location} value={location}>
              {location}
            </option>
          ))}
        </select>
        <select value={priceRange} onChange={handlePriceRangeChange}>
          <option value="">Select Price Range</option>
          {priceRanges.map((range) => (
            <option key={range} value={range}>
              {range}
            </option>
          ))}
        </select>
        <select value={bedrooms} onChange={handleBedroomsChange}>
          <option value="">Select Bedrooms</option>
          {bedroomOptions.map((option) => (
            <option key={option} value={option}>
              {option}
            </option>
          ))}
        </select>
      </div>
      <div className="homes-grid">
        {mappedHomes.length > 0 ? mappedHomes : <p>Loading...</p>}
      </div>
    </div>
  ) : (
    <>
      <div className="nav-error">You must be logged in to view this page.</div>
      <button className="error-nav" onClick={() => navigate("/")}>
        Go to Login
      </button>
    </>
  );
};

export default Browse;
