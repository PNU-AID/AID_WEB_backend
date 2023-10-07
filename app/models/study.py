from beanie import Document, Link

from . import User


class Study(Document):
    """User DB representation"""

    owner: Link[User]
    title: str
    content: str

    class Settings:
        name = "study"
