from marshmallow import Schema, fields, validates, ValidationError
from models import User
import re  # for email validation

class UserSchema(Schema):
    id = fields.Int(dump_only=True)  # Field to be serialized but not deserialized
    name = fields.Str(required=True)
    email = fields.Str(required=True)
    role = fields.Str(required=True)

    # Password should only be used during user creation (load_only=True)
    password = fields.Str(load_only=True, required=True)

    @validates('email')
    def validate_email(self, value):
        """Validate email format."""
        email_regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
        if not re.match(email_regex, value):
            raise ValidationError("Invalid email format.")
    
    @validates('role')
    def validate_role(self, value):
        """Ensure that the role is one of the accepted values."""
        if value not in ['admin', 'teamlead', 'teammember']:
            raise ValidationError('Role must be one of "admin", "teamlead", or "teammember"')

    def serialize(self, user):
        """Customize the serialization of a user object."""
        return {
            'id': user.id,
            'name': user.name,
            'email': user.email,
            'role': user.role
        }
