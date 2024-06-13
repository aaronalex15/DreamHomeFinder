import React, { useEffect, useState, useContext } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { UserContext } from "./UserContext";
import toast from "react-hot-toast";

const HomeDetails = () => {
  const { user } = useContext(UserContext);
  const navigate = useNavigate();
  const { id } = useParams();
  const [home, setHome] = useState(null);
  const [showReviewModal, setShowReviewModal] = useState(false);
  const [reviewData, setReviewData] = useState({
    rating: "",
    review: "",
    rec_age: "",
  });

  useEffect(() => {
    fetch(`/homes/${id}`)
      .then((res) => {
        if (res.ok) {
          return res.json().then(setHome);
        }
        return res.json().then((errorObj) => toast.error(errorObj.Error));
      })
      .catch((error) => {
        console.error("Error fetching home details:", error);
        toast.error("Error fetching home details.");
      });
  }, [id]);

  if (!home) {
    return <div>Loading...</div>;
  }

  const handleAddReviewClick = () => {
    setShowReviewModal(true);
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    let formattedValue = value;
    if (name === "rating") {
      formattedValue = parseInt(value, 10); // Convert to integer
    }
    setReviewData((prev) => ({ ...prev, [name]: formattedValue }));
  };

  const handleSubmitReview = (e) => {
    e.preventDefault();
    fetch("/reviews", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        ...reviewData,
        home_id: home.id,
        user_id: user.id,
      }),
    })
      .then((res) => {
        if (res.ok) {
          return res.json().then((data) => {
            setShowReviewModal(false);
            setHome((prevHome) => ({
              ...prevHome,
              reviews: [...prevHome.reviews, data],
            }));
          });
        } else {
          return res.json().then((errorObj) => toast.error(errorObj.Error));
        }
      })
      .catch((error) => {
        console.error("Error submitting review:", error);
        toast.error("Failed to submit review.");
      });
  };

  const handleAddToStack = () => {
    if (!user || !user.id || !home || !home.id) {
      toast.error("Invalid operation.");
      return;
    }
    fetch(`/${user.id}/add_to_stack/${home.id}`, {
      method: "POST",
    })
      .then((res) => {
        if (res.ok) {
          return res.json().then(() => {
            toast.success("Home added to your stack!");
          });
        } else {
          return res.json().then((errorObj) => {
            toast.error(errorObj.Error);
          });
        }
      })
      .catch((error) => {
        console.error("Error adding home to stack:", error);
        toast.error("Failed to add home to stack.");
      });
  };

  return user ? (
    <div className="main-container">
      <div>
        <button
          id="back-button"
          onClick={() => {
            navigate(-1);
          }}
        >
          Back
        </button>
      </div>
      <div className="home-details-container">
        <div className="home-image">
          <img src={home.photo} alt={home.title} />
        </div>
        <div className="home-details">
          <span>
            <strong>Title:</strong> {home.title}
          </span>
          <span>
            <strong>Location:</strong> {home.location}
          </span>
          <span>
            <strong>Price:</strong> ${home.price}
          </span>
          <span>
            <strong>Bedrooms:</strong> {home.bedrooms}
          </span>
          <span>
            <strong>Bathrooms:</strong> {home.bathrooms}
          </span>
          <span>
            <strong>Area:</strong> {home.area} sqft
          </span>
          <span>
            <strong>Year Built:</strong> {home.year_built}
          </span>
          <p>{home.description}</p>
        </div>
      </div>
      <div className="buttons-container">
        <button onClick={handleAddToStack}>Add to Stack</button>
        <button onClick={handleAddReviewClick}>Add Review</button>
      </div>
      {showReviewModal && (
        <div className="review-container">
          <h3>Add Your Review</h3>
          <textarea
            placeholder="Write your review here..."
            name="review"
            value={reviewData.review}
            onChange={handleChange}
          />
          <select
            name="rating"
            value={reviewData.rating}
            onChange={handleChange}
          >
            <option value="">Select a rating</option>
            {[1, 2, 3, 4, 5].map((num) => (
              <option key={num} value={num}>
                {num}
              </option>
            ))}
          </select>
          <select
            name="rec_age"
            value={reviewData.rec_age}
            onChange={handleChange}
          >
            <option value="">Select recommended age</option>
            <option value="Single Family Home">Single Family Home</option>
            <option value="Condo">Condo</option>
            <option value="Townhouse">Townhouse</option>
            <option value="Apartment">Apartment</option>
          </select>
          <button onClick={handleSubmitReview}>Submit Review</button>
          <button id="close-button" onClick={() => setShowReviewModal(false)}>
            X
          </button>
        </div>
      )}
      <div className="reviews-container">
        <h3>Reviews</h3>
        {home.reviews && home.reviews.length > 0 ? (
          home.reviews.map((review, index) => (
            <div key={index}>
              <p>{review.review}</p>
            </div>
          ))
        ) : (
          <p>No reviews yet.</p>
        )}
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

export default HomeDetails;
