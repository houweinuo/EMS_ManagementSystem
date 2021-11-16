from django.contrib import admin

# Register your models here.
from user.models import Staff, User, DepartMent

admin.site.register(Staff)
admin.site.register(User)
admin.site.register(DepartMent)
