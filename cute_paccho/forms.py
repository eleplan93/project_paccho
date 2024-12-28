from django import forms
from django.core.validators import RegexValidator
from datetime import date
import gspread
from flask import render_template
from oauth2client.service_account import ServiceAccountCredentials
from .models import app


class WorkCreate(forms.Form):
    
    NAME_CHOICES = [
        ('富岡マキ', '富岡マキ'),
        ('川島直人', '川島直人'),
        ('小林夏乃', '小林夏乃'),
        ('伊藤巧', '伊藤巧'),
    ]

    name = forms.ChoiceField(
        required=True,
        choices=NAME_CHOICES, 
        widget=forms.Select
    )
    
    project_name = forms.CharField(
        required=True,
        widget=forms.TextInput
        )
    
    last_update = forms.DateField(
        input_formats = ['%y.%m.%d'],
        required=True,
        initial=date.today,
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    dead_line = forms.DateField(
        input_formats = ['%y.%m.%d'],
        required=True,
        initial=date.today,
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    detail_line = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={'placeholder': '200文字以内'})
        )

    check_done = forms.BooleanField(
        widget=forms.CheckboxInput,
        required=False
        )


class CulcMainFeederInput(forms.Form):
    
    #電気方式の選択
    SPEC_CHOICES = [
        ('単相3線式(200/100V)', '単相3線式(200/100V)'),
        ('三相3線式(200V)', '三相3線式(200V)'),
    ]

    ElecSpec = forms.ChoiceField(
        choices=SPEC_CHOICES,
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'}) 
    )
    
    #電気容量の入力
    ElecCapacity = forms.IntegerField(
        required=True,
        widget=forms.NumberInput(attrs={'class':'form-control'})
    )
    
    #幹線長入力 km換算
    FeederLength = forms.IntegerField(
        required=True,
        widget=forms.NumberInput(attrs={'class':'form-control'})
    )

class EarthCableCulcInput(forms.Form):
    #電気方式の選択
    SPEC_CHOICES = [
        ('20', '20'),
        ('30', '30'),
        ('40', '40'),
        ('50', '50'),
        ('60', '60'),
        ('75', '75'),
        ('100', '100'),
        ('125', '125'),
        ('150', '150'),
        ('175', '175'),
        ('200', '200'),
        ('225', '225'),
        ('250', '250'),
        ('300', '300'),
        ('350', '350'),
        ('400', '400'),
        ('500', '500'),
        ('600', '600'),
        ('800', '800'),
        ('1000', '1000'),
    ]

    CalculateTrip = forms.ChoiceField(
        choices=SPEC_CHOICES,
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'}) 
    )

class FaqCreate(forms.Form):

    NAME_CHOICES = [
        ('問合せ', '問合せ'),
        ('業務見積依頼', '業務見積依頼'),
        ('募集エントリー', '募集エントリー'),
        ('その他', 'その他'),
    ]

    FaqTitle = forms.ChoiceField(
        label='問合せ内容の選択', 
        choices=NAME_CHOICES, 
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
        )
    
    TelephoneNumber = forms.CharField(  # CharField を使用
        label='電話番号',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '090-1234-5678'}),
        validators=[RegexValidator(r'^\d{2,4}-\d{2,4}-\d{4}$', '電話番号の形式が正しくありません')]
    )
    
    MailAddress = forms.CharField(  # CharField を使用
        label='メールアドレス',
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'example@example.com'}),
        validators=[RegexValidator(regex=r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', message='有効なメールアドレスを入力してください。')]
    )

    Massage = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={'placeholder': '200文字以内'})
        )
    
    Name = forms.CharField(  # CharField を使用
        label='名前',
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        )
    
    CompanyName = forms.CharField(  # CharField を使用
        label='会社名',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        )

def get_spredsheet_list(app):
    with app.app_context():

        #Googleスプレッドシートへの認証情報
        scope = ['https://spreadsheets.google.com/feeds',
                    'https://www.googleapis.com/auth/drive']
        credentials = ServiceAccountCredentials.from_json_keyfile_name('mystical-magnet-443807-q4-64e4c79c960c.json', scope)

        gc = gspread.authorize(credentials)

        # スプレッドシートを開く
        spreadsheet = gc.open_by_key('1CigEfuCvnvkeditOI3cIf1RhL5fkPZ-1nfq5JyzDoDE')
        AboutInput = spreadsheet.worksheet('InputReferData')

        # データを取得
        input_cable_list = AboutInput.get_all_values()

        return input_cable_list
    
@app.route('/')
def index_three():
    data = get_spredsheet_list()
    return render_template('cute_paccho/CulcConduitSize.html', data=data)
    

class CulcConduitSizeInput(forms.Form):
    #電気方式の選択
    input_cable_lists = get_spredsheet_list(app)

    CableName = forms.ChoiceField(
        choices=input_cable_lists,
        required=True,
        widget=forms.Select() 
    )

    CableNumber =forms.IntegerField(
        required=True,
        widget=forms.NumberInput
    )

