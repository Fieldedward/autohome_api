from django.contrib import admin, messages
from .models import Car, CarDetail, CarsImg, CarFactory
from django.shortcuts import redirect
from django.utils.html import format_html


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    # 当前页面显示的字段
    list_display = ('id', 'name', 'car_type', 'price', 'seats_choice', 'energy_type', 'stock_num')

    # 按字段排序
    ordering = ('id',)

    # 可编辑字段
    list_editable = ('name',)

    # 分页
    list_per_page = 5

    # 增加自定义按钮
    actions = ['empty_stock_button', 'stockpiling_button']

    # 搜索字段
    search_fields = ['name']

    def empty_stock_button(self, request, queryset):
        obj = queryset.first()
        Car.objects.filter(id=obj.id).update(stock_num=0)
        messages.add_message(request, messages.INFO, '清空库存成功')

    empty_stock_button.short_description = '清空库存'
    empty_stock_button.icon = '	fa fa-minus'
    empty_stock_button.type = 'danger'
    empty_stock_button.style = 'color:black;'
    empty_stock_button.confirm = '点击会清空库存，请在此确认您的操作'

    def stockpiling_button(self, request, queryset):
        obj = queryset.first()
        old_stock_num = obj.stock_num
        old_stock_num += 5
        new_stock_num = old_stock_num
        Car.objects.filter(id=obj.id).update(stock_num=new_stock_num)
        messages.add_message(request, messages.SUCCESS, '增加库存成功')

    stockpiling_button.short_description = '增加库存'
    stockpiling_button.icon = 'fa fa-plus'
    stockpiling_button.type = 'success'
    stockpiling_button.style = 'color:black;'
    stockpiling_button.confirm = '点击会增加5库存，请在此确认您的操作'


@admin.register(CarDetail)
class CarDetailAdmin(admin.ModelAdmin):
    # 当前页面显示的字段
    list_display = ('id', 'car', 'displacement', 'color', 'emission_standard',
                    'mileage', 'production_mode', 'trans_num', 'popular')

    # 按字段排序
    ordering = ('id',)

    # 分页
    list_per_page = 5

    # 可编辑字段
    list_editable = ('trans_num',)

    # 搜索字段
    search_fields = ['color']

    # 增加控制人气按钮
    actions = ['empty_popular_button', 'increase_popular_button']

    def empty_popular_button(self, request, queryset):
        obj = queryset.first()
        CarDetail.objects.filter(id=obj.id).update(popular=0)

    empty_popular_button.short_description = '清空人气'
    empty_popular_button.icon = 'fa fa-trash'
    empty_popular_button.type = 'danger'
    empty_popular_button.style = 'color:black;'
    empty_popular_button.confirm = '发现商家有非法刷人气行为，点击清空车辆人气'

    def increase_popular_button(self, request, queryset):
        obj = queryset.first()
        old_popular = obj.popular
        old_popular += 10000
        new_popular = old_popular
        CarDetail.objects.filter(id=obj.id).update(popular=new_popular)

    increase_popular_button.short_description = '增加人气'
    increase_popular_button.icon = 'fa fa-star'
    increase_popular_button.type = 'success'
    increase_popular_button.style = 'color:black;'
    increase_popular_button.confirm = '点击会给车辆增加一万人气，此为商家付费服务，请确认操作车辆'


@admin.register(CarsImg)
class CarsImgAdmin(admin.ModelAdmin):
    # 当前页面显示的字段
    list_display = ('id', 'name', 'car_picture')

    # 增加自定义按钮
    actions = ['check_image_button', ]

    # 按字段排序
    ordering = ('id',)

    # 分页
    list_per_page = 2

    # 搜索字段
    search_fields = ['id']

    def check_image_button(self, request, queryset):
        obj = queryset.first()
        url = obj.img_url
        return redirect(url)

    check_image_button.short_description = '查看图片'
    check_image_button.icon = 'fa fa-play-circle'
    check_image_button.type = 'danger'
    check_image_button.style = 'color:black;'

    # Admin自定义返回列表
    def car_picture(self, models_obj):
        return format_html('<img src="{}" height="200" width="300">', '{}'.format(models_obj.img_url))

    car_picture.short_description = '车辆展示图'


@admin.register(CarFactory)
class CarFactoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'addr', 'tel')
    actions = ['']
    # actions = ['action_custom']
    # 按字段排序
    ordering = ('id',)

    # 可编辑字段
    list_editable = ('tel',)

    # 自定义按钮
    def action_custom(self, request, queryset):
        print("自定义按钮", request, queryset)
        messages.add_message(request, messages.SUCCESS, 'SUCCESS')
        messages.add_message(request, messages.ERROR, 'ERROR')
        messages.add_message(request, messages.DEBUG, 'DEBUG')
        messages.add_message(request, messages.WARNING, 'WARNING')
        messages.add_message(request, messages.INFO, 'INFO')

    action_custom.short_description = '自定义按钮'
    action_custom.icon = 'fas fa-audio-description'
    action_custom.type = 'Success'
    action_custom.enable = True
    action_custom.confirm = '你是否执意要点击这个按钮？'
    # action_demo.action_url = ''

    # 分页
    list_per_page = 5

    # 动态限制,返回显示的数据值
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(id__gte=1)

    # 判断,动态返回显示字段
    def get_list_display(self, request):
        if not request.user.is_superuser:
            res_list_display = ('id', 'name')
        else:
            res_list_display = self.list_display
        return res_list_display

    # 搜索字段
    list_filter = ('name', "addr")
    # list_filter_multiples = ('tel',)  # 搜索多选

    # 查询字段
    search_fields = ('name',)
    actions_on_top = True

    # 判断 动态限制返回的自定义按钮
    def get_actions(self, request):
        actions = super(CarFactoryAdmin, self).get_actions(request)
        if not request.user.is_superuser:
            # 删除,限制的自定义按钮
            if 'action_custom' in actions:
                del actions['action_custom']
        return actions
