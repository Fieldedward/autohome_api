from django.contrib import admin
from .models import User
from django.utils.html import format_html


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    # 当前页面显示的字段
    list_display = ('id', 'username', 'is_superuser', 'mobile', 'real_user', 'is_locked', 'is_del', 'head_picture')

    # 增加自定义按钮
    actions = ['lock_button', 'unlock_button', 'close_account', 'restore_account']

    # 搜索字段
    search_fields = ['username']

    # 排序
    ordering = ['id', ]

    # 分页
    list_per_page = 4

    # Admin自定义返回列表
    def head_picture(self, models_obj):
        icon_url = "http://127.0.0.1:8000/media/" + str(models_obj.icon)
        return format_html('<img src="{}" height="80" width="80">', '{}'.format(icon_url))

    head_picture.short_description = '照片'

    def lock_button(self, request, queryset):
        user_obj = queryset.first()
        # print(user_obj, type(user_obj))
        User.objects.filter(username=user_obj.username).update(is_locked=1)

    lock_button.short_description = '锁定用户'
    lock_button.icon = 'fa fa-unlock'
    lock_button.type = 'info'
    lock_button.style = 'color:black;'
    lock_button.confirm = '你确定要锁定此用户'

    def unlock_button(self, request, queryset):
        user_obj = queryset.first()
        User.objects.filter(username=user_obj.username).update(is_locked=0)

    unlock_button.short_description = '解锁用户'
    unlock_button.icon = 'fa fa-key'
    unlock_button.type = 'success'
    unlock_button.style = 'color:black;'
    unlock_button.confirm = '你确定要解锁此用户'

    def close_account(self, request, queryset):
        user_obj = queryset.first()
        User.objects.filter(username=user_obj.username).update(is_del=1)

    close_account.short_description = '注销用户'
    close_account.icon = 'fa fa-times'
    close_account.type = 'info'
    close_account.style = 'color:black;'
    close_account.confirm = '你确定要注销此用户?'

    def restore_account(self, request, queryset):
        user_obj = queryset.first()
        User.objects.filter(username=user_obj.username).update(is_del=0)

    restore_account.short_description = '恢复用户'
    restore_account.icon = 'fa fa-check'
    restore_account.type = 'success'
    restore_account.style = 'color:black;'
    restore_account.confirm = '你确定要恢复此用户?'
