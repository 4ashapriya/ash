from rest_framework.authtoken.views import obtain_auth_token
from django.conf.urls import url
from django.urls import path
from .views import DeleteAPIView, UpdateAPIView, PermissionAPIView, RegisterAPIView, BulkInsertView
# swagger
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='Swagger API')

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="API Documentation",
      default_version='v1',
      description="User Details",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


urlpatterns = [

	path('register',RegisterAPIView.as_view(),name = 'register'),

   path('login/',obtain_auth_token,name ='login'),

   path('permission',PermissionAPIView.as_view(),name = 'permission'),
   path('update',UpdateAPIView.as_view(),name = 'update'),

   # path('reg',views.Registerupdate.as_view(),name='reg'),

   path('delete/<pk>',DeleteAPIView.as_view(),name = 'delete'),
   path('employee/', BulkInsertView.as_view(), name='employee'),
   path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]

# from django.contrib.auth import views
# from django.urls import path
# from .views import EmployeeUploadView
