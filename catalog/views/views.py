import datetime

from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import  ListView, DetailView, TemplateView
from catalog.models import secUser, UserTools, User, UserSign, CodeB,Company, SecUserApprove, Profile, UserRequest, UserRequestApprove, UserRequestApproveMaster, ExcelUploadRecord, UserRetire, UserRetireApprove
from django.views.generic.edit import CreateView
from django.contrib.messages.views import SuccessMessageMixin
from catalog.views.util import send_simple_mail
from django.urls import reverse_lazy
from django.utils import timezone
import json
from django.http import JsonResponse
from django.db.models import Q


@login_required
def index(request):

    company_list = Company.objects.all()
  
    upload_result = []

    for i in company_list:
        record_=ExcelUploadRecord.objects.filter(company=i.code)
        upload_data = [i.name, False, False, False, False, False, False, False, False, False, False, False, False,]

        for row in record_:
            yy, mm = row.year_month.split('-')
            upload_data[int(mm)] = True

        upload_result.append(upload_data)  


    context = {
        'upload_result': upload_result
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)


def docs(request, doc_type):
    sign_check = UserSign.objects.filter(doc_type=doc_type).filter(loginuser=request.user).count()
    sign_date = ''

    if sign_check == 1:
        sign = UserSign.objects.filter(doc_type=doc_type).filter(loginuser=request.user)
        sign_date = sign[0].signdate
    user_ = Profile.objects.filter(user=request.user)[0]

    return_page = 'docs.html'

    code_ = CodeB.objects.filter(code='D'+doc_type)

    context = {
        'profile': user_,
        'today': datetime.date.today(),
        'title': code_[0].title,
        'body': code_[0].body,
        'sign_check': sign_check,
        'sign_date': sign_date,
        'doc_type': doc_type,
    }

    return render(request, return_page, context=context)


def doc_sign(request, doc_type):
    if request.method == "POST":
        loginuser = request.user
        signdate = datetime.date.today()
        docSign = UserSign(loginuser=loginuser, doc_type=doc_type, signdate=signdate)
        docSign.save()
        messages.info(request, '서명이 완료되었습니다.')
    else:
        return redirect('docs', doc_type)

    return redirect('docs', doc_type)


class SecUserDV(DetailView):
    model = secUser
    owner = secUser.name

    def get_context_data(self, **kwargs):
        context = super(SecUserDV, self).get_context_data(**kwargs)
        context['approve_list'] = SecUserApprove.objects.all().filter(user_req=self.object).order_by('seq')
        context['curr_user'] = self.request.user
        return context


class SecUserLV(ListView):
    model = secUser

    def get_queryset(self):
        rtn = secUser.objects.filter(req_user=self.request.user).filter(status='N').order_by('-date_of_start')
        return rtn

    def get_context_data(self, **kwargs):
        context = super(SecUserLV, self).get_context_data(**kwargs)
        return context


def SECUserList(request):

    so = request.GET.get('so', 'P')  # 조회범위

    if so == 'P':
        context =  secUser.objects.filter(req_user=request.user).filter(Q(status='P')|Q(status='N'))
    elif so == 'N':
        context = secUser.objects.filter(req_user=request.user).filter(status='N')
    elif so == 'G':
        context = secUser.objects.filter(req_user=request.user).filter(status='G')
    elif so == 'D':
        context = secUser.objects.filter(req_user=request.user).filter(status='D')
    else:
        context = secUser.objects.filter(req_user=request.user)

    data = {
        'object_list': context,
        'so': so,
    }
    return render(request, 'catalog/secuser_list.html', data)


class SecUserCV(SuccessMessageMixin, CreateView):
    model = secUser
    fields = ('userid', 'lastname', 'firstname', 'usergrade', 'phone', 'Company', 'project', 'summary')
    success_url = reverse_lazy('user_create_list')
    success_message = "신청이 완료되었습니다."

    def get_context_data(self, **kwargs):
        context = super(SecUserCV, self).get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        form.instance.req_user = self.request.user
        form.instance.date_of_start = datetime.date.today()
        context = self.get_context_data()
        self.object = form.save()

        make_approve_list(self.object, self.object.project.owner, self.object.project.manager)

        return super().form_valid(form)


def make_approve_list(a, b, c):
    new_list = SecUserApprove(user_req=a, seq=1, stage='Y', app_user=b)
    new_list.save()

    receiver=[str(new_list.app_user)+'@samchully.co.kr']
    send_simple_mail('[그룹 성과 관리]승인요청', '계정 생성 요청이 있습니다.',receiver)

    new_list = SecUserApprove(user_req=a, seq=2, final='Y', app_user=c)
    rtn = new_list.save()

    return rtn


def create_account(final_id, ip_, empID_, entry_main):
    print(entry_main.firstname)

    new_user = User.objects.create_user(username=final_id,
                                        email=final_id+"@samchully.co.kr",
                                        password="1!"+final_id,
                                        last_name=entry_main.lastname,
                                        first_name=entry_main.firstname)
    new_user.save()

    t = '[안내]그룹 성과 관리 접속 계정이 생성되었습니다.'

    b = '삼천리 그룹 성과 관리 계정 생성 안내<br>'
    b += '<br>ID :&nbsp'+final_id
    b += '<br>Password :&nbsp1!'+final_id
    b += '<br><br>사용 안내'
    b += '<br>- 최초 로그인 후 패스워드 변경하여 사용해 주시기 바랍니다.'


    r = [final_id+'@samchully.co.kr']
    send_simple_mail(t, b, r)

    new_profile = Profile(user=new_user, kor_name=entry_main.lastname+entry_main.firstname,
                          grade=entry_main.usergrade, company=entry_main.Company,
                          project=entry_main.project, permission='G', status='P', ip=ip_, empID=empID_,
                          phone=entry_main.phone, gen_date=datetime.date.today())
    rtn = new_profile.save()

    return rtn


def update_approve_list(request):
    print(request.method)
    if request.method == 'POST':
        body = json.loads(request.body)
        print(body)
        ref = body['req']
        seq = body['seq']
        comment_ = body['comment']

        entry_main = secUser.objects.get(pk=ref)
        entry = SecUserApprove.objects.get(user_req=ref, seq=seq)
        entry_all = SecUserApprove.objects.all().filter(user_req=ref)
        if body['btn'] == 'approved':
            entry.approved = 'Y'

            if entry.final != 'Y':
                entry_main.status = 'P'
                next_seq = str(int(seq) + 1)
                entry_next = SecUserApprove.objects.get(user_req=ref, seq=next_seq)
                entry_next.stage = 'Y'
                entry_next.save()

                receiver = [str(entry_next.app_user)+'@samchully.co.kr']
                send_simple_mail('[그룹 성과 관리]승인요청', '계정생성 승인요청이 있습니다.', receiver)
            else:
                entry_main.status = 'G'
                final_id = body['account']
                ip_ = body['ip']
                empID_ = body['empID']
                if final_id =='':
                    messages.warning(request, '그룹웨어 계정이 입력되지 않았습니다.<br>계정 입력 후 재처리 바랍니다.')
                    return messages
                else: create_account(final_id, ip_, empID_, entry_main)

        elif body['btn'] == 'denied':
            entry_main.status = 'D'
            entry.approved = 'N'

        entry.stage = ''
        entry.approve_date = timezone.now()
        entry.comment = comment_
        entry.save()
        entry_main.save()

        messages.info(request, '정상적으로 처리가 완료되었습니다.')
        return JsonResponse(body)
    else:
        messages.warning(request, '요청처리에 실패하였습니다. 관리자에게 문의바랍니다.')
        return messages


def SecUserApproveLV(request):
    rtn = SecUserApprove.objects.filter(app_user=request.user).filter(stage='Y')
    data = {
        'object_list': rtn,
    }
    return render(request, 'SecUserApprove_list.html', data)


class UserRequestCV(CreateView):
    model = UserRequest
    fields = ('type', 'ip_address', 'memo')
    success_url = reverse_lazy('request_list')

    def get_context_data(self, **kwargs):
        context = super(UserRequestCV, self).get_context_data(**kwargs)

        return context

    def form_valid(self, form):
        form.instance.req_user = self.request.user
        form.instance.date_of_req = datetime.date.today()
        context = self.get_context_data()
        self.object = form.save()

        ####  프로젝트 담당자 등록
        make_request_approve_list(self.object, 1, self.object.req_user.profile.project.owner, "Y")

        #### 신청유형별 조치 담당자 등록
        approve_list = UserRequestApproveMaster.objects.all().filter(type=self.object.type)

        for i in approve_list:
            make_request_approve_list(self.object, i.seq+1, i.app_user, "")

        return super().form_valid(form)


def make_request_approve_list(obj, i, req, yn):
    new_list = UserRequestApprove(req_id=obj, seq=i, app_user=req, stage=yn)
    rtn = new_list.save()

    return rtn


class ProfileDV(DetailView):
    model = Profile

    def get_context_data(self, **kwargs):
        context = super(ProfileDV, self).get_context_data(**kwargs)
        context['tools_'] = UserTools.objects.all().filter(user=self.object)
        context['docs_'] = UserSign.objects.all().filter(loginuser=self.object.user)
        context['reqs_'] = UserRequest.objects.filter(req_user=self.object.user)
        context['approve_'] = UserRetireApprove.objects.filter(retiree=self.object).order_by('seq')
        act_ = UserRetire.objects.filter(retiree=self.object).order_by('code')
        context['retire_'] = act_

        return context


class ProfileLV(ListView):
    model = Profile

    def get_queryset(self):
        rtn = Profile.objects.filter(status="O")
        return rtn

    def get_context_data(self, **kwargs):
        context = super(ProfileLV, self).get_context_data(**kwargs)
        context['mylist'] = UserRetire.objects.filter(status="N").filter(manager=self.request.user)
        return context




