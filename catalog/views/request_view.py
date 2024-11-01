import datetime
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from catalog.models import UserTools, Project, User, UserSign, Company, UserRequest, Profile,  UserRequestTypeMaster, UserRequestApproveMaster, UserRequestApprove
from catalog.forms import UserRequestForm
from django.views.generic import ListView, DetailView
from django.urls import reverse_lazy
from django.contrib import messages
import json
from django.http import JsonResponse
from catalog.views.util import send_simple_mail


def request_list(request):
    pjt_list = UserRequestTypeMaster.objects.all().filter(status='Y').order_by('type_name')
    use_list = UserRequest.objects.filter(req_user=request.user)
    in_use = []
    for i in pjt_list:

        exist_ = 'N'
        status_ = ''
        req_id_ = ''

        for t in use_list:
           if i.type == t.type.type:
                exist_ = 'Y'
                status_ = t.status
                req_id_ = t.id

        if exist_ == 'Y':
            l1 = {'id': i.id,
                  'name': i.type_name,
                  'desc': i.type_desc,
                  'type': i.type,
                  'status': status_,
                  'req_id': req_id_,
                  'use':'Y'}
            in_use.append(l1)
        else:
            l2 = {'id': i.id,
                  'name':i.type_name,
                  'desc':i.type_desc,
                  'type':i.type,
                  'status':status_,
                  'req_id': req_id_,
                  'use':'N'}
            in_use.append(l2)

    data = {
        'pjt_': pjt_list,
        'req_': use_list,
        'use_': in_use,

    }

    return render(request, 'request.html', data)


def request_create(request, type_id):
    req_m = UserRequestTypeMaster.objects.filter(id=type_id)


    if request.method == 'POST':
        form = UserRequestForm(request.POST)
        if form.is_valid():

            req_ = form.save(commit=False)
            req_.req_user = request.user
            req_.status = 'N'  # 추가한 속성 author 적용
            req_.date_of_req = datetime.date.today()
            req_.type = req_m[0]
            req_.save()
            make_req_approve_list(type_id, req_, request.user)
            messages.info(request, '정상적으로 처리가 완료되었습니다.')
            return redirect('request_list')
        else: print(form.errors)
    else:
        doc_ = UserSign.objects.filter(loginuser=request.user)
        sign_err = '투입단계 서약이 완료되지 않았습니다. 서약을 완료한 후 보안허용 신청 바랍니다.'

        if doc_:
            chk = []
            for d_ in doc_:
                chk.append(d_.doc_type)
            print(chk)
            if 'V' in chk and 'S' in chk and 'P' in chk:
                form = UserRequestForm()
            else:
                messages.warning(request, sign_err)
                return redirect('request')
        else:
            messages.warning(request, sign_err)
            return redirect('request')

    context = {'form': form}
    context['type'] = type_id
    context['title'] = req_m[0].type_name
    context['desc'] = req_m[0].description

    return render(request, 'request_detail.html', context)


def make_req_approve_list(t_id, req_, reu_):

    add_ = 0
    if reu_.profile.project.manager:
        new_l = UserRequestApprove(req_id=req_, seq=1+add_, stage='Y', app_user=reu_.profile.project.manager)
        new_l.save()

        mail_body = '<br>보안허용 승인요청이 있습니다.<br>'
        mail_body += '<br>요청자 : ' + req_.req_user.profile.kor_name + '&nbsp' + req_.req_user.profile.grade
        mail_body += '<br>요청 유형 : ' + req_.type.type_name

        send_simple_mail('[인원보안포털]승인요청',mail_body , [str(new_l.app_user)+'@serveone.co.kr'])

        add_ += 1
        if reu_.profile.project.owner:
            new_l = UserRequestApprove(req_id=req_, seq=1+add_, app_user=reu_.profile.project.owner)
            new_l.save()
            add_ += 1
    else:
        if reu_.profile.project.owner:
            new_l = UserRequestApprove(req_id=req_, seq=1+add_, stage='Y', app_user=reu_.profile.project.owner)
            new_l.save()
            add_ += 1

    app_u = UserRequestApproveMaster.objects.filter(type=t_id).order_by('seq')
    i = 1
    cnt_a = app_u.count()

    if cnt_a == 1:
        new_l = UserRequestApprove(req_id=req_, seq=i+add_, final='Y', app_user=app_u[0].app_user)
        new_l.save()
    elif cnt_a > 1:
        for u in app_u:
            if i == cnt_a:
                new_l = UserRequestApprove(req_id=req_, seq=i+add_, final='Y', app_user=u.app_user)
                new_l.save()
            else:
                new_l = UserRequestApprove(req_id=req_, seq=i+add_, app_user=u.app_user)
                new_l.save()
            i += 1

    return app_u


def request_approve(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        print(body)

        ref = body['req']
        seq = body['seq']
        entry_main = UserRequest.objects.get(id=ref)
        entry = UserRequestApprove.objects.get(req_id=ref, seq=seq)
        entry_all = UserRequestApprove.objects.all().filter(req_id=ref)
        if body['btn'] == 'approved':
            entry.approved = 'Y'

            if entry.final != 'Y':
                entry_main.status = 'P'
                next_seq = str(int(seq) + 1)
                entry_next = UserRequestApprove.objects.get(req_id=ref, seq=next_seq)
                print(entry_next)
                entry_next.stage = 'Y'
                entry_next.save()
                print(entry_next.app_user)

                mail_body = '<br>보안허용 승인요청이 있습니다.<br>'
                mail_body += '<br>요청자 : ' + entry_main.req_user.profile.kor_name +'&nbsp'+ entry_main.req_user.profile.grade
                mail_body += '<br>요청 유형 : ' + entry_main.type.type_name
                send_simple_mail('[인원보안포털]승인요청', mail_body, [str(entry_next.app_user)+'@serveone.co.kr'])

            else:
                entry_main.status = 'G'
                ty_ = body['type']


                if ty_ != 'N':
                    va_ = body['value']
                    tools = UserTools.objects.create(
                        user=entry_main.req_user.profile,
                        tools=ty_,
                        info=va_,
                        in_use="Y",
                        date_of_start=timezone.now())
                    tools.save()

                    mail_body = '<br>신청하신 [' + entry_main.type.type_name + '] 요청이 승인 되었습니다.'
                    mail_body += '<br>처리결과 : '+ va_
                    mail_body += '<br>프로젝트 담당자의 안내에 따라 이용하여 주시기 바랍니다.'
                    send_simple_mail('[인원보안포털]요청승인완료', mail_body, [str(entry_main.req_user) + '@serveone.co.kr'])

                    if ty_ == 'V':
                        vdi_user = Profile.objects.filter(user=entry_main.req_user)[0]
                        vdi_user.vdi_ip = body['v_ip']
                        vdi_user.save()

                else:
                    mail_body = '<br>신청하신 [' + entry_main.type.type_name + '] 요청이 승인 되었습니다.<br>'
                    mail_body += '<br>프로젝트 담당자의 안내에 따라 이용하여 주시기 바랍니다.'
                    send_simple_mail('[인원보안포털]요청승인완료', mail_body, [str(entry_main.req_user) + '@serveone.co.kr'])


        elif body['btn'] == 'denied':
            entry_main.status = 'D'
            entry.approved = 'N'

            receiver = [str(entry_main.req_user) + '@serveone.co.kr']
            mail_body = '<br>신청하신 ['+entry_main.type.type_name+'] 요청이 반려되었습니다.'
            mail_body += '<br>사유 : '+ body['comment']
            send_simple_mail('[인원보안포털]요청반려', mail_body, receiver)

        entry.stage = ''
        entry.approve_date = timezone.now()
        entry.comment = body['comment']
        entry.save()
        print(entry_main.status)
        entry_main.save()

        data = {
            'object': entry_main,
            'approve_list': entry_all,
            'ref': ref,
            'seq': seq,
        }
        messages.info(request, '정상적으로 처리가 완료되었습니다.')
        return JsonResponse(body)
    else:
        messages.warning(request, '요청처리에 실패하였습니다. 관리자에게 문의바랍니다.')
        return messages


class UserRequestLV(ListView):
    model = UserRequest
    #paginate_by = 10

    def get_queryset(self):
        rtn = UserRequest.objects.filter(req_user=self.request.user).order_by('-date_of_req')
        return rtn

    def get_context_data(self, **kwargs):
        context = super(UserRequestLV, self).get_context_data(**kwargs)
        context['count'] = self.get_queryset().count()
        return context


class UserRequestDV(DetailView):
    model = UserRequest

    def get_context_data(self, **kwargs):
        context = super(UserRequestDV, self).get_context_data(**kwargs)
        context['approve_list'] = UserRequestApprove.objects.all().filter(req_id=self.object).order_by('seq')
        context['curr_user'] = self.request.user
        return context


def UserRequestApproveLV(request):
    rtn = UserRequestApprove.objects.filter(app_user=request.user).filter(stage='Y')
    data = {
        'object_list': rtn,
    }
    return render(request, 'UserRequestApprove_list.html', data)
