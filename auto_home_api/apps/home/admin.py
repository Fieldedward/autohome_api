from django.contrib import admin, messages
from home.models import Banner
from django.utils.html import format_html

# Register your models here.

admin.site.site_header = '汽车之家'
admin.site.site_title = '汽车之家后台管理'
admin.site.index_title = '欢迎使用汽车之家后台管理'


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    # 当前页面显示的字段
    list_display = ('id', 'title', 'banner', 'link', 'info', 'is_show')

    # 按字段排序
    ordering = ('id',)

    # 可编辑字段
    list_editable = ('link',)

    # 分页
    list_per_page = 3

    def banner(self, models_obj):
        icon_url = "http://127.0.0.1:8000/media/" + str(models_obj.image)
        return format_html('<img src="{}" height="150" width="300">', '{}'.format(icon_url))

    # 增加自定义按钮
    actions = ['display_picture_button', 'unshelve_picture_button']

    def display_picture_button(self, request, queryset):
        obj = queryset.first()
        Banner.objects.filter(id=obj.id).update(is_show=1)
        messages.add_message(request, messages.INFO, '此图将在轮播图中展示')

    display_picture_button.short_description = '展示'
    display_picture_button.icon = 'fa fa-check'
    display_picture_button.type = 'success'
    display_picture_button.style = 'color:black;'

    def unshelve_picture_button(self, request, queryset):
        obj = queryset.first()
        Banner.objects.filter(id=obj.id).update(is_show=0)
        messages.add_message(request, messages.INFO, '此图将不在轮播图中展示')

    unshelve_picture_button.short_description = '下架'
    unshelve_picture_button.icon = 'fa fa-minus'
    unshelve_picture_button.type = 'danger'
    unshelve_picture_button.style = 'color:black;'

    # 搜索字段
    search_fields = ['title']
