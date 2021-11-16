import re

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db import DatabaseError
from django.http import HttpResponseBadRequest, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
# Create your views here.
from django.urls import reverse
from django.utils.timezone import now
from django.views import View

from user.models import User, Staff, DepartMent
from libs.captcha.captcha import captcha


class LoginView(View):
    def get(self, request):
        time = now()
        return render(request, 'login.html', locals())

    def post(self, request):
        mobile = request.POST.get('mobile')
        password = request.POST.get('password')
        remember = request.POST.get('remember')
        if not all([mobile, password]):
            return HttpResponseBadRequest('登录参数不全')
        if not re.match(r'^1[3-9]\d{9}$', mobile):
            return HttpResponseBadRequest('手机号输入格式不正确')
        if not re.match(r'[0-9a-zA-Z]{8,20}', password):
            return HttpResponseBadRequest('请输入8-20位密码')
        user = authenticate(mobile=mobile, password=password)
        if user is None:
            return HttpResponseBadRequest('用户名或密码错误')
        login(request, user)
        response = redirect(reverse('user:index'))
        # 如果没有点击记住密码
        if remember != 'on':
            request.session.set_expiry(0)
            response.set_cookie('is_login', True)
            response.set_cookie('username', user.username, max_age=14 * 24 * 3600)
        else:
            request.session.set_expiry(None)
            response.set_cookie('is_login', True)
            response.set_cookie('username', user.username, max_age=14 * 24 * 3600)

        return response


class ImageCodeView(View):
    def get(self, request):
        text, image = captcha.generate_captcha()
        print(text)
        print(image)
        return HttpResponse(image, content_type='image/jpeg')


class RegisterView(View):
    def get(self, request):
        time = now()
        return render(request, 'regist.html', locals())

    def post(self, request):
        username = request.POST.get('username')
        mobile = request.POST.get('mobile')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        gender = request.POST.get('sex')
        if not all([username, mobile, password, password2, gender]):
            return HttpResponseBadRequest('注册参数不全')
        if not re.match(r'^1[3-9]\d{9}$', mobile):
            return HttpResponseBadRequest('手机号输入格式不正确')
        if not re.match(r'[0-9a-zA-Z]{8,20}', password):
            return HttpResponseBadRequest('请输入8-20位密码')
        if password != password2:
            return HttpResponseBadRequest('两次输入密码不一致')
        # 保存注册用户
        try:
            User.objects.create_user(mobile=mobile, username=username, password=password)
        except DatabaseError:
            return HttpResponseBadRequest('注册失败，请稍后重试。')

        return redirect(reverse('user:login'))


class UpdateView(View):
    def get(self, request):
        update_id = request.GET.get('update_id')
        dep_names = DepartMent.objects.all()
        staff = Staff.objects.get(id=update_id)
        time = now()
        return render(request, 'updateEmp.html', locals())

    def post(self, request):
        id = request.POST.get('id')
        staff_name = request.POST.get('name')
        salary = request.POST.get('salary')
        age = request.POST.get('age')
        gender = request.POST.get('gender')
        birthday = request.POST.get('birthday')
        dep_id = request.POST.get('dep_id')
        # 因为存在外键，所以需要先实例化外键查询，然后再插入的表里面放入实例化后的外键连接
        dep_id = DepartMent.objects.get(id=dep_id)
        if not all([staff_name, salary, age, gender, birthday]):
            return HttpResponseBadRequest('请求参数不齐全')
        # 保存员工信息
        try:
            Staff.objects.filter(id=id).update(staff_name=staff_name,
                                               salary=salary,
                                               age=age,
                                               gender=gender,
                                               birthday=birthday,
                                               department_id=dep_id)
        except DatabaseError:
            return HttpResponseBadRequest('修改失败，请稍后重试')
        return redirect(reverse('user:index'))


class AddView(View):
    def get(self, request):
        time = now()
        dep_name = DepartMent.objects.all()
        return render(request, 'addEmp.html', locals())

    def post(self, request):
        staff_name = request.POST.get('name')
        salary = request.POST.get('salary')
        age = request.POST.get('age')
        gender = request.POST.get('gender')
        birthday = request.POST.get('birthday')
        dep_id = request.POST.get('dep_id')
        # 因为存在外键，所以需要先实例化外键查询，然后再插入的表里面放入实例化后的外键连接
        dep_id = DepartMent.objects.get(id=dep_id)
        if not all([staff_name, salary, age, gender, birthday]):
            return HttpResponseBadRequest('请求参数不齐全')
        # 保存员工信息
        try:
            Staff.objects.create(staff_name=staff_name,
                                 salary=salary,
                                 age=age,
                                 gender=gender,
                                 birthday=birthday,
                                 department_id=dep_id)
        except DatabaseError:
            return HttpResponseBadRequest('添加失败，请稍后重试')
        return redirect(reverse('user:index'))


class IndexView(LoginRequiredMixin, View):
    def get(self, request):
        staffs = Staff.objects.all()
        departments = DepartMent.objects.all()

        time = now()
        # 创建分页器对象
        paginator = Paginator(staffs, per_page=5)
        # 返回总页数
        total_page = paginator.page_range
        page_num = int(request.GET.get('pagenum', 1))
        if page_num not in total_page:
            page_num = 1
        # 每一页的对象
        page = paginator.page(page_num)
        return render(request, 'emplist.html', locals())

    def post(self, request):
        pass


class DeleteView(View):
    def get(self, request):

        delete_id = request.GET.get('delete_id')
        try:
            Staff.objects.get(id=delete_id).delete()
        except DatabaseError:
            return HttpResponseBadRequest('删除失败，请稍后重试')
        return redirect(reverse('user:index'))

    def post(self, request):
        pass


class LogoutView(View):
    def get(self, request):
        logout(request)
        response = redirect(reverse('user:login'))
        response.delete_cookie('is_login')
        return response


# ajax
def register_handle(request):
    mobile = request.GET.get('mobile')
    res = User.objects.filter(mobile=mobile)
    if res:
        return HttpResponse('该手机号已注册')
    else:
        return HttpResponse('')


def login_handle(request):
    mobile = request.GET.get('mobile')
    res = User.objects.filter(mobile=mobile)
    if res:
        return HttpResponse('')
    else:
        return HttpResponse('您输入的手机号未注册!')
