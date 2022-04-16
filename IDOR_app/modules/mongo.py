import uuid
from flask import current_app


__author__ = "tycooper"


class User:
    """A user."""


    def __init__(self, _id, email, password):
        self._id = _id # Patched: uuid.uuid4().hex if id is None else id, above is user_id=None. This was done in routes to be more presented.
        self.email = email
        self.password = password


    def save_to_mongo(self):
        """Method to submit the object to the db"""
        return current_app.db.AccountsSavedPatch.insert_one(self.json())


    def json(self):
        """Creates a JSON representation of post itself"""

        return {
            '_id': self._id,
            'email': self.email,
            'password': self.password,
        }


    @classmethod
    def from_mongo_id(cls, _id):
        user_data = current_app.db.AccountsSavedPatch.find_one({'_id': _id})
        return cls(
            _id=user_data['_id'], 
            email=user_data['email'], 
            password=user_data['password'], 
            )


    @classmethod
    def from_mongo_email(cls, email):
        user_data = current_app.db.AccountsSavedPatch.find_one({'email': email})
        return cls(
            _id=user_data['_id'], 
            email=user_data['email'], 
            password=user_data['password'], 
            )
