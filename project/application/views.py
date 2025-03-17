from rest_framework import viewsets
from rest_framework.generics import GenericAPIView,RetrieveAPIView,CreateAPIView
from rest_framework.response import Response
from .models import Organisation,CryptoPriceModel,AuthUser
from .serializers import OrganizationSerializer,CryptoPriceSerializer,CreateOrganisationSerializer,CreateUserSerializer,UserSignupSerializer
import uuid,random,string
from .tasks import fetch_crypto_prices
from django_celery_beat.models import PeriodicTask, IntervalSchedule
from rest_framework.permissions import IsAuthenticated, AllowAny

class UserSignup(CreateAPIView):
    """This class is to Register the User"""
    permission_classes = [AllowAny, ]
    serializer_class = CreateUserSerializer

    def post(self, request, *args, **kwargs):
        try:
            request.data["username"] = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
            request.data["org"] = request.data["org_id"]
            user = AuthUser.objects.filter(email=request.data["email"])
            if user:
                return Response({"status_code": 400,
                                 "message": "Email already registered Please Login",
                                 "error": None,
                                 "data": []})

            serializer = UserSignupSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"status_code": 200,
                                 "message": "User Registered Successfully",
                                 "error": None,
                                 "data": serializer.data})
            else:
                return Response({"status_code": 400,
                                 "message": "Unable to Registered User",
                                 "error": str(serializer.errors),
                                 "data": []})
        except Exception as error:
            return Response({"status_code": 500,
                             "message": "Unable to Registered User",
                             "error": str(error),
                             "data": []})

# This API is to create Organisation in Organisation Table
class CreateOrganisation(GenericAPIView):
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = CreateOrganisationSerializer

    def post(self,request,*args,**kwargs):
        org_id = "".join(random.choices(string.ascii_uppercase,k=10))
        print(org_id)
        data = {"id" : org_id,
        "name" : request.data["name"]}
        serializer = OrganizationSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            # fetch_crypto_prices.delay()
            return Response({
                "status_code":200,
                "data":serializer.data
            })

        else:
            return Response({
                "status_code": 400,
                "data": str(serializer.errors)
            })

# This API is to retrieve all the Organisation from organisation table
class OrganizationList(RetrieveAPIView):
    permission_classes = [IsAuthenticated, ]

    queryset = Organisation.objects.all()
    serializer_class = OrganizationSerializer

    def get(self, request, *args, **kwargs):
        queryset = Organisation.objects.all()
        serializer_class = OrganizationSerializer(instance=queryset, many=True)
        return Response({
            "status_code": 200,
            "data": serializer_class.data

        })

# This API is to retrieve all the Crypto Prices from organisation table
class CryptoPriceList(RetrieveAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = CryptoPriceSerializer

    def get(self, request, *args, **kwargs):
        print(request.user.org)
        queryset = CryptoPriceModel.objects.filter(org_id=request.user.org.id)
        serializer_class = CryptoPriceSerializer(queryset,many=True)
        return Response({
            "status_code": 200,
            "data": serializer_class.data

        })




def schedule_task(request):
    interval, _ = IntervalSchedule.objects.get_or_create(
        every=5,
        period=IntervalSchedule.MINUTES,
    )

    PeriodicTask.objects.create(
        interval=interval,
        name="my-schedule",
        task="application.tasks.fetch_crypto_prices",
    )

    return Response("Task scheduled!")

