from django.db import models


class Banner(models.Model):
    title = models.CharField(max_length=16, unique=True, verbose_name='名称')
    image = models.ImageField(upload_to='banner', verbose_name='图片')
    link = models.CharField(max_length=64, verbose_name='跳转链接')
    info = models.TextField(verbose_name='详情')
    is_show = models.BooleanField(default=1, verbose_name='是否展示')

    class Meta:
        db_table = 'banners'
        verbose_name_plural = '轮播图表'

    def __str__(self):
        return self.title
