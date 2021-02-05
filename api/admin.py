from django.contrib import admin
from .models import Domain, BreachedSite, Password, Account, BreachType, BreachSiteType

@admin.register(Domain)
class Domain(admin.ModelAdmin):
    list_display = ['domain', 'count']
    search_fields = ('domain',)

@admin.register(BreachedSite)
class Breached_Site(admin.ModelAdmin):
    list_display = ['domain', 'breach_type', 'account_breach_count']
    search_fields = ('domain',)


@admin.register(Password)
class Password(admin.ModelAdmin):
    list_display = ['hash', 'count']
    search_fields = ('hash',)

@admin.register(Account)
class Email(admin.ModelAdmin):
    list_display = ['email', 'domain','get_products' , 'count']
    search_fields = ('email',)

    def get_products(self, obj):
        return "\n".join([p.hash for p in obj.passwords.all()])

@admin.register(BreachType)
class BreachType(admin.ModelAdmin):
    list_display = ['type', 'count']
    search_fields = ('type',)

@admin.register(BreachSiteType)
class BreachSiteType(admin.ModelAdmin):
    list_display = ['type', 'count']
    search_fields = ('type',)