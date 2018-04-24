from django.contrib.sessions.models import Session
from django.http import JsonResponse

from exception.base import TZBaseError
from tz_user.models import TZUser

def auth_required(view):
    def decorator(request, *args, **kwargs):
        data = {}
        print(request.GET)
        print(request.POST)
        token = request.POST.get('tztoken') or request.GET.get('tztoken')
        try:
            session = Session.objects.filter(session_key=token).first()
            if not session:
                data['code'] = 10001
                data['msg'] = '登录已过期，请重新登录！'
            else:
                user_id = session.session_data
                user = TZUser.objects.filter(pk=user_id).first()
                request.user = user
                return view(request, *args, **kwargs)
        except TZBaseError as e:
            data['code'] = e.code
            data['msg'] = e.msg
        return JsonResponse(data=data)
    return decorator