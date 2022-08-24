from django.contrib import admin
from .models import Coupon

# Register your models here.


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    # 当前页面显示的字段
    list_display = ('id', 'user', 'coupon_one', 'coupon_two', 'coupon_three', 'is_generate')

    # 搜索字段
    search_fields = ['id', ]

    # 排序
    ordering = ['id', ]

    # 增加自定义按钮
    actions = ['reset_button', ]

    def reset_button(self, request, queryset):
        # 方案一
        obj = queryset.first()
        Coupon.objects.filter(id=obj.id).update(coupon_one=1, coupon_two=1, coupon_three=1, is_generate=0)
        # 方案二
        # queryset.delete()

    reset_button.short_description = '重置优惠'
    reset_button.icon = 'fa fa-undo'
    reset_button.type = 'info'
    reset_button.style = 'color:black;'
    reset_button.confirm = '重置优惠后，用户可以重新领取三张优惠券'
