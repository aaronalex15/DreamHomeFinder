from . import SerializerMixin, validates, re, db

class Home(db.Model, SerializerMixin):
    __tablename__ = 'homes'

    id = db.Column(db.Integer, primary_key=True)
    attom_home_id = db.Column(db.Integer, nullable=False)
    address = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    state = db.Column(db.String(50), nullable=False)
    zip_code = db.Column(db.String(10), nullable=False)
    price = db.Column(db.Numeric, nullable=False)
    bedrooms = db.Column(db.Integer, nullable=False)
    bathrooms = db.Column(db.Integer, nullable=False)
    square_feet = db.Column(db.Integer, nullable=False)
    lot_size = db.Column(db.Integer, nullable=False)
    year_built = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(5000), nullable=False)
    crime_activity = db.Column(db.String(255), nullable=False)
    school_rating = db.Column(db.String(50), nullable=False)
    cover_photo = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    # Relationships
    home_favorites = db.relationship('HomeFavorite', back_populates='home', cascade="all, delete-orphan")
    reviews = db.relationship('Review', back_populates='home', cascade="all, delete-orphan")

    # Serialize
    serialize_rules = ('-reviews.home', '-home_favorites',)

    # Representation
    def __repr__(self):
        return f"""
            <Home {self.id}
                attom_home_id: {self.attom_home_id}
                address: {self.address}
                city: {self.city}
                state: {self.state}
                zip_code: {self.zip_code}
                price: {self.price}
                bedrooms: {self.bedrooms}
                bathrooms: {self.bathrooms}
                square_feet: {self.square_feet}
                lot_size: {self.lot_size}
                year_built: {self.year_built}
                />
        """

    # Validations
    @validates("address")
    def validate_address(self, _, address):
        if not isinstance(address, str):
            raise TypeError("Address must be a string.")
        elif not 2 <= len(address) <= 255:
            raise ValueError(f"Address must be between 2 and 255 characters.")
        return address
    
    @validates("city")
    def validate_city(self, _, city):
        if not isinstance(city, str):
            raise TypeError("City must be a string.")
        elif not 2 <= len(city) <= 50:
            raise ValueError(f"City must be between 2 and 50 characters.")
        return city
    
    @validates("state")
    def validate_state(self, _, state):
        if not isinstance(state, str):
            raise TypeError("State must be a string.")
        elif not 2 <= len(state) <= 50:
            raise ValueError(f"State must be between 2 and 50 characters.")
        return state
    
    @validates("zip_code")
    def validate_zip_code(self, _, zip_code):
        if not re.match(r'^\d{5}(?:[-\s]\d{4})?$', zip_code):
            raise ValueError("Zip code must be a valid US zip code.")
        return zip_code
    
    @validates("price")
    def validate_price(self, _, price):
        if not isinstance(price, (int, float, Decimal)):
            raise TypeError("Price must be a numeric value.")
        elif price <= 0:
            raise ValueError("Price must be a positive value.")
        return price
    
    @validates("bedrooms")
    def validate_bedrooms(self, _, bedrooms):
        if not isinstance(bedrooms, int):
            raise TypeError("Bedrooms must be an integer.")
        elif bedrooms < 0:
            raise ValueError("Bedrooms cannot be negative.")
        return bedrooms
    
    @validates("bathrooms")
    def validate_bathrooms(self, _, bathrooms):
        if not isinstance(bathrooms, int):
            raise TypeError("Bathrooms must be an integer.")
        elif bathrooms < 0:
            raise ValueError("Bathrooms cannot be negative.")
        return bathrooms
    
    @validates("square_feet")
    def validate_square_feet(self, _, square_feet):
        if not isinstance(square_feet, int):
            raise TypeError("Square feet must be an integer.")
        elif square_feet <= 0:
            raise ValueError("Square feet must be a positive value.")
        return square_feet
    
    @validates("lot_size")
    def validate_lot_size(self, _, lot_size):
        if not isinstance(lot_size, int):
            raise TypeError("Lot size must be an integer.")
        elif lot_size < 0:
            raise ValueError("Lot size cannot be negative.")
        return lot_size
    
    @validates("year_built")
    def validate_year_built(self, _, year_built):
        if not isinstance(year_built, int):
            raise TypeError("Year built must be an integer.")
        elif year_built < 0:
            raise ValueError("Year built cannot be negative.")
        return year_built

    @validates("description")
    def validate_description(self, _, description):
        if not isinstance(description, str):
            raise TypeError("Description must be a string.")
        elif not 2 <= len(description) <= 5000:
            raise ValueError(f"Description must be between 2 and 5000 characters.")
        return description

    @validates("crime_activity")
    def validate_crime_activity(self, _, crime_activity):
        if not isinstance(crime_activity, str):
            raise TypeError("Crime activity must be a string.")
        elif not 2 <= len(crime_activity) <= 255:
            raise ValueError(f"Crime activity must be between 2 and 255 characters.")
        return crime_activity

    @validates("school_rating")
    def validate_school_rating(self, _, school_rating):
        if not isinstance(school_rating, str):
            raise TypeError("School rating must be a string.")
        elif not 2 <= len(school_rating) <= 50:
            raise ValueError(f"School rating must be between 2 and 50 characters.")
        return school_rating
    
    @validates("cover_photo")
    def validate_cover_photo(self, _, cover_photo):
        required_prefix = "https://"
        if not cover_photo.startswith(required_prefix):
            raise ValueError(f"Cover photo URL must start with {required_prefix}.")
        return cover_photo
