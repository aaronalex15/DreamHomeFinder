from . import SerializerMixin, validates, re, db

class Review(db.Model, SerializerMixin):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer)
    review = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    home_id = db.Column(db.Integer, db.ForeignKey('homes.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    # Relationship
    home = db.relationship('Home', back_populates='reviews')
    user = db.relationship('User', back_populates='reviews')

    # Serialize
    serialize_only = ('id', 'rating', 'review', 'home_id', 'user_id', 'user.username')

    # Representation
    def __repr__(self):
        return f""" 
            <Review {self.id}
                rating: {self.rating}
                review: {self.review}
                home_id: {self.home_id}
                user_id: {self.user_id}
                />
        """

    # Validations
    @validates("rating")
    def validate_rating(self, _, rating):
        if not isinstance(rating, int):
            raise TypeError("Rating must be an integer.")
        elif not 1 <= rating <= 5:
            raise ValueError("Rating must be between 1 (lowest) and 5 (highest).")
        return rating
    
    @validates("review")
    def validate_review(self, _, review):
        if not isinstance(review, str):
            raise TypeError("Review must be a string.")
        elif not 5 <= len(review) <= 5000:
            raise ValueError("Review must be between 5 and 5000 characters.")
        return review
        
    @validates("home_id")
    def validate_home_id(self, _, home_id):
        if not isinstance(home_id, int):
            raise TypeError("Home ids must be integers.")
        elif home_id < 1:
            raise ValueError(f"{home_id} has to be a positive integer.")
        from models.home import Home
        if not db.session.get(Home, home_id):
            raise ValueError(
                f"{home_id} has to correspond to an existing home."
            )
        return home_id
    
    @validates("user_id")
    def validate_user_id(self, _, user_id):
        if not isinstance(user_id, int):
            raise TypeError("User ids must be integers.")
        elif user_id < 1:
            raise ValueError(f"{user_id} has to be a positive integer.")
        from models.user import User
        if not db.session.get(User, user_id):
            raise ValueError(
                f"{user_id} has to correspond to an existing user."
            )
        return user_id
