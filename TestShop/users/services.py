from TestShop.users.models import User


class UserService:
    model = User

    @classmethod
    def save(cls, username: str, email: str, password):
        obj = cls.model(username=username, email=email, password=password)
        obj.save()
        