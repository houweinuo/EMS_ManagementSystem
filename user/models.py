from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.

# 管理员模型
class User(AbstractUser):
    mobile = models.CharField(max_length=50, unique=True)
    USERNAME_FIELD = 'mobile'
    REQUIRED_FIELDS = ['username']

    class Meta:
        db_table = 'tb_user'
        verbose_name_plural = '管理员'

    def __str__(self):
        return self.mobile


# 部门模型
class DepartMent(models.Model):
    dep_name = models.CharField(max_length=50)

    class Meta:
        db_table = 'tb_dep'
        verbose_name_plural = '部门管理'

    def __str__(self):
        return self.dep_name


# 员工模型
class Staff(models.Model):
    GENDER_CHOICE = [
        (0, '男'),
        (1, '女'),
    ]
    staff_name = models.CharField(max_length=50)
    age = models.PositiveSmallIntegerField()
    salary = models.PositiveIntegerField()
    avatar = models.ImageField(upload_to='avatar/%Y%m%d', blank=True)
    birthday = models.DateField()
    gender = models.IntegerField(choices=GENDER_CHOICE)
    department_id = models.ForeignKey(DepartMent, on_delete=models.CASCADE)

    class Meta:
        db_table = 'tb_staff'
        verbose_name_plural = '员工管理'

    def __str__(self):
        return self.staff_name
