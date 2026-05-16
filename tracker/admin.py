from django.contrib import admin
from .models import Category, Transaction

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'icon', 'user')
    list_filter  = ('type', 'user')
    search_fields = ('name',)

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('note', 'type', 'amount', 'category', 'date', 'user')
    list_filter  = ('type', 'date', 'user')
    search_fields = ('note',)
    date_hierarchy = 'date'
