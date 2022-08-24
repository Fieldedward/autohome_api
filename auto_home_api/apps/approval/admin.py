from django.contrib import admin
from approval.models import CarPendingApproval
from cars.models import Car, CarDetail, CarsImg


# Register your models here.


@admin.register(CarPendingApproval)
class CarPendingApprovalAdmin(admin.ModelAdmin):
    # 当前页面显示的字段
    list_display = (
        'id', 'name', 'car_type', 'price', 'seats_choice', 'energy_type', 'stock_num', 'displacement', 'color',
        'emission_standard',
        'mileage', 'production_mode', 'trans_num', 'is_approval')

    # 按字段排序
    ordering = ('id',)

    # 增加审核按钮
    actions = ['approval_button', 'disapproval_button']

    # 搜索框
    search_fields = ('name',)

    # 分页
    list_per_page = 5

    # 可编辑字段
    list_editable = ('price',)

    def approval_button(self, request, queryset):
        obj = queryset.first()
        # 添加到车辆详情表
        car_detail_obj = CarDetail.objects.create(car_detail=obj.car_detail, displacement=obj.displacement,
                                                  color=obj.color,
                                                  emission_standard=obj.emission_standard, mileage=obj.mileage,
                                                  production_mode=obj.production_mode, trans_num=obj.trans_num)
        # 添加到车表
        # print(obj.name)
        Car.objects.create(name=obj.name, car_type=obj.car_type, price=obj.price, seats_choice=obj.seats_choice,
                           energy_type=obj.energy_type, stock_num=obj.stock_num, second_car=1,
                           carFactory_id=obj.carFactory, car_info_detail=car_detail_obj,
                           distributors_id=obj.distributor_id)
        # TODO:添加到车辆图片表
        CarPendingApproval.objects.filter(pk=obj.pk).update(is_approval=1)

    approval_button.short_description = '审核'
    approval_button.icon = 'fa fa-car'
    approval_button.type = 'danger'
    approval_button.style = 'color:black;'
    approval_button.confirm = '审核通过，将添加到车表，请再次确认您的操作'

    def disapproval_button(self, request, queryset):
        queryset.delete()

    disapproval_button.short_description = '退回'
    disapproval_button.icon = 'fa fa-trash'
    disapproval_button.type = 'danger'
    disapproval_button.style = 'color:black;'
    disapproval_button.confirm = '审核不通过，将添删除该条信息，请再次确认您的操作'
