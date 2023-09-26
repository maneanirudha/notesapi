from django.contrib import admin
from .models import Notes,Useractivation,Subscriptionplans,User_subscription_details
# Register your models here.


admin.site.register(Notes)
admin.site.register(Useractivation)
admin.site.register(Subscriptionplans)
admin.site.register(User_subscription_details)