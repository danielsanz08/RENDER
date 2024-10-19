from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model

class NameBackend(BaseBackend):
    def authenticate(self, request, name=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            # Usamos filter() y obtenemos el primer resultado con first()
            user = UserModel.objects.filter(name=name).first()
            if user is not None and user.check_password(password):
                return user
        except UserModel.DoesNotExist:
            return None
        return None

    def get_user(self, user_id):
        UserModel = get_user_model()
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None
