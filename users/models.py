from django.db import models

# Create your models here.
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractUser
#from phonenumber_field.modelfields import PhoneNumberField



class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)
        
        
class CustomUser(AbstractUser):
	username = None
	email = models.EmailField(_('email address'), unique=True)
	nom = models.CharField(max_length=25,null=False,default='.')
	prenom = models.CharField(max_length=25,null=False,default='.')
	adresse1 = models.CharField(max_length=40,null=False,default='.')
	adresse2 = models.CharField(max_length=40,null=True,default='.')
	codepostal = models.IntegerField(default = 0,null=False)
	ville = models.CharField(max_length=35,null=False,default='.')
	telephone = models.CharField(max_length=15,null=True,default='.')
	nbreinesmax = models.IntegerField(default = 10,null=False)

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = []

	objects = CustomUserManager()

	def __str__(self):
		return self.email
