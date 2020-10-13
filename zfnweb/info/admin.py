from django.contrib import admin
from info.models import Students,Teachers

admin.site.site_title="西院助手后台系统"

admin.site.site_header="西院助手后台管理"

admin.site.index_title="欢迎来到西院助手后台管理"

class StuAdmin(admin.ModelAdmin):
    ordering = ('-updateTime',)
    fieldsets = (
        ("基本信息", {'fields': ['studentId', 'name', 'gpa', 'classMonitor','national']}),
        ("院系班级", {'fields':['collegeName', 'majorName', 'className']}),
        ("额外信息", {'fields':['phoneNumber', 'birthDay', 'searchTimes','graduationSchool','domicile','email','idNumber']}),
        ("登录相关", {'fields':['updateTime', 'refreshTimes']}),
        ("Cookies", {'fields':['JSESSIONID', 'route']}),
    )
    list_display = ('studentId','name','national','collegeName','majorName','className','gpa','email','phoneNumber','birthDay','domicile','graduationSchool','refreshTimes','updateTime')
    search_fields = ('studentId','name','email','phoneNumber','birthDay','graduationSchool')
    list_filter = ('majorName','className','domicile')
    list_per_page = 20

class TeaAdmin(admin.ModelAdmin):
    fieldsets = (
        ("基本信息", {'fields': ['name', 'sex', 'collegeName', 'title']}),
        ("联系方式", {'fields':['phoneNumber', 'QQ', 'wechat']}),
    )
    list_display = ('name', 'sex', 'collegeName', 'title', 'phoneNumber', 'QQ', 'wechat')
    search_fields = ('name', 'collegeName', 'phoneNumber')
    list_filter = ('name', 'collegeName', 'phoneNumber')
    list_per_page = 20

admin.site.register(Students, StuAdmin)
admin.site.register(Teachers, TeaAdmin)