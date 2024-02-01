from django.contrib import admin
from .models import *
# Register your models here.
class ClinicAdmin(admin.ModelAdmin):
    pass
admin.site.register(Clinic, ClinicAdmin)

class CustomUserAdmin(admin.ModelAdmin):
    pass
admin.site.register(CustomUser, CustomUserAdmin)

class ReviewAdmin(admin.ModelAdmin):
    pass
admin.site.register(Review, ReviewAdmin)

class QueueingAdmin(admin.ModelAdmin):
    pass
admin.site.register(Queueing, QueueingAdmin)

class PaymentAdmin(admin.ModelAdmin):
    pass
admin.site.register(Payment, PaymentAdmin)