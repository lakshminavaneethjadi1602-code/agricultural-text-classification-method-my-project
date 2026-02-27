"""agricultural_text_classification_method URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url # pyright: ignore[reportMissingModuleSource]
from django.contrib import admin # pyright: ignore[reportMissingModuleSource]
from Remote_User import views as remoteuser # pyright: ignore[reportMissingImports]
from agricultural_text_classification_method import settings # pyright: ignore[reportMissingImports]
from Service_Provider import views as serviceprovider # pyright: ignore[reportMissingImports]
from django.conf.urls.static import static # pyright: ignore[reportMissingModuleSource]


urlpatterns = [
    url('admin/', admin.site.urls),
   url(r'^$', remoteuser.index, name="index"),
   url(r'^login/$', remoteuser.login, name="login"),
    url(r'^Register1/$', remoteuser.Register1, name="Register1"),
   url(r'^predict_text_classification/$', remoteuser.predict_text_classification, name="predict_text_classification"),
    url(r'^ViewYourProfile/$', remoteuser.ViewYourProfile, name="ViewYourProfile"),
   url(r'^serviceproviderlogin/$',serviceprovider.serviceproviderlogin, name="serviceproviderlogin"),
   url(r'View_Remote_Users/$',serviceprovider.View_Remote_Users,name="View_Remote_Users"),
   url(r'^charts/(?P<chart_type>\w+)', serviceprovider.charts,name="charts"),
  url(r'^charts1/(?P<chart_type>\w+)', serviceprovider.charts1, name="charts1"),
    url(r'^likeschart/(?P<like_chart>\w+)', serviceprovider.likeschart, name="likeschart"),
    url(r'^View_Prediction_Of_Agricultural_Text_Classification_Type_Ratio/$', serviceprovider.View_Prediction_Of_Agricultural_Text_Classification_Type_Ratio, name="View_Prediction_Of_Agricultural_Text_Classification_Type_Ratio"),
  url(r'^train_model/$', serviceprovider.train_model, name="train_model"),
    url(r'^View_Prediction_Of_Agricultural_Text_Classification_Type/$', serviceprovider.View_Prediction_Of_Agricultural_Text_Classification_Type, name="View_Prediction_Of_Agricultural_Text_Classification_Type"),
    url(r'^Download_Predicted_DataSets/$', serviceprovider.Download_Predicted_DataSets, name="Download_Predicted_DataSets"),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
