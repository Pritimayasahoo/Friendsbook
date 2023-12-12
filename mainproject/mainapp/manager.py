#use it for normalize email
import email.utils as email_utils
from django.contrib.auth.models import BaseUserManager

#use BaseUserManager to modify the default admin model
class CustomUserManager(BaseUserManager):
    #use the CustomUserManager during migration
    use_in_migrations=True


    """Create and save a User with the given email and password."""
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email must required')
        
        #normalize the mail
        parsed_email = email_utils.parseaddr(email)[1]
        normalized_email = parsed_email.lower()

        user = self.model(email=normalized_email, **extra_fields)
        #use set_password to encrypt password
        user.set_password(password)
        #save the created user in database
        user.save(using=self._db)
        return user


    """Create and save a SuperUser with the given email and password."""
    def create_superuser(self, email, password, **extra_fields):
        #For super_user set these fields as True
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        #Call the create_user here to create a user 
        return self.create_user(email, password, **extra_fields)