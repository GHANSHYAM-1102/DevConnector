from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import PermissionsMixin


class UserManager(BaseUserManager):

    use_in_migrations = True

    def create_user(self, name, email, password=None, **extra_fields):
        """Creates a new user profile object"""

        if not email:
            raise ValueError('Users must have an email address')

        if not name:
            raise ValueError('Users must have a name')

        email = self.normalize_email(email)
        name = name.strip()
        user = self.model(name=name, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')

        return self.create_user('yash', email, password, **extra_fields)




class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    avatar = models.URLField(max_length=255, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email



class Profile(models.Model):
    user = models.OneToOneField('User', on_delete=models.CASCADE, related_name='profile', blank=True)
    company = models.CharField(max_length=256, blank=True)
    website = models.URLField(max_length=255, blank=True)
    location = models.CharField(max_length=255, blank=True)
    status = models.CharField(max_length=100,blank=True)
    skills = models.TextField(help_text="Comma Seperated value",blank=True)
    bio = models.TextField(blank=True)
    githubusername = models.CharField(max_length=50, blank=True)
    youtube = models.CharField(max_length=255, blank=True)
    twitter = models.CharField(max_length=255, blank=True)
    facebook = models.CharField(max_length=255, blank=True)
    linkedin = models.CharField(max_length=255, blank=True)
    instagram = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.user.name

class Experience(models.Model):
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE, related_name='experience', blank=True)
    title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    from_date = models.DateField()
    to_date = models.DateField(blank=True, null=True)
    current = models.BooleanField(default=False)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title

class Education(models.Model):
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE, related_name='education', blank=True)
    school = models.CharField(max_length=255)
    degree = models.CharField(max_length=255)
    field_of_study = models.CharField(max_length=255)
    from_date = models.DateField()
    to_date = models.DateField(blank=True, null=True)
    current = models.BooleanField(default=False)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.school

class Post(models.Model):
    user = models.ForeignKey('User',on_delete=models.CASCADE, blank=True, related_name='posts')
    text = models.CharField(max_length=255)
    name = models.CharField(max_length=255, blank=True)
    avatar = models.URLField(max_length=200, blank=True)
    likes = models.ManyToManyField('User', related_name="likes" , blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text

    class Meta:
        ordering = ('-date',)


class Comment(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name="user_comments", blank=True)
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name="post_comments", blank=True)
    text = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.text}-{self.user.name}"

    class Meta:
        ordering = ('-date',)

