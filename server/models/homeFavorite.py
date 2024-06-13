from . import SerializerMixin, validates, re, db
from models.home import Home
from models.favoritesCollection import FavoriteCollection

class HomeFavorite(db.Model, SerializerMixin):
    __tablename__ = 'home_favorites'

    favorite_collection_id = db.Column(db.Integer, db.ForeignKey('favorite_collections.id'), primary_key=True, index=True)
    home_id = db.Column(db.Integer, db.ForeignKey('homes.id'), primary_key=True, index=True)

    # Relationship
    favorite_collection = db.relationship('FavoriteCollection', back_populates='home_favorites')
    home = db.relationship('Home', back_populates='home_favorites')

    # Serialize
    serialize_rules = ('-favorite_collection.home_favorites', '-home.home_favorites',)

    # Representation
    def __repr__(self):
        return f""" 
            <HomeFavorite
                favorite_collection_id: {self.favorite_collection_id}
                home_id: {self.home_id}
                />
        """
    
    # Validations
    @validates("favorite_collection_id")
    def validate_favorite_collection_id(self, _, favorite_collection_id):
        if not isinstance(favorite_collection_id, int):
            raise TypeError("FavoriteCollection ids must be integers.")
        elif favorite_collection_id < 1:
            raise ValueError("FavoriteCollection id has to be a positive integer.")
        elif not db.session.get(FavoriteCollection, favorite_collection_id):
            raise ValueError("FavoriteCollection id has to correspond to an existing favorite collection.")
        return favorite_collection_id
    
    @validates("home_id")
    def validate_home_id(self, _, home_id):
        if not isinstance(home_id, int):
            raise TypeError("Home ids must be integers.")
        elif home_id < 1:
            raise ValueError("Home id has to be a positive integer.")
        elif not db.session.get(Home, home_id):
            raise ValueError("Home id has to correspond to an existing home.")
        return home_id
