from . import SerializerMixin, validates, re, db

class Home(db.Model, SerializerMixin):
    __tablename__ = "homes"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    home_type = db.Column(db.String, nullable=False)
    max_guests = db.Column(db.Integer, nullable=False)
    total_occupancy = db.Column(db.Integer)
    total_bedrooms = db.Column(db.Integer)
    total_bathrooms = db.Column(db.Integer)
    location = db.Column(db.String)
    amenities = db.Column(db.String)
    price_per_night = db.Column(db.Float)
    image = db.Column(db.String)
    host_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    # Relationship
    host = db.relationship("User", back_populates="homes")
    reviews = db.relationship("Review", back_populates="home", cascade="all, delete-orphan")
    home_favorites = db.relationship("HomeFavorite", back_populates="home", cascade="all, delete-orphan")

    # Serialize
    serialize_only = (
        "id",
        "title",
        "description",
        "home_type",
        "max_guests",
        "total_occupancy",
        "total_bedrooms",
        "total_bathrooms",
        "location",
        "amenities",
        "price_per_night",
        "image",
        "host_id",
        "reviews.rating",
    )

    # Representation
    def __repr__(self):
        return f""" 
            <Home {self.id}
                title: {self.title}
                description: {self.description}
                home_type: {self.home_type}
                max_guests: {self.max_guests}
                total_occupancy: {self.total_occupancy}
                total_bedrooms: {self.total_bedrooms}
                total_bathrooms: {self.total_bathrooms}
                location: {self.location}
                amenities: {self.amenities}
                price_per_night: {self.price_per_night}
                image: {self.image}
                host_id: {self.host_id}
                />
        """

    # Validations
    @validates("title")
    def validate_title(self, _, title):
        if not isinstance(title, str):
            raise TypeError("Title must be a string.")
        elif not 5 <= len(title) <= 50:
            raise ValueError("Title must be between 5 and 50 characters.")
        return title
    
    @validates("description")
    def validate_description(self, _, description):
        if not isinstance(description, str):
            raise TypeError("Description must be a string.")
        elif not 10 <= len(description) <= 500:
            raise ValueError("Description must be between 10 and 500 characters.")
        return description

    @validates("home_type")
    def validate_home_type(self, _, home_type):
        if not isinstance(home_type, str):
            raise TypeError("Home type must be a string.")
        elif home_type not in {"house", "apartment", "condo", "cabin"}:
            raise ValueError("Invalid home type.")
        return home_type
    
    @validates("max_guests")
    def validate_max_guests(self, _, max_guests):
        if not isinstance(max_guests, int):
            raise TypeError("Max guests must be an integer.")
        elif max_guests <= 0:
            raise ValueError("Max guests must be a positive integer.")
        return max_guests
    
    @validates("price_per_night")
    def validate_price_per_night(self, _, price_per_night):
        if not isinstance(price_per_night, float):
            raise TypeError("Price per night must be a float.")
        elif price_per_night <= 0:
            raise ValueError("Price per night must be a positive number.")
        return price_per_night
    
    @validates("host_id")
    def validate_host_id(self, _, host_id):
        if not isinstance(host_id, int):
            raise TypeError("Host ids must be integers.")
        elif host_id < 1:
            raise ValueError("Host id has to be a positive integer.")
        from models.user import User
        if not db.session.get(User, host_id):
            raise ValueError("Host id has to correspond to an existing user.")
        return host_id
