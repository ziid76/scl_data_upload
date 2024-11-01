from django.urls import path
from catalog.views import views, manage_view, user_view, request_view, retire_view, util, upload_view
from django.utils.translation import gettext_lazy as _

urlpatterns = [
    path('', views.index, name='index'),
    path('profile/password/', user_view.password_edit_view, name='password_edit'),
    path('doc/<str:doc_type>', views.docs, name='docs'),
    path('doc/sign/<str:doc_type>', views.doc_sign, name='doc_sign'),
]

# 보안 요청 관리
urlpatterns += [
    path('request', request_view.request_list, name='request'),
    # path('request/new', views.UserRequestCV.as_view(), name='request_new'),
    path('request/create/<int:type_id>', request_view.request_create, name='request_create'),
    path('request/mylist', request_view.UserRequestLV.as_view(), name='request_list'), #개인별 신청내역
    path('request/approve_list', request_view.UserRequestApproveLV, name='request_approve_list'), #승인자 승인목록
    path('request/<int:pk>', request_view.UserRequestDV.as_view(), name='request_detail'), #신청내역 상세
    path('request/approve', request_view.request_approve, name='request_approve')
]
# 인원투입관리
urlpatterns += [
    path('user/<int:pk>', views.ProfileDV.as_view(), name='user'),
    path('user_create/<int:pk>', views.SecUserDV.as_view(), name='user_create_detail'),
    path(_('user_create/add'), views.SecUserCV.as_view(), name='user_create_new'),
    path('user_create/list', views.SECUserList, name='user_create_list'),
    path('user_create/approve_list', views.SecUserApproveLV, name='user_approve_list'),
    path('user_create/approve_result', views.update_approve_list, name='user_approve_result'),
]


# 인원철수관리
urlpatterns += [
    path('user/retire/list', views.ProfileLV.as_view(), name='user_dismiss_list'),
    path('user/retire/<int:id>', retire_view.user_retire, name='user_dismiss'),
    path('user/retire/approve_list', retire_view.UserRetireApproveList, name='user_dismiss_approve_list'),
    path('user/retire/approve', retire_view.retire_approve, name='user_retire_approve'),
    path('user/retire/update', retire_view.user_retire_update, name='user_retire_update')
]

#관리자-현황관리
urlpatterns += [
    path('manage/project_list', manage_view.project_list, name='project_list'),
    path('manage/project_user_list/<int:pjt_id>', manage_view.project_user_list, name='project_user_list'),
    path('manage/user', manage_view.manage_user, name='manage_user'),
    path('manager/tools', manage_view.tools, name='tools'),
]

urlpatterns += [
    path('dev/datepicker', util.datepicker, name='datepicker'),
    path('dev/api/user_api', util.api_user_approve, name='api_user'),
]

urlpatterns += [
    path('upload/', upload_view.upload_excel, name='upload_excel'),
    path('upload/success/',upload_view.upload_success, name='upload_success'),
    path('upload/commit/',upload_view.commit_excel_upload, name='upload_commit'),
    path('upload/upload_result/',upload_view.excel_upload_result, name='excel_upload_result'),
    path('upload/history/',upload_view.excel_upload_history, name='upload_history'),
    path('upload/<int:pk>',upload_view.excel_upload_detail, name='upload_detail'),

]

