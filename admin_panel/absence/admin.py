from datetime import datetime
from django.contrib import admin
from django.db.models import Count, Q

from absence.models import Absence, Office, TelegramUser, TelegramUserAbsences

from django.contrib.admin import SimpleListFilter


class BaseDateFilter(SimpleListFilter):
    title = 'date'
    parameter_name = 'date'

    def lookups(self, request, model_admin):
        return [
            (date, date.strftime('%B %Y')) for date in Absence.objects.dates('date', 'month').all()
        ]

    def queryset(self, request, queryset):
        return queryset


class DateFilter(BaseDateFilter):
    title = 'date'
    parameter_name = 'date'

    def queryset(self, request, queryset):
        if date := self.value():
            cur_date = datetime.strptime(date, '%Y-%m-%d')
            return queryset.filter(date__year=cur_date.year, date__month=cur_date.month)

        return queryset


class AbsenceAdmin(admin.ModelAdmin):
    list_display = ('telegram_user_name', 'message', 'date')
    list_filter = ('telegram_user__name', DateFilter)

    def telegram_user_name(self, obj):
        return obj.telegram_user and obj.telegram_user.name

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


class AbsenceSummaryAdmin(admin.ModelAdmin):
    change_list_template = 'admin/absence_summary_change_list.html'
    list_filter = ('name', BaseDateFilter)

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(
            request,
            extra_context=extra_context,
        )
        try:
            qs = response.context_data['cl'].queryset
        except (AttributeError, KeyError):
            return response

        if date := request.GET.get('date'):
            cur_date = datetime.strptime(date, '%Y-%m-%d')
            qs = qs.annotate(
                total_absences=Count(
                    'absences',
                    filter=Q(
                        absences__date__year=cur_date.year, absences__date__month=cur_date.month
                    ),
                )
            )
        else:
            qs = qs.annotate(total_absences=Count('absences'))

        response.context_data['summary'] = list(qs)
        return response

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(Absence, AbsenceAdmin)
admin.site.register(TelegramUserAbsences, AbsenceSummaryAdmin)
admin.site.register(Office, OfficeAdmin)
admin.site.register(TelegramUser, TelegramUserAdmin)
