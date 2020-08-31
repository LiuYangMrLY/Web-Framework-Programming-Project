from django.db import models


class User(models.Model):
    username = models.CharField(max_length=20, verbose_name='用户名', unique=True, null=False, blank=False)
    password = models.CharField(max_length=100, verbose_name='密码', null=False, blank=False)

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = '用户'

    def __str__(self):
        return self.username

    @property
    def info(self):
        return UserInfo.objects.filter(user=self)[0]


class UserInfo(models.Model):
    Gender = (
        ('M', 'male'),
        ('F', 'female'),
        ('S', 'secret'),
    )

    user = models.ForeignKey('User', on_delete=models.PROTECT, verbose_name='用户')
    name = models.CharField(max_length=50, verbose_name='姓名', null=False, blank=True, default='')
    sex = models.CharField(max_length=1, verbose_name='性别', choices=Gender, null=False, blank=False, default='S')
    avatar = models.ImageField(upload_to='img', verbose_name='头像', default='default.jpg')
    email = models.EmailField(verbose_name='邮箱', null=False, blank=True, default='')
    quote = models.CharField(max_length=200, verbose_name='自我名言', null=False, blank=True, default='')
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    last_edited_time = models.DateTimeField(verbose_name='修改时间', auto_now=True)

    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user.username

    @property
    def links(self):
        result = []
        for one in self.user.links.all():
            result.append({
                'type': one.type,
                'content': one.content
            })

        return result


class Link(models.Model):
    Link_Type = (
        ('G', 'GitHub'),
        ('C', 'CSDN'),
        ('T', 'Twitter'),
    )

    user = models.ForeignKey('User', on_delete=models.PROTECT, verbose_name='用户', related_name='links')
    type = models.CharField(max_length=1, verbose_name='类型', choices=Link_Type, null=False, blank=False)
    content = models.CharField(max_length=200, verbose_name='网址', null=False, blank=False)

    class Meta:
        verbose_name = '外链'
        verbose_name_plural = '外链'

    def __str__(self):
        return self.user.info.name
