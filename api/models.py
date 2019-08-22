from django.db import models
'''
表1 receiver(主键) dingding-webhook
表2 自增ID alertname instance job monitor severity startsAt endsAt receiver post_times
'''


# Create your models here.
class Receiver(models.Model):
    receiver = models.CharField(primary_key=True, max_length=30)
    dingding_robot_api = models.CharField(max_length=200)

    class Meta:
        db_table = 'receiver'


class Alert_info(models.Model):
    id = models.AutoField(primary_key=True)
    alertname = models.CharField(max_length=100)
    instance = models.CharField(max_length=50)
    job = models.CharField(max_length=30)
    monitor = models.CharField(max_length=30)
    severity = models.CharField(max_length=30)
    startsAt = models.DateTimeField()
    endsAt = models.DateTimeField()
    receiver = models.CharField(max_length=30)
    status = models.CharField(max_length=10)
    post_times = models.PositiveIntegerField()

    class Meta:
        db_table = 'alert_info'

    def get_webhook_url(self):
        return Receiver.objects.get(receiver=self.receiver).dingding_robot_api
