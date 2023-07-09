from django.contrib import admin
from client.models import Client , ClientComment ,ClientFile
# Register your models here.
admin.site.register(Client)
admin.site.register(ClientComment)
admin.site.register(ClientFile)