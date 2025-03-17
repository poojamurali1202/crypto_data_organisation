from django.urls import path, include
from .views import OrganizationList,CryptoPriceList,CreateOrganisation,schedule_task,UserSignup,UpdateOrganisation,DeleteOrganisation

from rest_framework_simplejwt.views import (
    TokenObtainPairView,

)

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data['id'] = self.user.id  # Use 'id' instead of 'user_id'
        return data

from rest_framework_simplejwt.views import TokenObtainPairView


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


from rest_framework import permissions
from drf_yasg.views import get_schema_view

from drf_yasg import openapi

from drf_yasg.generators import OpenAPISchemaGenerator

schema_view = get_schema_view(

    openapi.Info(
        title="Bitcoin",
        default_version='v1',
        hideHostname=False,
        description="TEst",
    ),
    public=True,
    permission_classes=[permissions.AllowAny],

)



urlpatterns = [
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0),
         name='schema-swagger-ui'),
    # path("crypto_prices/",OrganizationList.as_view()),
    # path("organisations/",CryptoPriceList.as_view()),
    path("create_organisation/",CreateOrganisation.as_view()),
    path("update_organisation_name/",UpdateOrganisation.as_view()),
    path("delete_organisation/",DeleteOrganisation.as_view()),
    path("view_crypto_prices/",CryptoPriceList.as_view()),
    path("schedule/",schedule_task),
    path("user_signup/",UserSignup.as_view()),
    path('jwt_token/',
         include([
             path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair')]
         ))
]
