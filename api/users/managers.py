from django.contrib.auth.base_user import BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, username, password, email, profile_picture, role, **kwargs):
        if not username:
            raise ValueError("A username for the user must be set.")
        if not password:
            raise ValueError("A password for the user must be set.")
        if not email:
            raise ValueError("An email for the user must be set.")
        if role not in ["C", "D"]:
            raise ValueError("A role for the user must be set as C (customer) or D (driver).")

        email = self.normalize_email()
        user = self.model(email=email, username=username, profile_picture=profile_picture, role=role)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        email = self.normalize_email()
        superuser = self.model(email=email, username=username)
        superuser.set_password(password)
        superuser.save()
        return superuser

    def get_queryset(self):
        return super().get_queryset()
