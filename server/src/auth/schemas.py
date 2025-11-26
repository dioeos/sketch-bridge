from pydantic import BaseModel, EmailStr


class UserSchemaBase(BaseModel):
    email: EmailStr | None = None
    first_name: str | None = None
    last_name: str | None = None


class UserSchemaCreate(UserSchemaBase):
    """User Schema when client sends data to create user"""

    password: str | None = None


class UserSchema(UserSchemaBase):
    """User schema used for responses (no password)"""

    id: str

    class ConfigDict:
        from_attributes = True
