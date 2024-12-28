from django.shortcuts import render
from django.shortcuts import redirect
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from .models import stuff_work
from .models import faq_logging
from .models import app
from .forms import WorkCreate
from .forms import FaqCreate
from .forms import CulcMainFeederInput
from .forms import EarthCableCulcInput
from .forms import CulcConduitSizeInput
from .ProjectProgress import get_progress
from . import CulcVoltageDrop
from . import CulcEarthSize
from . import CulcConduitSize
import datetime



def index(request):
    return render(request, 'cute_paccho/index.html')

def CompanyProfIndex(request):
    return render(request, 'cute_paccho/CompanyProfIndex.html')

def Recruitment(request):
    return render(request, 'cute_paccho/Recruitment.html')

def PrivacyPolicy(request):
    return render(request, 'cute_paccho/PrivacyPolicy.html')

def SiteMap(request):
    return render(request, 'cute_paccho/SiteMap.html')

def AboutEleplan(request):
    return render(request, 'cute_paccho/AboutEleplan.html')

def CompanyData(request):
    return render(request, 'cute_paccho/CompanyData.html')

def EnvironmentalActivities(request):
    return render(request, 'cute_paccho/EnvironmentalActivities.html')


@login_required(login_url='/admin/login/?next=/admin/')
def WorkRead(request):
    data = stuff_work.objects.all()
    params = {
        'data': data,
    }
    return render(request, 'cute_paccho/MembersIndex.html', params)

@login_required(login_url='/admin/login/?next=/admin/')
def WorkAdd(request,page=1):
    params = {
        'form':WorkCreate(),
    }

    if request.method == 'POST':
        name = request.POST['name']
        last_update = request.POST['last_update']
        project_name = request.POST['project_name']
        detail_line = request.POST['detail_line']
        dead_line = request.POST['dead_line']
        check_done = 'False'
        add_list = stuff_work(name=name,last_update=last_update,project_name=project_name,detail_line=detail_line,
                            dead_line=dead_line,check_done=check_done)
        add_list.save()
        return redirect(to='/cute_paccho/MembersIndex')

    return render(request, 'cute_paccho/WorkAddWindow.html', params)

@login_required(login_url='/admin/login/?next=/admin/')
def WorkEdit(request,num):
    obj = stuff_work.objects.get(id=num)

    if request.method == 'POST':
        obj.name = request.POST['name']
        obj.last_update = request.POST['last_update']
        obj.project_name = request.POST['project_name']
        obj.detail_line = request.POST['detail_line']
        obj.dead_line = request.POST['dead_line']
        obj.check_done = 'check_done' in request.POST
        obj.save()
        return redirect(to = '/cute_paccho/MembersIndex')
    
    params = {
        'id': num,
        'form': WorkCreate(initial={
            'name': obj.name,
            'last_update': obj.last_update,
            'project_name': obj.project_name,
            'detail_line': obj.detail_line,
            'dead_line': obj.dead_line,
            'check_done': obj.check_done,
        }),
    }
    return render(request, 'cute_paccho/WorkEditWindow.html', params)

@login_required(login_url='/admin/login/?next=/admin/')
def WorkDelete(request,num):
    obj = stuff_work.objects.get(id=num)
    
    if request.method == 'POST':
        obj.delete()
        return redirect(to = '/cute_paccho/MembersIndex')
    
    params = {
        'id': num,
        'form': WorkCreate(initial={
            'name': obj.name,
            'last_update': obj.last_update,
            'project_name': obj.project_name,
            'detail_line': obj.detail_line,
            'dead_line': obj.dead_line,
            'check_done': obj.check_done,
        }),
    }
    return render(request, 'cute_paccho/WorkDeleteWindow.html', params)

@login_required(login_url='/admin/login/?next=/admin/')
def ProjectProgressIndex(request):
    data = get_progress(app)  # test.py の関数を呼び出す
    return render(request, 'cute_paccho/ProjectProgressIndex.html', {'data': data})

@login_required(login_url='/admin/login/?next=/admin/')
def ElecCulcIndex(request):
    return render(request, 'cute_paccho/ElecCulcIndex.html')

@login_required(login_url='/admin/login/?next=/admin/')
def CulcMainFeeder(request):

    form = CulcMainFeederInput()

    if request.method == 'POST':
        ElecSpec = request.POST['ElecSpec']
        ElecCapacity = int(request.POST['ElecCapacity'])
        FeederLength = int(request.POST['FeederLength'])

        Elements, Answers= CulcVoltageDrop.CulcVoltageDrop(ElecSpec,ElecCapacity,FeederLength)
        request.session['Elements'] = Elements
        request.session['Answers'] = Answers

        return redirect('CulcMainFeeder')
    else:
        Elements = request.session.get('Elements', [])
        Answers = request.session.get('Answers', [])

    return render(request, 'cute_paccho/CulcMainFeeder.html',{'form':form, 'Elements':Elements, 'Answers':Answers})

@login_required(login_url='/admin/login/?next=/admin/')
def EarthCableCulc(request):

    form = EarthCableCulcInput()

    if request.method == 'POST':
        CalculateTrip = int(request.POST['CalculateTrip'])

        DecideCalculateTrip, DecideCableSize = CulcEarthSize.earth_cable_culc(CalculateTrip)
        print(DecideCalculateTrip, DecideCableSize)
        request.session['DecideCalculateTrip'] = DecideCalculateTrip
        request.session['DecideCableSize'] = DecideCableSize
        request.session['CalculateTrip'] = CalculateTrip

        return redirect('CulcEarthCableSize')
    else:
        DecideCalculateTrip = request.session.get('DecideCalculateTrip', [])
        DecideCableSize = request.session.get('DecideCableSize', [])
        CalculateTrip = request.session.get('CalculateTrip', [])

    return render(request, 'cute_paccho/CulcEarthCableSize.html',{'form':form, 'CalculateTrip':CalculateTrip, 'DecideCalculateTrip':DecideCalculateTrip, 'DecideCableSize':DecideCableSize})

def FaqIndex(request):

    data = faq_logging.objects.all()
    params = {
        'data': data,
    }
    return render(request, 'cute_paccho/FaqIndex.html', params)


def FaqIndexAdd(request):
    if request.method == 'POST':
        form = FaqCreate(request.POST)

        if form.is_valid():
            InputDate = datetime.datetime.today()
            FaqTitle = form.cleaned_data['FaqTitle']
            CompanyName = form.cleaned_data['CompanyName']
            Name = form.cleaned_data['Name']
            TelephoneNumber = form.cleaned_data['TelephoneNumber']
            MailAddress = form.cleaned_data['MailAddress']
            Massage = form.cleaned_data['Massage']

            Record = faq_logging(FaqTitle=FaqTitle,CompanyName=CompanyName,Name=Name,
                                        TelephoneNumber=TelephoneNumber,MailAddress=MailAddress,
                                        InputDate=InputDate,Massage=Massage)
            Record.save()

            # メール本文を作成
            subject = 'お問い合わせフォームから送信'
            message = f"""
                入力日: {InputDate}
                問合せ内容: {FaqTitle}
                会社名: {CompanyName}
                お名前: {Name}
                電話番号: {TelephoneNumber}
                メールアドレス: {MailAddress}
                問合せ内容: {Massage}
            """
            # メールを送信
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, ['info@eleplan.jp'])

        # フォーム送信後にリダイレクトするURLを指定
        # return redirect('完了ページのURL')  
        return redirect(to='/cute_paccho/FaqMailComplete')

    params = {
        'form':FaqCreate(),
    }
    return render(request, 'cute_paccho/FaqIndex.html', params)


def FaqMailComplete(request):
    #data = faq_logging.objects.order_by('-InputDate').first()
    
    #FaqTitle = data.FaqTitle
    #CompanyName = data.CompanyName
    #Name = data.Name
    #TelephoneNumber = data.TelephoneNumber
    #MailAddress = data.MailAddress
    #InputDate = data.InputDate
    #Massage = data.Massage

    #params = {
        #'FaqTitle':FaqTitle,
        #'CompanyName':CompanyName,
        #'Name' :Name,
        #'TelephoneNumber': TelephoneNumber,
        #'MailAddress': MailAddress,
        #'InputDate': InputDate,
        #'Massage': Massage,
    #}
    return render(request, 'cute_paccho/FaqMailComplete.html')

@login_required(login_url='/admin/login/?next=/admin/')
def CableAdd(request):
    form = CulcConduitSizeInput()

    if request.method == 'POST':
        CableName = request.POST['CableName']
        CableNumber = int(request.POST['CableNumber'])

        MatchConSizeListNarrow, MatchConSizeListWide= CulcConduitSize.CulculationConduitSize(CableName, CableNumber)
        request.session['MatchConSizeListNarrow'] = MatchConSizeListNarrow
        request.session['MatchConSizeListWide'] = MatchConSizeListWide

        return redirect(to='CulcConduitSize')
    else:
        MatchConSizeListNarrow = request.session.get('MatchConSizeListNarrow', [])
        MatchConSizeListWide = request.session.get('MatchConSizeListWide', [])
    
    return render(request, 'cute_paccho/CulcConduitSize.html',{'form':form,'MatchConSizeListNarrow':MatchConSizeListNarrow,'MatchConSizeListWide':MatchConSizeListWide})
