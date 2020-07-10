#
# # Register your models here.
#
# from django.contrib import admin
# from . import models
# import course.models
# import financial.models
#
#
# class UsersAdmin(admin.ModelAdmin):
#     list_display = ['openid','username','isActive', 'role','gender','domesticTelephone','foreignTelephone']
#     list_filter = ('role','isActive')
#     search_fields = ['username','domesticTelephone','foreignTelephone']
#     list_editable = ['isActive', 'role']
#
# class SchoolAdmin(admin.ModelAdmin):
#     list_display = ['s_name','market','func','qyfz']
#     list_filter = ('market','func')
#     search_fields = ['s_name','market','func','qyfz']
#     list_editable = ['market','func','qyfz']
#
# class Counselor(admin.ModelAdmin):
#     list_display = ['counselor','telephone']
#     list_editable = ['telephone']
#
# class Assistant(admin.ModelAdmin):
#     list_display = ['ast_name','password']
#
# #-----------------------------course-------------------------------
#
#
# class Course(admin.ModelAdmin):
#     list_display = ['course','category']
#     list_editable = ['category']
#
# class State(admin.ModelAdmin):
#     list_display = ['course','users','state']
#     list_editable = ['users','state']
#
# class Tuition(admin.ModelAdmin):
#     list_display = ['count','application_fee','course_fee','total_cost']
#     list_editable = ['application_fee','course_fee','total_cost']
#
#
# #-----------------------------financial-------------------------------
#
#
# class Ambassador_annual(admin.ModelAdmin):
#     list_display = ['id','floor','ceiling','annual_bonus','discount']
#     list_editable = ['floor','ceiling','annual_bonus','discount']
#
# class Base_commission(admin.ModelAdmin):
#     list_display = ['month','application_fee','month_target','month_complete','month_unfinished','quarter_target','quarter_complete']
#     list_editable = ['application_fee','month_target','month_complete','month_unfinished','quarter_target','quarter_complete']
#
# class Head_salary(admin.ModelAdmin):
#     list_display = ['level','base_salary','commission']
#     list_editable = ['base_salary','commission']
#
# class Market(admin.ModelAdmin):
#     list_display = ['type','low','middle','high']
#     list_editable = ['low','middle','high']
#
# class Head_annual(admin.ModelAdmin):
#     list_display = ['market','floor','ceiling','Annual_bonus']
#     list_editable = ['floor','ceiling','Annual_bonus']
#
# class Salary(admin.ModelAdmin):
#     list_display = ['ds_name','month','base_salary','apply_commission','supplement_commission','all_commission','quarter_commission','ds_year_commission','fz_year_commission','discount','underling_commission','deduct','task']
#
#
#
#
#
#
#
#
#
#
#
# admin.site.register(models.Users, UsersAdmin)
# admin.site.register(models.School, SchoolAdmin)
# admin.site.register(models.Counselor, Counselor)
# admin.site.register(models.Assistant, Assistant)
#
#
#
#
# admin.site.register(course.models.Course, Course)
# admin.site.register(course.models.State, State)
# admin.site.register(course.models.Tuition, Tuition)
#
#
#
# admin.site.register(financial.models.Ambassador_annual, Ambassador_annual)
# admin.site.register(financial.models.Base_commission, Base_commission)
# admin.site.register(financial.models.Head_salary, Head_salary)
# admin.site.register(financial.models.Market, Market)
# admin.site.register(financial.models.Head_annual, Head_annual)
# admin.site.register(financial.models.Salary, Salary)
