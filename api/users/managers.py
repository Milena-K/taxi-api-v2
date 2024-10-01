from django.contrib.auth.base_user import (
    BaseUserManager,
)
from django.contrib.auth.hashers import (
    make_password,
)


class UserManager(
    BaseUserManager
):
    def create_user(
        self,
        username,
        password,
        profile_picture,
        **extra_fields,
    ):
        if not username:
            raise ValueError(
                "A username for the user must be set."
            )
        if not password:
            raise ValueError(
                "A password for the user must be set."
            )

        user = self.model(
            username=username,
            profile_picture=profile_picture,
        )
        # TODO: change user to be active only when phone number is confirmed
        extra_fields.setdefault(
            "is_active", True
        )
        user.set_password(
            password
        )
        user.save()
        return user

    def create_superuser(
        self,
        username,
        password,
        **extra_fields,
    ):
        """
        Create and save a SuperUser with the given email and password.
        """
        superuser = self.model(
            username=username,
        )
        superuser.is_staff = (
            True
        )
        superuser.is_superuser = True
        superuser.is_active = True

        # TODO: the superuser should have a work email for contact
        superuser.set_password(
            password
        )
        superuser.save(
            using=self._db
        )
        return superuser

    def get_queryset(self):
        return super().get_queryset()
