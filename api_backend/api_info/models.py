from django.db import models

# Create your models here.


class ApiGroup(models.Model):
    group_name = models.CharField(max_length=255, primary_key=True, verbose_name='api组名')
    group_description = models.TextField(verbose_name='api组描述')

    class Meta:
        db_table = 'api_group'
        verbose_name = 'api组'
        verbose_name_plural = '02-api组'

    def __str__(self):
        return str(self.group_name)


class ApiInfo(models.Model):
    api_name = models.CharField(max_length=255, primary_key=True, verbose_name='api名')
    api_description = models.TextField(verbose_name='api描述')
    api_url = models.CharField(max_length=255, verbose_name='api url')
    api_docs = models.TextField(verbose_name='api文档')
    api_group = models.ForeignKey(ApiGroup, on_delete=models.CASCADE, db_column='api_group', verbose_name='api组')

    class Meta:
        db_table = 'api_info'
        verbose_name = 'api信息'
        verbose_name_plural = '01-api信息'

    def __str__(self):
        return str(self.api_name)
