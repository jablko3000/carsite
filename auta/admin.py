from django.contrib import admin

from .models import Auto, Rezervace, CustomUser, Image, Note

# Register your models here.

admin.site.site_header = 'Administrace aut'
admin.site.register(Auto)
admin.site.register(Rezervace)
admin.site.register(CustomUser)
admin.site.register(Image)
admin.site.register(Note)