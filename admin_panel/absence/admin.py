from django.contrib import admin

from absence.models import Absence, Office, TelegramUser


class AbsenceAdmin(admin.ModelAdmin):
    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class OfficeAdmin(admin.ModelAdmin):
    pass


class TelegramUserAdmin(admin.ModelAdmin):
    list_display = ('name', 'role_name', 'office_name', 'active')

    def office_name(self, obj):
        return obj.office and obj.office.name

    def role_name(self, obj):
        return obj.role and obj.role.name

    def has_add_permission(self, request, obj=None):
        return False


admin.site.register(Absence, AbsenceAdmin)
admin.site.register(Office, OfficeAdmin)
admin.site.register(TelegramUser, TelegramUserAdmin)
