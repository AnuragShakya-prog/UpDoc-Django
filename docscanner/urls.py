from django.urls import path
from . import views as doc_views


urlpatterns=[
    path("dashboard/",doc_views.dashboard,name="dashboard"),
    path("doc/<int:docId>/",doc_views.docView,name="doc_view"),
    path("docinfo/<int:docId>/",doc_views.docInfo,name="doc_info"),

]