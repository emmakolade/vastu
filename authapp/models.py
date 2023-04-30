from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission


class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('Owner must have an email address')
        if not username:
            raise ValueError('Owner must have a username')

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        create = self.create_user(email, username, password, **extra_fields)
        return create


class User(AbstractBaseUser, PermissionsMixin):
    full_name = models.CharField(max_length=300)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=30, unique=True)
    phone_number = models.CharField(max_length=20, blank=False)
    sex = models.CharField(max_length=50, blank=True)
    # otp = models.IntegerField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_property_owner = models.BooleanField(default=False)
    is_buyer = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name', 'username', 'phone_number']

    objects = UserManager()

    class Meta:
        verbose_name_plural = "Buyers and Property Owners"

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.full_name

    def get_short_name(self):
        return self.username


class OwnerUser(User):
    class Meta:
        verbose_name_plural = "Property Owners"


class BuyerUser(User):
    class Meta:
        verbose_name_plural = "Buyers"

# class OwnerUser(models.Model):
#     owner = models.OneToOneField(User, on_delete= models.CASCADE)
#     full_name = models.CharField(max_length=300)
#     email = models.EmailField(unique=True)
#     username = models.CharField(max_length=30, unique=True)
#     phone_number = models.CharField(max_length=20, blank=False)
#     sex = models.CharField(max_length=50, blank=True)
#     otp = models.IntegerField(blank=True, null=True)
#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['full_name', 'username', 'phone_number']

#     class Meta:
#         verbose_name_plural = "Property Owners"
# class BuyerUser(OwnerUser):
#     buyer = models.OneToOneField(User, on_delete= models.CASCADE)
#     class Meta:
#         verbose_name_plural = "Buyers"


# class BuyerUserManager(OwnerUserManager):
#     def create_user(self, email, username, password=None, **extra_fields):
#         if not email:
#             raise ValueError('Buyer must have an email address')
#         if not username:
#             raise ValueError('Buyer must have a username')

#         email = self.normalize_email(email)
#         buyer = self.model(email=email, username=username, **extra_fields)
#         buyer.set_password(password)
#         buyer.save()
#         return buyer

#     def create_superuser(self, email, username, password=None, **extra_fields):
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_superuser', True)
#         create = self.create_user(email, username, password, **extra_fields)
#         return create


# class BuyerUser(AbstractBaseUser, PermissionsMixin):
#     full_name = models.CharField(max_length=300)
#     email = models.EmailField(unique=True)
#     username = models.CharField(max_length=30, unique=True)
#     phone_number = models.CharField(max_length=20, blank=False)
#     sex = models.CharField(max_length=50, blank=True)
#     otp = models.IntegerField(blank=True, null=True)
#     is_active = models.BooleanField(default=False)
#     is_staff = models.BooleanField(default=False)
#     is_superuser = models.BooleanField(default=False)

#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['full_name', 'email', 'username', 'phone_number']

#     objects = BuyerUserManager()

#     groups = models.ManyToManyField(
#         Group,
#         verbose_name='groups',
#         blank=True,
#         related_name='buyer_group',
#         related_query_name='buyer',
#     )
#     user_permissions = models.ManyToManyField(
#         Permission,
#         verbose_name='user permissions',
#         blank=True,
#         related_name='buyer_group',
#         related_query_name='buyer',
#     )

#     class Meta:
#         verbose_name_plural = "Buyers"

#     def __str__(self):
#         return self.email

#     def get_full_name(self):
#         return self.full_name

#     def get_short_name(self):
#         return self.username
