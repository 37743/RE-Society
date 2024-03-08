from django.contrib import admin

from . import models

class WorkerAdmin(admin.ModelAdmin):
    list_display = ['full_name']
class SkillAdmin(admin.ModelAdmin):
    list_display = ['name']   
admin.site.register(models.Worker, WorkerAdmin)
admin.site.register(models.Skill, SkillAdmin)
