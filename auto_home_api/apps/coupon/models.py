from django.db import models
from user.models import User

# Create your models here.


"""
记录用户id，领取次数，只给三个用列表组织，每一次使用都自动选择最低折扣，用完一张就过期一张
"""


class Coupon(models.Model):
    """
    优惠券表,一旦使用,值改为1
    普通用户优惠折扣在0.88-1之间
    新用户固定为0.8
    """
    coupon_one = models.DecimalField(max_digits=3, decimal_places=2, verbose_name="优惠券一")
    coupon_two = models.DecimalField(max_digits=3, decimal_places=2, verbose_name="优惠券二")
    coupon_three = models.DecimalField(max_digits=3, decimal_places=2, verbose_name="优惠券三")
    new_user_coupon = models.DecimalField(max_digits=3, decimal_places=2, default=0.80, verbose_name="新用户优惠券")
    is_generate = models.BooleanField(default=0, verbose_name="是否领取过优惠券")
    # user_id = models.ForeignKey(to='User', on_delete=models.DO_NOTHING, verbose_name="用户")
    user_id = models.IntegerField(verbose_name="用户id")

    class Meta:
        db_table = 'auto_home_coupon'
        verbose_name = '优惠券表'
        verbose_name_plural = verbose_name

    @property
    def user(self,):
        obj = User.objects.filter(id=self.user_id).first()
        return obj.username

    def __str__(self):
        return self.user
