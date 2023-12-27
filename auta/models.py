from django.db import models
from django.utils import timezone
from django.contrib.auth.models import UserManager, AbstractBaseUser, PermissionsMixin
from django.core.validators import MaxValueValidator, MinValueValidator 

class CustomUserManager(UserManager):
    def _create_user(self, email, password, phone, full_name, **extra_fields):
        if not email:
            raise ValueError("Není vyplněn email")
        
        email = self.normalize_email(email)
        if self.model.objects.filter(email=email).exists():
            raise ValueError("Uživatel s tímto emailem již existuje")
        phone = phone.strip()
        full_name = full_name.strip()
        user = self.model(email=email, phone=phone, full_name=full_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_user(self, email=None, password=None, phone=None, full_name=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, phone, full_name, **extra_fields)
    def create_superuser(self, email=None, password=None, phone=None, full_name=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(email, password, phone, full_name, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    full_name = models.CharField(max_length=200)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(null=True, blank=True)
    
    objects = CustomUserManager()
    
    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['phone', 'full_name']
    
    def get_full_name(self):
        return self.full_name
    
    def get_short_name(self):
        return self.full_name.split(' ')[0]
    
    class Meta:
        verbose_name = 'Uživatel'
        verbose_name_plural = 'Uživatelé'
        db_table = 'customuser'

    def __str__(self):
        return f"Uživatel {self.full_name} s emailem {self.email}"

class Auto(models.Model):
    znacka = models.CharField(max_length = 50)
    model = models.CharField(max_length = 200)
    rok_vyroby = models.IntegerField(validators=[MinValueValidator(1880), MaxValueValidator(2050)])
    cena = models.IntegerField(validators=[MinValueValidator(0)])
    img = models.CharField(max_length = 200)
    def __str__(self):
        return f"Auto značky {self.znacka}, modelu {self.model}, z roku {self.rok_vyroby}"
    
    class Meta:
        verbose_name = 'Auto'
        verbose_name_plural = 'Auta'

class Rezervace(models.Model):
    auto = models.ForeignKey(Auto, on_delete=models.CASCADE)
    datum_a_cas = models.DateTimeField()
    def __str__(self):
        return f"Rezervace pro {self.auto} - {self.datum_a_cas}"
    
    class Meta:
        verbose_name = 'Rezervace'
        verbose_name_plural = 'Rezervace'
