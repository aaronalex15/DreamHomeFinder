from . import SerializerMixin, validates, re, db
from sqlalchemy.ext.hybrid import hybrid_property
from config import flask_bcrypt

class User(db.Model, SerializerMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    _password_hash = db.Column(db.String, nullable=False)
    profile_image = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    # Relationship
    favorite_collections = db.relationship(
        "FavoriteCollection", back_populates="user", cascade="all, delete-orphan"
    )
    reviews = db.relationship(
        "Review", back_populates="user", cascade="all, delete-orphan"
    )

    # Serialize
    serialize_rules = (
        "-favorite_collections.user",
        "-reviews.user",
    )

    # Representation
    def __repr__(self):
        return f""" 
            <User {self.id}
                username: {self.username}
                email: {self.email}
                />
        """

    # Validations
    @validates("username")
    def validate_username(self, _, username):
        if not isinstance(username, str):
            raise TypeError("Username must be a string.")
        elif not 3 <= len(username) <= 20:
            raise ValueError("Username must be between 3 and 20 characters.")
        return username

    @validates("email")
    def validate_email(self, _, email):
        if not isinstance(email, str):
            raise TypeError("Email must be a string.")
        elif not 5 <= len(email) <= 40:
            raise ValueError("Email must be between 5 and 40 characters.")
        email_regex = r"[^@]+@[^@]+\.[^@]+"
        if not re.match(email_regex, email):
            raise ValueError("Invalid email format.")
        return email

    @hybrid_property
    def password_hash(self):
        return self._password_hash

    @password_hash.setter
    def password_hash(self, password):
        if not isinstance(password, str):
            raise TypeError("Password must be a string.")
        elif not 8 <= len(password) <= 50:
            raise ValueError("Password must be between 8 and 50 characters.")
        self._password_hash = flask_bcrypt.generate_password_hash(password).decode('utf-8')
    
    def authenticate(self, password):
        return flask_bcrypt.check_password_hash(self._password_hash, password)
