from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from catalog.models import UserTools, Project, User, UserSign, Company, UserRequest, Profile,  UserRequestApproveMaster


def project_list(request):
    pjt_list = Project.objects.all().filter(yn='N')

    p_cnt = []
    for p_ in pjt_list:
        c_ = Profile.objects.filter(project=p_).count()
        i_ = Profile.objects.filter(project=p_).filter(status='P').count()
        d_ = Profile.objects.filter(project=p_).filter(status='D').count()
        pjt_ = {
            'id':p_.id,
            'name': p_.name,
            'owner': p_.owner,
            'manager': p_.manager,
            'total_': c_,
            'in_': i_,
            'out_':d_
        }
        p_cnt.append(pjt_)

    data = {
        'project_list': p_cnt,
    }

    return render(request, 'project_list.html', data)


def project_user_list(request, pjt_id):

    pjt = Project.objects.filter(id=pjt_id)
    print(pjt[0].name)
    print(type(pjt[0].name))
    user_l = Profile.objects.filter(project=pjt_id)

    user_list = return_profile_detail(user_l)

    data = {
        'pjt_': pjt[0],
        'object': user_list,
    }

    return render(request, 'project_user_list.html', data)


def manage_user(request):

    user_l = Profile.objects.all()
    user_list = return_profile_detail(user_l)

    data = {
        'pjt_': '',
        'object': user_list,
    }

    return render(request, 'project_user_list.html', data)


def return_profile_detail(user_l):
    user_list = []

    for u_ in user_l:
        sign_ = UserSign.objects.filter(loginuser=u_.user)
        use_ = UserTools.objects.filter(user=u_.user.profile).filter(in_use='Y')

        doc_v = 'N'
        doc_s = 'N'
        doc_p = 'N'
        doc_c = 'N'
        doc_d = 'N'

        tool_v = 'N'
        tool_s = 'N'
        tool_d = 'N'
        tool_a = 'N'

        if sign_.count() > 0:
            for s_ in sign_:
                if s_.doc_type == 'V': doc_v = 'Y'
                if s_.doc_type == 'S': doc_s = 'Y'
                if s_.doc_type == 'P': doc_p = 'Y'
                if s_.doc_type == 'C': doc_c = 'Y'
                if s_.doc_type == 'D': doc_d = 'Y'

        if use_.count() > 0:
            for s_ in use_:
                if s_.tools == 'V': tool_v = 'Y'
                if s_.tools == 'S': tool_s = 'Y'
                if s_.tools == 'D': tool_d = 'Y'
                if s_.tools == 'A': tool_a = 'Y'

        rtn = {'id':u_.id,
               'user': u_.user,
               'company': u_.company,
               'project': u_.project,
               'kor_name': u_.kor_name,
               'grade': u_.grade,
               'gen_date': u_.gen_date,
               'del_date': u_.del_date,
               'status': u_.status,
               'doc_v': doc_v,
               'doc_s': doc_s,
               'doc_p': doc_p,
               'doc_c': doc_c,
               'doc_d': doc_d,
               'tool_v': tool_v,
               'tool_s': tool_s,
               'tool_d': tool_d,
               'tool_a': tool_a,
               }
        user_list.append(rtn)

    return user_list


def tools(request):
    so = request.GET.get('so', 'ALL')  # 조회범위

    if so == 'ALL':
        context = UserTools.objects.filter(in_use='Y')
    else:
        context = UserTools.objects.filter(tools=so)

    data = {
        'object_list': context,
        'so': so,
    }

    return render(request, 'admin/tools.html', data)


