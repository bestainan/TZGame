from django.contrib import admin
from django.db.models import F
from xadmin.views import filter_hook, UpdateAdminView

from .models import TZUser, Mail
import xadmin


class TZUserAdmin(object):
    title = 'users'
    list_display = ['nickname', 'add_money', 'tel', ]
    search_fields = ['nickname', 'tel', 'alipay_name']
    exclude = ['is_delete', 'total', 'auth', 'invite_user', 'alipay_name', 'alipay_account', 'bank_name', 'bank_account', 'bank_card_name']

    @filter_hook
    def save_models(self):
        obj = self.new_obj
        if obj.add_money>0:
            obj.money += F('add_money')
            obj.total += F('add_money')
            if obj.invite_user:
                obj.invite_user.money += obj.add_money * 0.3
                obj.invite_user.save()
                if obj.invite_user.invite_user:
                    obj.invite_user.invite_user.money += obj.add_money * 0.3
                    obj.invite_user.invite_user.save()
            obj.save()
            obj.add_money = 0
            obj.save()
        flag = self.org_obj is None and 'create' or 'change'
        self.log(flag, self.change_message(), self.new_obj)


class TZUserMailAdmin(object):
    title = 'mails'
    list_display = ['title', 'info', 'user']
    search_fields = ['title', 'user']


    # list_display = [ 'name','desc','detail','degree','learn_times','students','get_zj_nums','go_to']   #显示的字段
    # search_fields = ['name', 'desc', 'detail', 'degree', 'students']             #搜索
    # list_filter = [ 'name','desc','detail','degree','learn_times','students']    #过滤
    # model_icon = 'fa fa-book'            #图标
    # ordering = ['-click_nums']           #排序
    # readonly_fields = ['click_nums']     #只读字段
    # exclude = ['fav_nums']               #不显示的字段
    # # list_editable = ['degree','desc']
    # # refresh_times = [3,5]                #自动刷新（里面是秒数范围）
    # inlines = [LessonInline,CourseResourceInline]    #增加章节和课程资源
    # style_fields = {"detail": "ueditor"}
    #
    # def queryset(self):
    #     # 重载queryset方法，来过滤出我们想要的数据的
    #     qs = super(CourseAdmin, self).queryset()
    #     # 只显示is_banner=True的课程
    #     qs = qs.filter(is_banner=False)
    #     return qs
    #


xadmin.site.register(TZUser, TZUserAdmin)
xadmin.site.register(Mail, TZUserMailAdmin)
