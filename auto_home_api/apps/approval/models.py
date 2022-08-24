from django.db import models

# Create your models here.


class CarPendingApproval(models.Model):
    car_type = (
        (0, '轿车'),
        (1, 'SUV'),
        (2, '跑车')
    )

    seats_choice = (
        (2, '两座'),
        (5, '五座'),
        (7, '七座')
    )

    second_car = (
        (0, "新车"),
        (1, "二手车"),
    )

    manual_trans = (
        (0, "手动档"),
        (1, "自动挡"),
    )

    energy_type = (
        (0, "新能源"),
        (1, "汽油"),
    )
    name = models.CharField(max_length=128, verbose_name="车辆名称")
    car_type = models.SmallIntegerField(choices=car_type, default=0, verbose_name="车辆类型")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='价格', default=0)
    seats_choice = models.SmallIntegerField(choices=seats_choice, default=0, verbose_name="车座数")
    energy_type = models.SmallIntegerField(choices=energy_type, default=0, verbose_name='能源类型')
    manual_trans = models.SmallIntegerField(choices=manual_trans, default=0, verbose_name="变速箱")
    second_car = models.SmallIntegerField(choices=second_car, default=1, verbose_name="是否二手")
    carFactory = models.SmallIntegerField(verbose_name="厂家编号")
    stock_num = models.IntegerField(default=1, verbose_name="库存数量")
    is_approval = models.BooleanField(default=0, verbose_name="是否已审核")

    # TODO:车辆详情
    car_detail_id = models.IntegerField(verbose_name="车辆详情id")
    emission_standard_choice = (
        (0, '无'),
        (1, '国四'),
        (2, '国五'),
        (3, '国六'),
        (4, '国六b'),

    )
    production_mode = (
        (0, '合资'),
        (1, '进口'),
        (2, '国产'),
    )

    car_detail = models.TextField(max_length=1024, null=True, verbose_name='车辆描述')
    # 排量
    displacement = models.CharField(max_length=8, null=True, verbose_name='排量')
    # 车辆颜色
    color = models.CharField(max_length=8, verbose_name='车辆颜色')
    # 国标
    emission_standard = models.SmallIntegerField(choices=emission_standard_choice, default=0, verbose_name="排放国标")
    # 里程
    mileage = models.CharField(max_length=16, verbose_name='车辆里程')
    # 生产方式
    production_mode = models.SmallIntegerField(choices=production_mode, default=0, verbose_name="生产方式")
    # 过户次数
    trans_num = models.IntegerField(default=0, verbose_name='过户次数')

    # TODO:经销商表
    distributor_id = models.IntegerField(verbose_name="经销商id")

    # TODO:图片链接
    img_list = models.CharField(max_length=512, verbose_name="图片链接列表")

    class Meta:
        db_table = "pending_approval_car"
        verbose_name = "待审核车表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name



