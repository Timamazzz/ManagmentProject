from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users_app.fieldsets import default_fieldsets, create_fieldsets, reserve_fieldsets, \
    activity_report_create_fieldsets, activity_report_failed_detail_fieldsets, activity_report_detail_fieldsets, \
    update_report_detail_fieldsets, update_report_create_fieldsets, update_report_failed_detail_fieldsets
from users_app.models import User, Volunteer, Remark, VolunteerItem, Item, Report, ActivityReport, UpdateReport, \
    SalaryReport, Combat
from users_app.utils import export_to_excel, export_volunteers_and_items_to_excel


class RemarkInline(admin.TabularInline):
    model = Remark
    extra = 1
    can_delete = True

    def has_add_permission(self, request, obj=None):
        """Запрещает добавлять нарекания, если доброволец уволен"""
        return obj and obj.status == 'active' if obj else False

    def has_change_permission(self, request, obj=None):
        """Запрещает редактирование нареканий у уволенных"""
        return obj and obj.status == 'active' if obj else False


class VolunteerItemInline(admin.TabularInline):
    model = VolunteerItem
    extra = 1
    can_delete = True

    def has_add_permission(self, request, obj=None):
        """Запрещает добавлять нарекания, если доброволец уволен"""
        return obj and obj.status == 'active' if obj else False

    def has_change_permission(self, request, obj=None):
        """Запрещает редактирование нареканий у уволенных"""
        return obj and obj.status == 'active' if obj else False


class CombatInline(admin.TabularInline):
    model = Combat
    extra = 0
    ordering = ("-date",)
    fields = ("date", "amount")
    show_change_link = True


@admin.register(User)
class MyUserAdmin(UserAdmin):
    pass


@admin.register(Volunteer)
class VolunteerAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "number_service",
        "status",
        "last_name",
        "first_name",
        "patronymic",
        "birthday",
        "passport_series",
        "passport_number",
        "passport_issued",
        "passport_issue_date",
        "contract_date",
        "order_number",
        "enrollment_date",
        "salary_amount",
        "bic",
        "bank_name",
        "correspondent_account",
        "checking_account",
        "inn",
        "kpp",
    )
    list_filter = ("status", "contract_date", "enrollment_date", "dismissal_date")
    search_fields = ("last_name", "first_name", "patronymic", "number_service")
    inlines = (RemarkInline, VolunteerItemInline)
    fieldsets = default_fieldsets

    def get_inline_instances(self, request, obj=None):
        """Возвращает инлайны, но скрывает нарекания, если доброволец уволен"""
        if obj and (obj.status == 'dismissed' or obj.status == 'reserve'):
            return []
        # if request.user.has_perm("users_app.can_manage_reserve"):
        #     return [inline for inline in super().get_inline_instances(request, obj) if
        #             not isinstance(inline, RemarkInline)]

        return super().get_inline_instances(request, obj)

    def get_fieldsets(self, request, obj=None):
        """Изменяет отображение полей в зависимости от статуса"""
        fieldsets = list(super().get_fieldsets(request, obj))
        if not obj:
            return create_fieldsets

        if obj.status == 'dismissed':
            fieldsets = [fs for fs in fieldsets if 'performance_report' not in fs[1].get('fields', [])]

        if request.user.has_perm("users_app.can_manage_reserve") and not request.user.is_superuser:
            return reserve_fieldsets

        return tuple(fieldsets)

    def save_model(self, request, obj, form, change):
        """Валидация перед сохранением"""
        if not change and request.user.has_perm("users_app.can_manage_reserve"):
            obj.status = "reserve"

        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        """Фильтрует список в зависимости от прав пользователя"""
        qs = super().get_queryset(request)

        if request.user.is_superuser:
            return qs

        if request.user.has_perm("users_app.can_manage_reserve"):
            return qs.filter(status="reserve")

        return qs.none()

    def get_readonly_fields(self, request, obj=None):
        """Делает статус только для чтения, если пользователь не суперюзер"""
        if request.user.is_superuser:
            return []

        if request.user.has_perm("users_app.can_manage_reserve"):
            return ["status"]

        return []

    # --- Функция экспорта в Excel ---
    def export_active_volunteers(self, request, queryset):
        return export_to_excel(queryset.filter(status='active'), "active_volunteers.xlsx")

    def export_dismissed_volunteers(self, request, queryset):
        return export_to_excel(queryset.filter(status='dismissed'), "dismissed_volunteers.xlsx")

    def export_volunteers_and_items(self, request, queryset):
        return export_volunteers_and_items_to_excel(queryset, "volunteers_and_items.xlsx")

    export_active_volunteers.short_description = "Выгрузить выбранных действующих в Excel"
    export_dismissed_volunteers.short_description = "Выгрузить выбранных уволенных в Excel"
    export_volunteers_and_items.short_description = "Выгрузить добровольцев и их предметы в Excel"

    actions = [export_active_volunteers, export_dismissed_volunteers, export_volunteers_and_items]


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)
    list_filter = ('name',)


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('start_date', 'end_date', 'created_at', 'file')
    readonly_fields = ('created_at', 'file')
    ordering = ('-created_at',)

    def has_change_permission(self, request, obj=None):
        """Отключаем возможность редактирования отчета после создания"""
        if obj:
            return False
        return super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        """Оставляем возможность удаления"""
        return True


@admin.register(ActivityReport)
class ActivityReportAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'report_date', 'file', 'status')
    readonly_fields = ('created_at', 'status', 'error_details')
    ordering = ('-created_at',)
    fieldsets = activity_report_detail_fieldsets

    def has_change_permission(self, request, obj=None):
        return False

    def get_fieldsets(self, request, obj=None):
        fieldsets = list(super().get_fieldsets(request, obj))
        if not obj:
            return activity_report_create_fieldsets

        if obj.status == 'failed':
            fieldsets = activity_report_failed_detail_fieldsets

        return tuple(fieldsets)


@admin.register(UpdateReport)
class UpdateReportAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'file', 'status')
    readonly_fields = ('created_at', 'status', 'error_details')
    ordering = ('-created_at',)
    fieldsets = update_report_detail_fieldsets

    def has_change_permission(self, request, obj=None):
        return False

    def get_fieldsets(self, request, obj=None):
        fieldsets = list(super().get_fieldsets(request, obj))
        if not obj:
            return update_report_create_fieldsets

        if obj.status == 'failed':
            fieldsets = update_report_failed_detail_fieldsets

        return tuple(fieldsets)


@admin.register(SalaryReport)
class SalaryReportAdmin(admin.ModelAdmin):
    list_display = ("start_date", "end_date", "created_at", "file")
    readonly_fields = ("created_at", "file")
    ordering = ("-created_at",)
    inlines = [CombatInline]

    def has_change_permission(self, request, obj=None):
        """Отключаем возможность редактирования отчета после создания"""
        if obj:
            return False
        return super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        """Оставляем возможность удаления"""
        return True


@admin.register(Combat)
class CombatAdmin(admin.ModelAdmin):
    list_display = ("volunteer", "date", "amount")
    list_filter = ("date",)
    search_fields = ("volunteer__last_name", "volunteer__first_name", "volunteer__number_service")
    ordering = ("-date",)
