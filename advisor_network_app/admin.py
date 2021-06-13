from django.contrib import admin
from .models import Advisor, booking
# Register your models here.

@admin.register(Advisor)
class AdvisorAdmin(admin.ModelAdmin):
    list_display=("name",)