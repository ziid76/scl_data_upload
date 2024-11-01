import datetime

from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import  ListView, DetailView, TemplateView
from catalog.models import secUser, UserTools, User, UserSign, CodeB, SecUserApprove, Profile, UserRequest, UserRequestApprove, UserRequestApproveMaster, UserCode,UserRetire, UserRetireApprove
from django.views.generic.edit import CreateView
from django.contrib.messages.views import SuccessMessageMixin
from catalog.views.util import send_simple_mail
from django.urls import reverse_lazy
from django.utils import timezone
import json
from django.http import JsonResponse
from django.db.models import Q


@login_required
def UserRetireApproveList(request):
    rtn = UserRetireApprove.objects.filter(app_user=request.user).filter(stage='Y')
    data = {
        'object_list': rtn,
    }
    return render(request, 'UserRetireApprove_list.html', data)


def user_retire(request, id):

    p_ = Profile.objects.filter(id=id)[0]
    p_.status = 'O'
    p_.ret_date = timezone.now()
    p_.save()

    ret_ = UserRetireApprove(retiree=p_, seq=1, app_user=p_.project.owner, stage='Y')
    ret_.save()
    ret_ = UserRetireApprove(retiree=p_, seq=2, app_user=p_.project.manager, final='Y')
    ret_.save()

    send_simple_mail('[인원보안포털]철수승인요청', '인원철수 승인요청이 있습니다.', [str(p_.project.owner) + '@serveone.co.kr'])

    messages.info(request, '철수 신청이 완료 되었습니다.')

    return redirect('user', id)


def user_retire_update(request):

    if request.method == 'POST':
        body = json.loads(request.body)
        print(body)
        pid_ = body['profile']
        c_ = body['code']
        t_ = body['type']
        p_ = Profile.objects.filter(id=pid_)[0]
        code_ = UserCode.objects.filter(code=c_)[0]
        comment_ = body['comment']

        tools_ = UserTools.objects.filter(user=p_).filter(tools=t_)
        for t in tools_:
            t.in_use = 'N'
            t.date_of_end = timezone.now()
            t.save()

        update_t = UserRetire.objects.filter(retiree=p_).filter(code=code_)[0]
        update_t.status = 'Y'
        update_t.comment = comment_
        update_t.date = timezone.now()
        update_t.save()

        sum_ = UserRetire.objects.filter(retiree=p_).count()
        cnt_ = UserRetire.objects.filter(retiree=p_).filter(status='Y').count()

        if sum_ == cnt_:
            p_.status = 'D'
            p_.del_date = timezone.now()
            p_.save()

        messages.info(request, '정상적으로 처리가 완료되었습니다.')

        return JsonResponse(body)

    else:
        print('실패')
        messages.warning(request, '요청처리에 실패하였습니다. 관리자에게 문의바랍니다.')
        return messages


def retire_approve(request):
    print(request.method)
    if request.method == 'POST':
        body = json.loads(request.body)
        print(body)
        ref = body['approveID']

        entry = UserRetireApprove.objects.get(pk=ref)
        p_ = Profile.objects.filter(id=entry.retiree.id)[0]

        if body['btn'] == 'approved':
            entry.approved = 'Y'

            if entry.final != 'Y':
                next_seq = str(int(entry.seq) + 1)
                entry_next = UserRetireApprove.objects.get(retiree=entry.retiree, seq=next_seq)
                entry_next.stage = 'Y'
                entry_next.save()

                receiver = [str(entry_next.app_user)+'@serveone.co.kr']
                send_simple_mail('[인원보안포털]철수승인요청', '인원철수 승인요청이 있습니다.', receiver)
            else:
                code_ = UserCode.objects.filter(status='Y').order_by('code')
                for c_ in code_:
                    new_ = UserRetire(retiree=p_, code=c_, manager=c_.manager)
                    new_.save()
                    mail_body = '<br>인원철수처리 요청이 있습니다.<br>'
                    mail_body += '<br>대상자 : '+ str(p_)
                    mail_body += '<br>요청 : '+ str(c_)
                    send_simple_mail('[인원보안포털]철수처리요청', mail_body, [str(c_.manager)+'@serveone.co.kr'])

        elif body['btn'] == 'denied':
            entry.approved = 'N'
            p_.status = 'P'

        entry.stage = ''
        entry.approve_date = timezone.now()
        entry.comment = body['comment']
        entry.save()
        p_.save()

        messages.info(request, '정상적으로 처리가 완료되었습니다.')
        return JsonResponse(body)
    else:
        messages.warning(request, '요청처리에 실패하였습니다. 관리자에게 문의바랍니다.')
        return messages
