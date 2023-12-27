from django.contrib import admin

from .models import Auto, Rezervace, CustomUser

# Register your models here.


admin.site.register(Auto)
admin.site.register(Rezervace)
admin.site.register(CustomUser)