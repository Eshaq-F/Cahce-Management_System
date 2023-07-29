from django.contrib import admin
from api.models import Transaction, User


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'id', 'cache')
    search_fields = ('username', 'id')
    readonly_fields = ('cache',)


class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'type', 'amount', 'user')
    search_fields = ('id', 'category')
    list_filter = ('type',)


admin.site.register(Transaction, TransactionAdmin)
admin.site.register(User, UserAdmin)
