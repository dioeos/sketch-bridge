from pydantic import BaseModel, EmailStr


class UserSchemaBase(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str


class UserSchemaCreate(UserSchemaBase):
    """User Schema when client sends data to create user"""

    password: str


class UserSchema(UserSchemaBase):
    """User schema used for responses (no password)"""

    id: str

    class ConfigDict:
        from_attributes = True
