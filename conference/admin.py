from django.contrib import admin

from conference.models import Registration, paymentReceived, AmountReceived


class RegistrationAdmin(admin.ModelAdmin):
    search_fields = ["registration_number", "salutation", "first_name", "middle_name", "last_name", "position", "gender", "affiliation", "institution", "department", "address_1", "address_2", "city", "state", "zip", "country", "phone", "email", "bank", "branch", "check_number", "abstract", "comment"]
    list_filter = ["position"]
admin.site.register(Registration, RegistrationAdmin)

class paymentReceivedAdmin(admin.ModelAdmin):
    search_fields = ["payment_received", "comment"]
    list_filter = ["payment_received"]

admin.site.register(paymentReceived, paymentReceivedAdmin)

class AmountReceivedAdmin(admin.ModelAdmin):
    search_fields = ["registration__registration_number","registration__first_name","registration__last_name","registration__middle_name","registration__institution","registration__department","payment_received", "payment_type", "comment", "amount", "transcation_no"]
    list_filter = ["payment_received", "payment_type"]

admin.site.register( AmountReceived, AmountReceivedAdmin)
