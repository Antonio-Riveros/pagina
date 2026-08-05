from django.contrib import admin
from .models import Message

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'email', 'fecha', 'leido')
    list_filter = ('leido', 'fecha')
    search_fields = ('nombre', 'email', 'mensaje')
    list_editable = ('leido',)
    readonly_fields = ('nombre', 'email', 'mensaje', 'fecha')

    def has_add_permission(self, request):
        return False
