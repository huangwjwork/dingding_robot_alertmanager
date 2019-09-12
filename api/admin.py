from django.contrib import admin
from api.models import Receiver, Alert
# Register your models here.


class ReceiverAdmin(admin.ModelAdmin):
    list_display = ('receiver', 'receiver_num', 'dingtalk_robot_api')
    ordering = ('receiver', 'receiver_num')


class AlertAdmin(admin.ModelAdmin):
    list_display = ('id', 'status', 'alertname', 'instance', 'job', 'startsAt',
                    'endsAt', 'receiver', 'post_times')
    ordering = ('id', 'startsAt')


admin.site.register(Receiver, ReceiverAdmin)
admin.site.register(Alert, AlertAdmin)
