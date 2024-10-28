from extensions import ma
from models import User

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model=User
        exclude=["id"]
        include_fk = True