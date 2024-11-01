from django.contrib import admin
from catalog.models import Project, Company, secUser, UserSign, Profile, UserTools, SecUserApprove
from catalog.models import UserRequest, UserRequestApprove, UserRequestTypeMaster, UserRequestApproveMaster
from catalog.models import CodeB, UserCode, UserRetire, UserRetireApprove


admin.site.register(Company)

@admin.register(UserCode)
class UserCode(admin.ModelAdmin):
    list_display = ('code','name', 'manager','desc', 'status')


@admin.register(Project)
class Project(admin.ModelAdmin):
    list_display = ('name','owner', 'manager','yn')


@admin.register(CodeB)
class CodeB(admin.ModelAdmin):
    list_display = ('code','title')


@admin.register(UserRetireApprove)
class UserRetireApprove(admin.ModelAdmin):
    list_display = ('retiree','seq','app_user','approved')


@admin.register(UserSign)
class UserSign(admin.ModelAdmin):
    list_display = ('loginuser', 'doc_type', 'signdate')


class SecUserApproveInline(admin.StackedInline):
    model = SecUserApprove
    extra = 2


@admin.register(secUser)
class secUser(admin.ModelAdmin):
    inlines = (SecUserApproveInline,)
    list_display = ('id','userid','lastname','firstname','Company', 'project','admin_request_user', 'req_user','status')


class UserToolsInline(admin.StackedInline):
    model = UserTools
    extra = 2

@admin.register(Profile)
class Profile(admin.ModelAdmin):
    inlines = (UserToolsInline,)
    list_display = ('kor_name', 'company', 'project', 'status')

@admin.register(UserRetire)
class UserRetire(admin.ModelAdmin):
    list_display = ('code', 'retiree', 'manager')


class UserRequestApproveInline(admin.StackedInline):
    model = UserRequestApprove
    extra = 2


@admin.register(UserRequest)
class UserRequest(admin.ModelAdmin):
    inlines = (UserRequestApproveInline,)
    list_display = ('id', 'req_user', 'type', 'status')


class UserRequestApproveMasterInline(admin.StackedInline):
    model = UserRequestApproveMaster
    extra = 2


@admin.register(UserRequestTypeMaster)
class UserRequestTypeMaster(admin.ModelAdmin):
    inlines = (UserRequestApproveMasterInline,)
    list_display = ('type_name','type', 'type_desc', 'status')


