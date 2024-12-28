from django.db import models
from flask import Flask

app = Flask(__name__)

# Create your models here.
class stuff_work(models.Model):
    name = models.CharField(max_length=100)
    last_update = models.DateField()
    project_name = models.CharField(max_length=100)
    detail_line = models.CharField(max_length=200)
    dead_line = models.DateField()
    check_done = models.BooleanField()

def __str__(self):
    return self.name + {self.last_update.strftime('%Y.%m.%d')} + self.project_name + self.detail_line + self.dead_line + str(self.check_done)


class faq_logging(models.Model):
    FaqTitle = models.CharField(max_length=10)
    CompanyName = models.CharField(max_length=20)
    Name = models.CharField(max_length=10)
    TelephoneNumber = models.CharField(max_length=15)
    MailAddress = models.CharField(max_length=30)
    InputDate = models.DateField(auto_now_add=True)
    Massage = models.CharField(max_length=200)

def __str__(self):
    return self.FaqTitle + self.Name + self.TelephoneNumber + self.MailAddoress + self.InputDate + self.Massage


class calc_conduit_size(models.Model):
    CulcSerial = models.CharField(max_length=10)
    CableName = models.CharField(max_length=10)
    CableNumber = models.CharField(max_length=10)


def __str__(self):
    return self.CableName + self.CableNumber
