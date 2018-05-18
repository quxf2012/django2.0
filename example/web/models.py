from django.db import models


# Create your models here.


class Assets(models.Model):
    """
        资产表
    """
    hostname = models.CharField(max_length=32, blank=True, null=True)
    system_type = models.CharField(max_length=32, blank=True, null=True)
    system_version = models.CharField(max_length=8, blank=True, null=True)
    system_arch = models.CharField(max_length=16, blank=True, null=True)
    lan_ip = models.CharField(max_length=24, unique=True)
    wan_ip = models.CharField(max_length=64, blank=True)
    idc_id = models.IntegerField()
    mac = models.CharField(max_length=32, blank=True, null=True)
    kernel = models.CharField(max_length=32, blank=True, null=True)
    kernel_version = models.CharField(max_length=64, blank=True, null=True)
    cpu_model = models.CharField(max_length=64, blank=True, null=True)
    cpu_num = models.CharField(max_length=4, blank=True, null=True)
    memory = models.CharField(max_length=128, blank=True, null=True)
    disk = models.CharField(max_length=1024, blank=True, null=True)
    status = models.CharField(max_length=16, blank=True, null=True)

    def __str__(self):
        return self.lan_ip

    class Meta:
        verbose_name = "资产"
        verbose_name_plural = "资产管理"
