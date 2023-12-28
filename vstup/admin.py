from django.contrib import admin

from .models import Entrant, University, Faculty, Department, Specialty, Onp, ForeignLanguage, EducationForm, FundingSource

#admin.site.register(Entrant)
@admin.register(Entrant)
class EntrantAdmin(admin.ModelAdmin):
    pass 

# admin.site.register(University)
@admin.register(University)
class UniversityAdmin(admin.ModelAdmin):
    pass 

#admin.site.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ('name', 'shortName') 
admin.site.register(Faculty, FacultyAdmin) 


# admin.site.register(Department)
@admin.register(Department)
class CathedraAdmin(admin.ModelAdmin):
    list_display = ('name', 'shortName', 'display_specialty') 


@admin.register(Specialty)
class SpecialtyAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'display_departments') 
    list_filter = ( 'code' , 'name' )


admin.site.register(Onp)
admin.site.register(ForeignLanguage)
admin.site.register(EducationForm)
admin.site.register(FundingSource)
