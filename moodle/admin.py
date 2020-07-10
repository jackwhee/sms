from django.contrib import admin
from moodle import models
from django.contrib.admin.models import LogEntry
# from pypinyin import lazy_pinyin

# Register your models here.

@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    list_display = ['object_repr','object_id','action_flag','user','change_message','action_time']
    search_fields = ['object_repr','change_message','object_id']
    list_filter = ['action_flag','user']


class MoodleUserAdmin(admin.ModelAdmin):
    list_display = ['m_ac', 'nick','role']
    list_filter = ['role']
    search_fields = ['m_ac','nick']
    ordering = ['role']
    # raw_id_fields = ('users',)
    # autocomplete_fields = ('users',)

    def formfield_for_foreignkey(self, db_field, request, *args, **kwargs):
        if db_field.name == 'users':
            # obj_id = request.resolver_match.args[0]  # 这里获取当前对象id，非常重要
            # sorted(models.Users.objects.filter(isActive='true'), key=lambda ch: lazy_pinyin(ch))
            kwargs['queryset'] = models.Users.objects.filter(isActive='true').order_by('username')  # 添加过滤条件
            # kwargs['queryset'] = sorted(models.Users.objects.filter(isActive='true'), key=lambda ch: lazy_pinyin(ch))  # 添加过滤条件
        return super(MoodleUserAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(models.MoodleUser,MoodleUserAdmin)


class MoodleExamAdmin(admin.ModelAdmin):
    list_display = ['exam_name', 'moodle_course','moodle_user','exam_type']
    ordering = ['moodle_user']
    search_fields = ['moodle_course__c_name', 'moodle_user__nick']
    list_filter = ['exam_type']
    list_editable = ['exam_type']
    # raw_id_fields = ('moodle_user', )
    # autocomplete_fields = ('moodle_user', )

    def formfield_for_foreignkey(self, db_field, request, *args, **kwargs):
        if db_field.name == 'moodle_user':
            kwargs['queryset'] = models.MoodleUser.objects.filter(role='prof').order_by('nick')  # 添加过滤条件


        return super(MoodleExamAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(models.MoodleExam,MoodleExamAdmin)


class MoodleExamStuAdmin(admin.ModelAdmin):
    list_display = ['exam_name', 'moodle_course','moodle_user']
    ordering = ['moodle_user']
    search_fields = ['moodle_course__c_name','moodle_user__nick']
    autocomplete_fields = ('moodle_course', 'moodle_user')

admin.site.register(models.MoodleExamStu,MoodleExamStuAdmin)

class LinshiAdmin(admin.ModelAdmin):
    list_display = ['exam_name', 'moodle_course','moodle_user']
    ordering = ['moodle_user']
    search_fields = ['moodle_course__c_name','moodle_user__nick']
    autocomplete_fields = ('moodle_course', 'moodle_user')

admin.site.register(models.Linshi,LinshiAdmin)


class MoodleActiveAdmin(admin.ModelAdmin):
    list_display = ['title']
admin.site.register(models.MoodleActive,MoodleActiveAdmin)


class MoodleNoticeAdmin(admin.ModelAdmin):
    list_display = ['info']
admin.site.register(models.MoodleNotice,MoodleNoticeAdmin)


class MoodleSubjectAdmin(admin.ModelAdmin):
    list_display = ['s_name']
admin.site.register(models.MoodleSubject,MoodleSubjectAdmin)


class MoodleCourseInline(admin.TabularInline): # TabularInline
  # extra = 1
  model = models.MoodleVideo
  # fieldsets = ['v_name','video_add']

class MoodleCourseAdmin(admin.ModelAdmin):
    list_display = ['c_name','subject','is_hot']
    # list_display = ['c_name','subject','is_hot','m_video']
    list_filter = ['subject__s_name','is_hot']
    search_fields = ['c_name']
    list_editable = ['is_hot']
    ordering = ['subject__s_name','c_name']
    inlines = [MoodleCourseInline,]

    # def m_video(self,obj):
    #     return obj.m_video.all()

admin.site.register(models.MoodleCourse,MoodleCourseAdmin)


class MoodleCUSAdmin(admin.ModelAdmin):
    list_display = ['moodle_user','moodle_course','is_teach']
    list_filter = ['is_teach']
    search_fields = ['moodle_user__nick','moodle_course__c_name']
    ordering = ['moodle_user','moodle_course__c_name']
    # raw_id_fields = ('moodle_course','moodle_user')
    autocomplete_fields = ('moodle_course','moodle_user')

    def formfield_for_foreignkey(self, db_field, request, *args, **kwargs):
        if db_field.name == 'moodle_user':
            # obj_id = request.resolver_match.args[0]  # 这里获取当前对象id，非常重要
            kwargs['queryset'] = models.MoodleUser.objects.order_by('role') # 添加过滤条件
        return super(MoodleCUSAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
admin.site.register(models.MoodleCUS,MoodleCUSAdmin)


class MoodleVideoAdmin(admin.ModelAdmin):
    list_display = ['v_name','moodle_course']
    list_filter = ['moodle_course__subject__s_name']
    search_fields = ['moodle_course__c_name']
    ordering = ['moodle_course','v_name']
    # raw_id_fields = ('moodle_course')
    autocomplete_fields = ('moodle_course',)
admin.site.register(models.MoodleVideo,MoodleVideoAdmin)


class MoodleCoursewareAdmin(admin.ModelAdmin):
    list_display = ['cs_name','moodle_course']
    list_filter = ['moodle_course__subject__s_name']
    search_fields = ['moodle_course__c_name']
    ordering = ['moodle_course']
    # raw_id_fields = ('moodle_course')
    autocomplete_fields = ('moodle_course',)
admin.site.register(models.MoodleCourseware,MoodleCoursewareAdmin)

admin.site.site_title = "Moodle数据后台"
admin.site.site_header = "Moodle数据后台"







