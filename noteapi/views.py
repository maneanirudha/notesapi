from django.shortcuts import render
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.authentication import BasicAuthentication 
from rest_framework.authentication import TokenAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated 
from django.contrib.auth.mixins import LoginRequiredMixin

from django.core.mail import send_mail
from django.conf import settings

from noteapi.models import Notes,Useractivation,User_subscription_details,Subscriptionplans
from django.contrib.auth.models import User
from noteapi.serializers import NotesSerializer,UserSerializer,UserValidation,Subscription_details
from rest_framework.decorators import api_view, authentication_classes , permission_classes

from django.db.models import Q
from datetime import date
import random

@api_view(['GET','POST',])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def note_list(request):
    if request.method == 'GET':

        # if request.user.IsAuthenticated:
        user = request.user
        notes = Notes.objects.filter(user = user)

        # countries = Countries.objects.all()
        # name = request.GET.get('name',None)
        # if name is not None:
        #     countries = countries.filter(name__icontains=name)

        

        notes_serializer = NotesSerializer(notes,many=True)
        return JsonResponse(notes_serializer.data,safe=False)

    elif request.method == 'POST':


        user = request.user
        user_data = JSONParser().parse(request)

        if User.objects.filter(Q(username=user)):
  
            getdata = Useractivation.objects.filter(user=user).values()
            # print(getdata)

            for isactive in getdata:
                is_active_status = isactive['is_active']
                # print(is_active_status)
            
            if is_active_status == True:

                user = request.user
                
                notes = Notes.objects.all()

                # notes_data = JSONParser().parse(request)

                notes_serializer = NotesSerializer(data=user_data)

                getsubid = User_subscription_details.objects.filter(user=user).values()

                for subid in getsubid:
                    sub_id = subid['sub']
                    subcription_date = subid['subcription_date']
                
                # print(sub_id)
                # print(subcription_date)

                
                today = date.today()

                # Calculates date difference between todays date and subscription date

                date_diff = (today-subcription_date).days

                if sub_id==1:
                    user_notes = Notes.objects.filter(user=user).values()
                    current_note_count = len(user_notes)

                    if current_note_count == 5:

                        return JsonResponse({'message':'you have only 5 notes limit to add, please subscribe for paid plans'})

                    elif date_diff>30:

                        return JsonResponse({'message':'your free trial is expired!'})

                    else:
                        if Notes.objects.filter(note=user_data.get("note")).values():
                            return JsonResponse({'message':'The note is already exist'},status=status.HTTP_400_BAD_REQUEST)
                    # print(arr)
                    # print(countries_data.get("name"))

                        else:
                            if notes_serializer.is_valid():
                                notes_serializer.save(user = user)
                                return JsonResponse(notes_serializer.data,status=status.HTTP_201_CREATED)
                        return JsonResponse(notes_serializer.errors,status=status.HTTP_400_BAD_REQUEST)

            else:
                return JsonResponse({'message':'please verify your email'})
        else:
            return JsonResponse({'message':'User not Found!'})


@api_view(['GET','PUT','DELETE','PATCH'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def notes_description(request,pk):
    try:
        user = request.user
        ''' Sort the notes list based on note id and check if that particular note 
        belongs to that user or not'''
        notes = Notes.objects.get(Q(pk=pk),Q(user=user))
        # notes = Notes.objects.all()

    except Notes.DoesNotExist:
        return JsonResponse({'message':'This note does not exist in your list'},status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        notes_serializer = NotesSerializer(notes)
        return JsonResponse(notes_serializer.data)

    elif request.method == 'PUT':
        notes_data = JSONParser().parse(request)
        notes_serializer = NotesSerializer(notes,data=notes_data)
        if notes_serializer.is_valid():
            notes_serializer.save(user=user)
            return JsonResponse(notes_serializer.data)
        return JsonResponse(notes_serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PATCH':
        notes_data = JSONParser().parse(request)
        notes_serializer = NotesSerializer(notes,data=notes_data)
        if notes_serializer.is_valid():
            notes_serializer.save()
            return JsonResponse(notes_serializer.data)
        return JsonResponse(notes_serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        notes.delete()
        return JsonResponse({'message':'Note was deleted successfully!'},status=status.HTTP_204_NO_CONTENT)


@api_view(['POST',])
def CreateUser(request):
    if request.method == 'POST':
        # temp = request.POST.get("username")
        user_data = JSONParser().parse(request)
        user_serializer = UserSerializer(data=user_data)
        # temp = request.POST['username']
        username = user_data.get("username")
        email = user_data.get("email")
        password = user_data.get("password")
        sub = user_data.get("sub_id")

        print(sub)

        # return JsonResponse({'messgae':'fetched succesfully'})
        '''check if user is already exist in system with same username or email'''
        if User.objects.filter(Q(username=username) | Q(email=email)):
            return JsonResponse({'message':'account already exist'},status=status.HTTP_400_BAD_REQUEST)
        elif user_serializer.is_valid():

            otp = random.randint(1111,9999)
            subject = "Notes app account verification code"
            message = f"Your verification code is {otp}"
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [email]
            
            res = send_mail(subject,message,email_from,recipient_list)
            # Checks email config is correct or not and then creates a user
            if res==1:
                user = User.objects.create_user(username,email,password)
                user.save()
                user_obj = UserValidation(data={'otp': otp,'user_id':user})
                user_obj.is_valid()
                user_obj.save(user = user)

                get_user_id = User.objects.filter(Q(username=username)).values()

                for user_id in get_user_id:
                    new_user_id = user_id['id']
            

                print(new_user_id)

                sub_date = date.today()
                sub_serializer = Subscription_details(data={'subcription_date':sub_date,'sub':sub,'user_id':new_user_id})
                sub_serializer.is_valid()
                print(sub_serializer)
                print(sub_serializer.is_valid())

                sub_serializer.save(user=user)

                # print(otp)
                # print(res)
            return JsonResponse(user_serializer.data,status=status.HTTP_201_CREATED)
        return JsonResponse(user_serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
        
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['PATCH',])
def VerifyUser(request):
    if request.method == 'PATCH':
        
        user = request.user
        user_data = JSONParser().parse(request)

        email = user_data.get("email")
        otp = user_data.get("otp")
        db_otp = ''
        print(otp)
        if User.objects.filter(Q(email=email)):

            # print(User.objects.filter(Q(email=email)))
            
            temp = Useractivation.objects.filter(user=user).values()
            getdata = Useractivation.objects.get(Q(user=user))
            for temp in temp:
                db_otp = temp['otp']
            
            # print(db_otp)

            if otp == db_otp:
                user_active = UserValidation(getdata,data={'otp':otp,'is_active':True})
                user_active.is_valid()
                user_active.save(user=user)
                return JsonResponse({'message':'User verified successfully'},status=status.HTTP_200_OK)

            else:
                return JsonResponse({'message':'Verification code incorrect'},status=status.HTTP_200_OK)
                
        else:
            return JsonResponse({'message':'User Not Found'})

@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['GET',])
def Test(request):
    if request.method == 'GET':


        user = request.user
        # user_data = JSONParser().parse(request)

        if User_subscription_details.objects.filter(Q(user=user)):
  
            getsubid = User_subscription_details.objects.filter(user=user).values()

            for subid in getsubid:
                sub_id = subid['sub_id']
            
            print(sub_id)



            return JsonResponse({'message':'data found'})

            