default_fieldsets = (
    (None, {
        'fields': ('number_service', )
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
        'fields': ('salary_amount', 'bic', 'bank_name', 'correspondent_account', 'checking_account', 'inn', 'kpp'),
    }),
    ('Увольнение', {
        'fields': ('status', 'dismissal_date', 'dismissal_order_number'),
        'description': 'Информация о статусе и увольнении'
    }),
)

create_fieldsets = (
    (None, {
        'fields': ('number_service',)
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
        'fields': ('salary_amount', 'bic', 'bank_name', 'correspondent_account', 'checking_account', 'inn', 'kpp'),
    }),
)
