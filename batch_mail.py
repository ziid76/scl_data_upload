#!/usr/bin/env python

import re
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "secup.settings")
import django
django.setup()

from catalog.models import Profile, Company, Project, UserRetireApprove, UserRequestApprove, SecUserApprove, UserRetire
from django.contrib.auth.models import User
from catalog.views.util import send_simple_mail
from django.db.models import Count
import logging

logger = logging.getLogger('batch-mail')


def check_request():
	status_y = UserRequestApprove.objects.filter(stage='Y').values('app_user').annotate(dcount=Count('app_user'))

	for line in status_y:
		approver = Profile.objects.filter(user=line['app_user'])[0]

		t = '[인원보안포털]보안허용 요청이 있습니다.'

		b = '미승인된 보안허용 신청이 있어 안내드립니다.<br>'
		b += '<br>미승인 건수 :&nbsp' + str(line['dcount']) +'건'

		r = [str(approver.user) + '@serveone.co.kr']

		send_simple_mail(t, b, r)
		
		batchlog('보안허용요청', r, str(line['dcount']))


def check_user():
	status_y = SecUserApprove.objects.filter(stage='Y').values('app_user').annotate(dcount=Count('app_user'))

	for line in status_y:
		approver = Profile.objects.filter(user=line['app_user'])[0]

		t = '[인원보안포털]인력투입 요청이 있습니다.'

		b = '미승인된 인력투입 신청이 있어 안내드립니다.<br>'
		b += '<br>미승인 건수 :&nbsp' + str(line['dcount']) +'건'

		r = [str(approver.user) + '@serveone.co.kr']

		send_simple_mail(t, b, r)
		
		batchlog('인력투입', r, str(line['dcount']))


def check_retire():
	status_y = UserRetireApprove.objects.filter(stage='Y').values('app_user').annotate(dcount=Count('app_user'))

	for line in status_y:
		approver = Profile.objects.filter(user=line['app_user'])[0]

		t = '[인원보안포털]철수승인이 요청이 있습니다.'

		b = '미승인된 인력철수 요청이 있어 안내드립니다.<br>'
		b += '<br>미승인 건수 :&nbsp' + str(line['dcount']) +'건'

		r = [str(approver.user) + '@serveone.co.kr']

		send_simple_mail(t, b, r)
		
		batchlog('철수승인', r, str(line['dcount']))


def check_retire_deal():
	status_y = UserRetire.objects.filter(status='').values('manager').annotate(dcount=Count('manager'))

	for line in status_y:
		approver = Profile.objects.filter(user=line['manager'])[0]

		t = '[인원보안포털]인력철수 처리요청이 있습니다.'

		b = '미승인된 인력철수 처리요청이 있어 안내드립니다.<br>'
		b += '<br>미처리 건수 :&nbsp' + str(line['dcount']) +'건'

		r = [str(approver.user) + '@serveone.co.kr']

		send_simple_mail(t, b, r)
		
		batchlog('철수처리', r, str(line['dcount']))


def batchlog(type, receiver, count):
	logger.info("[" + type +"] 수신자 : " + receiver[0] + " " + count + "건")


if __name__=='__main__':

	#create_user(sys.argv[1])
	check_request()
	check_user()
	check_retire()
	check_retire_deal()