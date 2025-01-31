from django.contrib import admin
from .models import FAQ
from django.utils.translation import gettext_lazy as _

class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'answer', 'get_translations', 'id', 'created_at', 'updated_at')
    search_fields = ('question',)
    list_filter = ('created_at', 'updated_at')
    
    fieldsets = (
        (None, {
            'fields': ('question', 'answer')
        }),
        (_('Translations'), {
            'fields': ('get_translations',)
        }),
    )
    
    def get_translations(self, obj):
        return ', '.join([
            f"{lang.upper()}: {obj.get_translated_question(lang)}" 
            for lang in ['hi', 'bn', 'sw', 'en']
        ])
    get_translations.short_description = _('Translations')

    formfield_overrides = {
        'answer': {'widget': admin.widgets.AdminTextareaWidget},
    }

admin.site.register(FAQ, FAQAdmin)

