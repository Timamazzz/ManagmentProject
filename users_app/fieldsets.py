default_fieldsets = (
    (None, {
        'fields': ('number_service', 'rank')
    }),
    ('Личные данные', {
        'fields': ('first_name', 'last_name', 'patronymic', 'birthday'),
    }),
    ('Паспортные данные', {
        'fields': ('passport_series', 'passport_number', 'passport_issued', 'passport_issue_date'),
    }),
    ('Данные о контракте', {
        'fields': ('contract_date', 'order_number', 'enrollment_date'),
    }),
    ('Банковские реквизиты', {
        'fields': (
            'salary', 'salary_amount', 'bic', 'bank_name', 'correspondent_account', 'checking_account', 'inn', 'kpp'),
    }),
    ('Увольнение', {
        'fields': ('status', 'dismissal_date', 'dismissal_order_number'),
        'description': 'Информация о статусе и увольнении'
    }),
)

reserve_fieldsets = (
    (None, {
        'fields': ('number_service', 'status', 'rank')
    }),
    ('Личные данные', {
        'fields': ('first_name', 'last_name', 'patronymic', 'birthday'),
    }),
    ('Паспортные данные', {
        'fields': ('passport_series', 'passport_number', 'passport_issued', 'passport_issue_date'),
    }),
    ('Данные о контракте', {
        'fields': ('contract_date', 'order_number', 'enrollment_date'),
    }),
    ('Банковские реквизиты', {
        'fields': (
            'salary', 'salary_amount', 'bic', 'bank_name', 'correspondent_account', 'checking_account', 'inn', 'kpp'),
    }),

)

create_fieldsets = (
    (None, {
        'fields': ('number_service', 'rank')
    }),
    ('Личные данные', {
        'fields': ('first_name', 'last_name', 'patronymic', 'birthday'),
    }),
    ('Паспортные данные', {
        'fields': ('passport_series', 'passport_number', 'passport_issued', 'passport_issue_date'),
    }),
    ('Данные о контракте', {
        'fields': ('contract_date', 'order_number', 'enrollment_date'),
    }),
    ('Банковские реквизиты', {
        'fields': (
        'salary', 'salary_amount', 'bic', 'bank_name', 'correspondent_account', 'checking_account', 'inn', 'kpp'),
    }),
)

activity_report_create_fieldsets = (
    (None, {'fields': ('report_date', 'file')}),
)

activity_report_detail_fieldsets = (
    (None, {'fields': ('report_date', 'file', 'status')}),
)

activity_report_failed_detail_fieldsets = (
    (None, {'fields': ('report_date', 'file', 'status')}),
    ('Ошибка', {'fields': ('error_details',)}),
)

update_report_create_fieldsets = (
    (None, {'fields': ('file',)}),
)

update_report_detail_fieldsets = (
    (None, {'fields': ('file', 'status')}),
)

update_report_failed_detail_fieldsets = (
    (None, {'fields': ('file', 'status')}),
    ('Ошибка', {'fields': ('error_details',)}),
)
