# coding: utf-8
import json
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from game_room.models import ApplyDetail
from .utils import AliPay
from django.db.backends import utils

APP_ID = '2018030502317371'
PRO_APP_ID = '2018030502317371'
SELLER_ID = '2088031427786165'


ALIPAY_TRADE_REFUND_MSG = {
    'ACQ.SYSTEM_ERROR': u'支付宝系统错误，请重试',
    'ACQ.SELLER_BALANCE_NOT_ENOUGH': u'商家余额不足，请联系客服处理',
    'ACQ.REFUND_AMT_NOT_EQUAL_TOTAL': u'退款金额超限',
    'ACQ.REASON_TRADE_BEEN_FREEZEN': u'请求退款的交易被冻结，联系支付宝小二，确认该笔交易的具体情况',
    'ACQ.TRADE_NOT_EXIST': u'交易不存在',
    'ACQ.TRADE_HAS_FINISHED': u'该交易已完结，不允许进行退款',
    'ACQ.TRADE_STATUS_ERROR': u'交易状态非法，确认交易是否已经付款',
    'ACQ.REASON_TRADE_REFUND_FEE_ERR': u'退款金额无效',
    'ACQ.TRADE_NOT_ALLOW_REFUND': u'当前交易不允许退款'
}


def alipay_info(request):
    order_id = request.GET.get('order_id')
    user_id = request.GET.get('user_id')
    print(order_id)
    print(user_id)
    order = ApplyDetail.objects.get(pk=order_id, user_id=user_id)
    alipay = AliPay(
        appid=PRO_APP_ID,
        app_notify_url='http://tzadmin.jiuxingjinfu.cn/alipay/callback/',
        app_private_key_path='%s/alipay/private.pem' % settings.PROJECT_DIR,
        alipay_public_key_path='',
        sign_type ='RSA2',
        debug = False
    )
    subject = order.room.name
    out_trade_no = order_id
    total_amount = order.money
    signed_string = alipay.api_alipay_trade_app_pay(subject, out_trade_no, total_amount, notify_url=None)
    data = {
        'signed_string': signed_string
    }
    result = {'returnCode': 1, 'error': 'success', 'data': data}
    response = HttpResponse(content=json.dumps(result))
    return response


    # 支付宝支付异步回调,验签等操作
def alipay_callback(self, request, format=None):
    print(request.POST)
    print(request.GET)
    return JsonResponse(data={'data': 'OK'})

    # result = 'failure'
    # alipay = AliPay(
    #     appid=PRO_APP_ID,
    #     app_notify_url='',
    #     app_private_key_path='',
    #     alipay_public_key_path='%s/alipay/pro_public.pem' % settings.PROJECT_DIR,
    #     sign_type = 'RSA2',
    #     debug = False
    # )
    # request.data._mutable = True
    # data = request.data
    # signature = data.pop('sign')[0]
    # print(json.dumps(data))
    # print(signature)
    # success = alipay.verify(data, signature)
    # trade_no = data.get('trade_no', None)
    # out_trade_no = data.get('out_trade_no')
    # total_amount = data.get('total_amount')
    # gmt_payment = data.get('gmt_payment')
    # seller_id = data.get('seller_id')
    # app_id = data.get('app_id')
    # if success:
    #     order = Order.objects.get(pk=out_trade_no)
    #     if not order:
    #         return HttpResponse(result)
    #     if not total_amount == utils.format_number(order.price, decimal_places=2, max_digits=10):
    #         # print u'订单号:%s，支付金额%s与订单金额不符，请检查' % (out_trade_no, total_amount)
    #         return HttpResponse(result)
    #     if not seller_id == SELLER_ID:
    #         # print u'订单号:%s，返回的商户ID(%s)不符，请检查' % (out_trade_no, seller_id)
    #         return HttpResponse(result)
    #     if not app_id == alipay.appid:
    #         # print u'订单号:%s，返回的APP_ID(%s)不符，请检查' % (out_trade_no, app_id)
    #         return HttpResponse(result)
    #     trade_status = data.get('trade_status')
    #     if trade_status == u'TRADE_SUCCESS' or trade_status == u'TRADE_FINISHED':
    #         # 修改order状态
    #         if order.status in [1, 7]:
    #             order.status = 2  # 已付款
    #         result = 'success'
    #     elif trade_status == u'TRADE_CLOSED': # 订单支付超时或已退款
    #         result = 'success'
    #     else:
    #         order.status = 7 if not order.status == 6 else 6 # 支付失败，前端显示未支付，可重复支付，如果订单正好自动关闭，则状态不变
    #         # print u'订单号:%s，支付宝返回状态:%s' % (out_trade_no, trade_status)
    #     # print 333
    #     order.trade_id = trade_no
    #     order.update_time = timezone.now()
    #     order.gmt_payment = timezone.datetime.strptime(gmt_payment, '%Y-%m-%d %H:%M:%S')
    #     # print 444
    #     order.save()
    #     # print 'success'
    #     return HttpResponse(result)
    # else:
    #     # print u'订单号:%s，验签失败' % out_trade_no
    #     return HttpResponse(result)

