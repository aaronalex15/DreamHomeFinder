from . import SerializerMixin, validates, re, db
from sqlalchemy.ext.associationproxy import association_proxy

class FavoriteCollection(db.Model, SerializerMixin):
    __tablename__ = 'favorite_collections'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    # Relationship
    home_favorites = db.relationship('HomeFavorite', back_populates='favorite_collection', cascade="all, delete-orphan")
    user = db.relationship('User', back_populates='favorite_collections')

    # Serialize
    serialize_rules = ('-home_favorites.favorite_collection', '-user.favorite_collections',)

    # Association Proxy
    homes = association_proxy('home_favorites', 'home')

    # Representation
    def __repr__(self):
        return f""" 
            <FavoriteCollection {self.id}
                name: {self.name}
                user_id: {self.user_id}
                />
        """
    
    # Validations
    @validates("name")
    def validate_name(self, _, name):
        if not isinstance(name, str):
            raise TypeError("Name must be a string.")
        elif not 2 <= len(name) <= 50:
            raise ValueError("Name must be between 2 and 50 characters.")
        return name
    
    @validates("user_id")
    def validate_user_id(self, _, user_id):
        if not isinstance(user_id, int):
            raise TypeError("User ids must be integers.")
        elif user_id < 1:
            raise ValueError("User id has to be a positive integer.")
        from models.user import User
        if not db.session.get(User, user_id):
            raise ValueError("User id has to correspond to an existing user.")
        return user_id
