from django.urls import path
from . import views

urlpatterns = [
    path("",views.index,name="home"),
    path("subbscription/",views.subscription,name="sub"),
    path("dashboard/",views.admin_home,name="dash")
]
