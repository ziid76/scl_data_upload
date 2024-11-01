from django.db import models
from django.urls import reverse # Used to generate URLs by reversing the URL patterns
from django.contrib.auth.models import User
from datetime import datetime
from django.core.validators import RegexValidator

class Project(models.Model):
    """프로젝트 목록 목록"""
    name = models.CharField(max_length=200, help_text='프로젝트명 입력')
    yn = models.CharField(max_length=1, help_text='종료여부')
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    manager = models.ForeignKey(User, related_name='owner', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        """String for representing the Model object."""
        return self.name


class Company(models.Model):
    """소속회사 목록"""
    name = models.CharField(max_length=200, help_text='신규로 등록할 회사명 입력')
    code = models.CharField(max_length=4, help_text='신규로 등록할 회사코드(4자리) 입력')

    def __str__(self):
        """String for representing the Model object."""
        return self.name


class secUser(models.Model):

    NEW = "N"
    IN_PROGRESS = "P"
    DONE = "G"
    DROP = "D"

    S_CHOICES=(
        (NEW, "신규요청"),
        (IN_PROGRESS, "승인진행중"),
        (DONE, "승인완료"),
        (DROP, "반려")
    )
    """Model representing a book (but not a specific copy of a book)."""
    userid = models.CharField(max_length=30)
    name = models.CharField(max_length=30,null=True, blank=True)
    req_user = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True)
    lastname = models.CharField(max_length=30)
    firstname = models.CharField(max_length=30)
    usergrade = models.CharField(max_length=30)
    #phoneNumberRegex = RegexValidator(regex=r'^01([0|1|6|7|8|9]?)-?([0-9]{3,4})-?([0-9]{4})$')
    #phone = models.CharField(validators=[phoneNumberRegex], max_length=13, null=True, blank=True)
    phone = models.CharField(max_length=13, null=True, blank=True)
    Company = models.ForeignKey('Company', on_delete=models.SET_NULL, null=True)
    project = models.ForeignKey('Project', on_delete=models.SET_NULL, null=True, help_text='소속 프로젝트 선택')
    summary = models.TextField(max_length=5000, null=True, blank=True, help_text='Enter a brief description of the book')
    date_of_start = models.DateField('투입일자', null=True, blank=True)
    date_of_end = models.DateField('철수일자', null=True, blank=True)
    status = models.CharField(choices=S_CHOICES, default="N", max_length=1, blank=True)

    def __str__(self):
        """String for representing the Model object."""
        return str(self.id)

    def get_absolute_url(self):
        """Returns the url to access a detail record for this book."""
        return reverse('user_create_detail', args=[str(self.id)])

    def admin_request_user(self):
        u_ = Profile.objects.filter(user=self.req_user)
        rtn = ''

        try:
            rtn=u_[0].kor_name
        except:
            rtn = ''

        return rtn

    admin_request_user.short_description = '요청자'

class SecUserApprove(models.Model):
    """ 인원 투입 요청 승인자 목록"""
    user_req = models.ForeignKey('secUser', on_delete=models.SET_NULL, null=True, blank=True)
    seq = models.IntegerField(null=True, blank=True)
    stage = models.CharField(max_length=1, null=True, blank=True)
    final = models.CharField(max_length=1, null=True, blank=True)
    app_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='approve_list')
    approved = models.CharField(max_length=1, null=True, blank=True)
    approve_date = models.DateTimeField(null=True, blank=True)
    comment = models.TextField(max_length=1000, null=True, blank=True)

    def __str__(self):
        return str(self.id)


class UserTools(models.Model):
    """Model representing a specific copy of a book (i.e. that can be borrowed from the library)."""

    T_CHOICES=(
        ("V", "VDI"),
        ("D", "DB Safer"),
        ("S", "서버접근제어"),
        ("A", "NAS"),
        ("E", "기타")
    )

    user = models.ForeignKey('Profile', on_delete=models.SET_NULL, null=True)
    tools = models.CharField(choices=T_CHOICES, max_length=1, blank=True, null=True,)
    in_use = models.CharField(max_length=1, blank=True, null=True)
    info = models.CharField(max_length=500, blank=True, null=True)
    date_of_start = models.DateTimeField(null=True, blank=True)
    date_of_end = models.DateTimeField(null=True, blank=True)


class UserSign(models.Model):
    """각종 양식에 서약 결과를 기록하는 Table"""
    loginuser = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    doc_type = models.CharField(max_length=1)
    signdate = models.DateField(null=True, blank=True)


class Profile(models.Model):

    MANAGER = "M"
    PROJECT_OWNER = "P"
    GENERAL_USER = "G"

    P_CHOICES=(
        (MANAGER, "관리자"),
        (PROJECT_OWNER, "프로젝트담당자"),
        (GENERAL_USER, "일반사용자"),
    )

    NEW = "N"
    IN_PROGRESS = "P"
    DONE = "D"
    ON_DROP = "O"

    S_CHOICES=(
        (NEW, "투입 진행중"),
        (IN_PROGRESS, "투입"),
        (DONE, "철수"),
        (ON_DROP, "철수 진행중")
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    kor_name = models.CharField(max_length=15, blank=True)
    grade = models.CharField(max_length=15, blank=True)
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, blank=True)
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, blank=True)
    permission = models.CharField(choices=P_CHOICES, max_length=1, blank=True)
    req_date = models.DateField(null=True, blank=True)
    gen_date = models.DateField(null=True, blank=True)
    ret_date = models.DateField(null=True, blank=True)
    del_date = models.DateField(null=True, blank=True)
    status = models.CharField(choices=S_CHOICES, max_length=1, blank=True, null=True,)
    phone = models.CharField(max_length=13, null=True, blank=True)
    ip = models.CharField(max_length=15, null=True, blank=True)
    vdi_ip = models.CharField(max_length=15, null=True, blank=True)
    empID = models.CharField(max_length=20, null=True, blank=True)

    def count_i(self):
        cnt = SecUserApprove.objects.filter(app_user=self.user).filter(stage='Y').count()
        return cnt

    def count_o(self):
        cnt = UserRequestApprove.objects.filter(app_user=self.user).filter(stage='Y').count()
        return cnt

    def count_d(self):
        cnt = UserRetireApprove.objects.filter(app_user=self.user).filter(stage='Y').count()
        return cnt

    def count_r(self):
        cnt = UserRetire.objects.filter(status="N").filter(manager=self.user).count()
        return cnt

    def chk_sign(self):
        rtn = []
        chk = UserSign.objects.filter(loginuser=self.user)
        if chk:
            for i in chk:
                rtn.append(i.doc_type)
        return rtn


    def __str__(self):
        """String for representing the Model object."""
        return self.kor_name


class UserRequest(models.Model):

    NEW = "N"
    IN_PROGRESS = "P"
    DONE = "G"
    DROP = "D"

    S_CHOICES=(
        (NEW, "신규요청"),
        (IN_PROGRESS, "승인진행중"),
        (DONE, "승인완료"),
        (DROP, "반려")
    )

    req_user = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True)
    type = models.ForeignKey('UserRequestTypeMaster', on_delete=models.SET_NULL, null=True)
    ip_address = models.CharField(max_length=20, null=True, blank=True, help_text='Enter IP Address')
    memo = models.TextField(max_length=5000, null=True, blank=True, help_text='Memo')
    date_of_req = models.DateField('투입일자', null=True, blank=True)
    status = models.CharField(choices=S_CHOICES, default="N", max_length=1, blank=True)


class UserRequestApprove(models.Model):
    """ 인원 투입 요청 승인자 목록"""
    req_id = models.ForeignKey('UserRequest', on_delete=models.SET_NULL, null=True, blank=True)
    seq = models.IntegerField(null=True, blank=True)
    app_user = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, blank=True)
    stage = models.CharField(max_length=1, null=True, blank=True)
    final = models.CharField(max_length=1, null=True, blank=True)
    approved = models.CharField(max_length=1, null=True, blank=True)
    comment = models.TextField(max_length=1000, null=True, blank=True, help_text='Comment')
    approve_date = models.DateTimeField(null=True, blank=True)


class UserRequestTypeMaster(models.Model):
    """ 사용자 요청 마스터 """
    type = models.CharField(max_length=1)
    type_name = models.CharField(max_length=20, null=True, blank=True)
    type_desc = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(max_length=5000, null=True, blank=True, help_text='Description')
    status = models.CharField(max_length=1, null=True, blank=True)

    def __str__(self):
        return self.type_name


class UserRequestApproveMaster(models.Model):
    """ 사용자 요청 승인자 목록  """

    type = models.ForeignKey('UserRequestTypeMaster', on_delete=models.SET_NULL, null=True, blank=True)
    seq = models.IntegerField(null=True, blank=True)
    app_user = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, blank=True)


class CodeB(models.Model):

    code = models.CharField(max_length=10)
    title = models.CharField(max_length=50, null=True, blank=True)
    body = models.TextField(null=True, blank=True)
    return_page = models.CharField(max_length=100, null=True, blank=True)


class UserCode(models.Model):
    """ 사용자 철수활동 마스터 """
    code = models.CharField(max_length=1)
    name = models.CharField(max_length=50, null=True, blank=True)
    manager = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, blank=True)
    desc = models.CharField(max_length=200, null=True, blank=True)
    status = models.CharField(max_length=1, null=True, blank=True)

    def __str__(self):
        return self.name


class UserRetire(models.Model):
    """ 사용자 철수 처리결과  """

    code = models.ForeignKey('UserCode', on_delete=models.SET_NULL, null=True, blank=True)
    retiree = models.ForeignKey('Profile', on_delete=models.SET_NULL, null=True, blank=True)
    manager = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=1, default="N", null=True, blank=True)
    comment = models.TextField(max_length=1000, null=True, blank=True, help_text='Comment')
    date = models.DateTimeField(null=True, blank=True)


class UserRetireApprove(models.Model):
    """ 인원 철수요청 승인자 목록"""
    retiree = models.ForeignKey('Profile', on_delete=models.SET_NULL, null=True, blank=True)
    seq = models.IntegerField(null=True, blank=True)
    app_user = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, blank=True)
    stage = models.CharField(max_length=1, null=True, blank=True)
    final = models.CharField(max_length=1, null=True, blank=True)
    approved = models.CharField(max_length=1, null=True, blank=True)
    comment = models.TextField(max_length=1000, null=True, blank=True, help_text='Comment')
    approve_date = models.DateTimeField(null=True, blank=True)

class ExcelUploadRecord(models.Model):
    company = models.CharField(max_length=50)  # 회사 이름
    serial_number = models.AutoField(primary_key=True)  # 일련번호 (자동 증가)
    year_month = models.CharField(max_length=7)  # 'YYYY-MM' 형식
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)  # 업로드한 유저
    uploaded_at = models.DateTimeField(default=datetime.now)  # 업로드 시간
    num_record = models.IntegerField(null=True, blank=True)



    def __str__(self):
        return f"{self.company} - {self.year_month} - {self.uploaded_by.username}"

class ExcelUpload(models.Model):
    upload_record = models.ForeignKey(ExcelUploadRecord, on_delete=models.CASCADE)
    company = models.CharField(max_length=4)
    yyyymm = models.CharField(max_length=6)
    account = models.CharField(max_length=12)
    account_name = models.CharField(max_length=50)
    account_value = models.BigIntegerField()

    def __str__(self):
        return self.name
    
