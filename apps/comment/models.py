from django.db import models


class Comment(models.Model):
    user = models.ForeignKey('account.User', on_delete=models.PROTECT, verbose_name='用户')
    content = models.CharField(max_length=200, verbose_name='内容', null=False, blank=False)
    create_time = models.DateTimeField(verbose_name='时间', auto_now_add=True)

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user.username
