# from django.contrib import admin
# from .models import Regulator, IndustrySector, RegulationType, Technology, Regulation

# admin.site.site_header = "RegAccess Project Administration"
# admin.site.site_title = "RegAccess Project Admin Portal"
# admin.site.index_title = "Welcome to RegAccess Project Administration"

# class RegulatorAdmin(admin.ModelAdmin):
#     list_display = ('name', 'jurisdiction', 'address','phone_no', 'regulatory_scope', 'legal_documents')
#     list_filter = ('jurisdiction',)
#     search_fields = ('name', 'jurisdiction')
#     fieldsets = (
#         (None, {
#             'fields': ('name', 'jurisdiction', 'address','phone_no', 'regulatory_scope', 'legal_documents')
#         }),
#     )

#     def formfield_for_choice_field(self, db_field, request, **kwargs):
#         if db_field.name == 'jurisdiction':
#             kwargs['choices'] = Regulator.JURISDICTION_CHOICES
#         return super().formfield_for_choice_field(db_field, request, **kwargs)

# class IndustrySectorAdmin(admin.ModelAdmin):
#     list_display = ('name',)
#     search_fields = ('name',)

# class RegulationTypeAdmin(admin.ModelAdmin):
#     list_display = ('name', 'description')
#     search_fields = ('name', 'description')

# class TechnologyAdmin(admin.ModelAdmin):
#     list_display = ('name',)
#     search_fields = ('name',)

# class RegulationAdmin(admin.ModelAdmin):
#     list_display = ('title', 'industry_sector', 'regulation_type', 'technology', 'regulatorydetails', 'url', 'display_regulators','email')
#     list_filter = ('industry_sector', 'regulation_type', 'technology')
#     search_fields = ('title', 'description')
#     fieldsets = (
#         (None, {
#             'fields': ('title', 'description', 'regulators', 'industry_sector', 'regulation_type', 'technology', 'regulatorydetails', 'url','email')
#         }),
#     )
#     filter_horizontal = ('regulators',)  # Use filter_horizontal for a multi-select widget

#     def display_regulators(self, obj):
#         return ", ".join([regulator.name for regulator in obj.regulators.all()])
#     display_regulators.short_description = 'Regulators'

# admin.site.register(Regulator, RegulatorAdmin)
# admin.site.register(IndustrySector, IndustrySectorAdmin)
# admin.site.register(RegulationType, RegulationTypeAdmin)
# admin.site.register(Technology, TechnologyAdmin)
# admin.site.register(Regulation, RegulationAdmin)

from django.contrib import admin
from .models import Regulator, IndustrySector, RegulationType, Technology, Regulation
from tinymce.widgets import TinyMCE
from django import forms

admin.site.site_header = "RegAccess Project Administration"
admin.site.site_title = "RegAccess Project Admin Portal"
admin.site.index_title = "Welcome to RegAccess Project Administration"

class RegulationForm(forms.ModelForm):
    class Meta:
        model = Regulation
        fields = '__all__'
        widgets = {
            'description': TinyMCE(attrs={'cols': 80, 'rows': 30}),
        }

class RegulatorAdmin(admin.ModelAdmin):
    list_display = ('name', 'jurisdiction', 'address', 'phone_no', 'regulatory_scope', 'legal_documents')
    list_filter = ('jurisdiction',)
    search_fields = ('name', 'jurisdiction')
    fieldsets = (
        (None, {
            'fields': ('name', 'jurisdiction', 'address', 'phone_no', 'regulatory_scope', 'legal_documents')
        }),
    )

    def formfield_for_choice_field(self, db_field, request, **kwargs):
        if db_field.name == 'jurisdiction':
            kwargs['choices'] = Regulator.JURISDICTION_CHOICES
        return super().formfield_for_choice_field(db_field, request, **kwargs)

class IndustrySectorAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class RegulationTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description')

class TechnologyAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class RegulationAdmin(admin.ModelAdmin):
    form = RegulationForm  # Use the custom form with TinyMCE
    list_display = ('title', 'industry_sector', 'regulation_type', 'technology', 'regulatorydetails', 'url','email', 'display_regulators')
    list_filter = ('industry_sector', 'regulation_type', 'technology')
    search_fields = ('title', 'description')
    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'regulators', 'industry_sector', 'regulation_type', 'technology', 'regulatorydetails', 'url','email')
        }),
    )
    filter_horizontal = ('regulators',)  # Use filter_horizontal for a multi-select widget

    def display_regulators(self, obj):
        return ", ".join([regulator.name for regulator in obj.regulators.all()])
    display_regulators.short_description = 'Regulators'

admin.site.register(Regulator, RegulatorAdmin)
admin.site.register(IndustrySector, IndustrySectorAdmin)
admin.site.register(RegulationType, RegulationTypeAdmin)
admin.site.register(Technology, TechnologyAdmin)
admin.site.register(Regulation, RegulationAdmin)

