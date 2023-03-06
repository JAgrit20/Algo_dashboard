

from django.contrib import admin
from .models import Positional_data,Vwap_Telegram_data

class RatingAdmin(admin.ModelAdmin):
    readonly_fields = ('date_time',)
admin.site.register(Positional_data,RatingAdmin)
admin.site.register(Vwap_Telegram_data,RatingAdmin)
# Register your models here.
