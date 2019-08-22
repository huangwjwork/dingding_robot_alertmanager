from django.contrib import admin
from api.models import Receiver, Alert_info
# Register your models here.


class ReceiverAdmin(admin.ModelAdmin):
    list_display = ('receiver', 'dingding_robot_api')
    ordering = ('receiver', )


class Alert_Info_Admin(admin.ModelAdmin):
    list_display = ('id', 'status', 'alertname', 'instance', 'job', 'monitor',
                    'severity', 'startsAt', 'endsAt', 'receiver', 'post_times')
    ordering = ('id', 'startsAt')


admin.site.register(Receiver, ReceiverAdmin)
admin.site.register(Alert_info, Alert_Info_Admin)
