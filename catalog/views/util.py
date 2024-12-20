from django.core.mail import EmailMessage
from django.shortcuts import render
import json
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import JsonResponse
import logging

logger = logging.getLogger('security')


def test_mail():
    t = 'Doc V 조회'
    b = 'Doc V가 조회되었습니다.'
    r = ['ziid76@gmail.com']

    rtn = send_simple_mail(t, b, r)

    return rtn


def send_simple_mail(title, body, receiver):
    mode = 'TEST'

    mail_template = '<head><meta http-equiv="Content-Type" content="text/html; charset=utf-8">  <title>그룹 성과 관리 시스템</title>'
    mail_template +='<style type="text/css">  body { margin-left: 0px; margin-top: 0px; margin-right: 0px; margin-bottom: 0px; } </style> </head>'
    mail_template +='<body><div style="position:absolute; width:100%;  overflow:hidden; border-top:#d64b72 solid 2px; font-family:맑은 고딕;color:#6d6d6d;line-height:30px;overflow:hidden; border-top:#d64b72 solid; border-bottom:#d64b72 solid 2px;font-family:Dotum,돋움,sans-serif;color:#6d6d6d;line-height:30px;  no-repeat;font-size:13px;">'
    mail_template += '<center> <table width="100%" border="0" cellspacing="0" cellpadding="20"><tr><td><b>그룹 성과 관리 시스템</b></td></tr><tr><td>'
    mail_template += body
    mail_template +='</td></tr> <tr><td>그룹 성과 관리 시스템 <a href="https://...">바로가기</a> &nbsp URL : https://...'
    mail_template +='<br><p style="font-size:14px;color:red">* 그룹 성과 관리 시스템은 크롬 브라우저에 최적화되어 있습니다. 크롬이나 엣지 브라우저를 통해 접속해주세요. *'
    mail_template +='<br>* 본 메일은 발신전용 메일입니다. 문의나 연락은 디지털기획팀 담당자에게 해주시기 바랍니다. *</p></td></tr></table> </div></body>'

    #테스트용 메일수신자
    if mode == 'TEST':
        print('mail to : ')
        print(receiver)
        receiver = ['ziid@samchully.co.kr']

    email = EmailMessage(
        title,  # 제목
        mail_template,  # 내용
        'ziid@samchully.co.kr', # 발신자
        to=receiver,  # 받는 이메일 리스트
    )
    email.content_subtype = "html"
    rtn = email.send()

    return rtn


def datepicker(request):
    return render(request, 's_datepicker.html')


@csrf_exempt
def api_user_approve(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        logger.info("API POST :")
        logger.info(body)
        return JsonResponse(body)
    else:
        logger.info("API GET :")
        context = {
            "method": request.method,
            #"dataset":json.loads(request.body)
            "dataset": request.GET.get('str')
        }
        logger.info(context)
        return render(request, 'api_test.html', context=context)

