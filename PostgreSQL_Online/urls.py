"""PostgreSQL_Online URL Configuration

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
from django.contrib import admin
from django.urls import path
from django.conf.urls import include,url
import schemas.views as sv
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/',include('django.contrib.auth.urls')),
    path('schemas/',sv.schemaView,name='schemas'),
    path('schemas/<int:schema_id>',sv.schemaOverview,name='overview'),
    path('schemas/query/<int:question_id>',sv.query,name='query'),
    path('signup/',sv.signUp,name='signup'),
    path('login/',sv.signIn,name='signin'),
    path('logout/',sv.logout_view,name='logout'),
    path('account/',sv.account,name='account'),
    path('status/<int:schema_id>',sv.status,name='status'),
    path('api/schemas/',sv.schema_api_view,name='schema_api'),
    path('api/schemas/<int:schema_id>',sv.schema_overview_api_view,name='schema_overview_api'),
    path('api/schemas/questions/<int:question_id>',sv.query_api_view,name='query_api'),
    path('api/login',sv.login_api_view,name='login_api'),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
