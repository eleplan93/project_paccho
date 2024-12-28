from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('CompanyProfIndex', views.CompanyProfIndex, name='CompanyProfIndex'),
    path('MembersIndex', views.WorkRead, name='MembersIndex'),
    path('WorkAddWindow/', views.WorkAdd, name='WorkAddWindow'),
    path('WorkAddWindow/<int:page>', views.WorkAdd, name='WorkAddPath'),
    path('WorkEditWindow/<int:num>', views.WorkEdit, name='WorkEditWindow'),
    path('WorkDeleteWindow/<int:num>', views.WorkDelete, name='WorkDeleteWindow'),
    path('ProjectProgressIndex/', views.ProjectProgressIndex, name='ProjectProgressIndex'),
    path('ElecCulcIndex/', views.ElecCulcIndex, name='ElecCulcIndex'),
    path('CulcMainFeeder/', views.CulcMainFeeder, name='CulcMainFeeder'),
    path('CulcEarthCableSize/', views.EarthCableCulc, name='CulcEarthCableSize'),
    path('AboutEleplan/', views.AboutEleplan, name='AboutEleplan'),
    path('CompanyData/', views.CompanyData, name='CompanyData'),
    path('EnvironmentalActivities/', views.EnvironmentalActivities, name='EnvironmentalActivities'),
    path('FaqIndex/', views.FaqIndexAdd, name='FaqIndexAdd'),
    path('Recruitment/', views.Recruitment, name='Recruitment'),
    path('PrivacyPolicy/', views.PrivacyPolicy, name='PrivacyPolicy'),
    path('SiteMap/', views.SiteMap, name='SiteMap'),
    path('CulcConduitSize/', views.CableAdd, name='CulcConduitSize'),
    path('FaqMailComplete/', views.FaqMailComplete, name='FaqMailComplete'),



]