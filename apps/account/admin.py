from django.contrib import admin

from . import models


# register models
admin.site.register([models.User, models.UserInfo, models.Link])

