from django.shortcuts import render
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.authentication import BasicAuthentication 
from rest_framework.permissions import IsAuthenticated 
from django.contrib.auth.mixins import LoginRequiredMixin

from noteapi.models import Notes
from django.contrib.auth.models import User
from noteapi.serializers import NotesSerializer,UserSerializer
from rest_framework.decorators import api_view, authentication_classes , permission_classes

from django.db.models import Q

@api_view(['GET','POST',])
@authentication_classes([BasicAuthentication])
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
        
        notes = Notes.objects.all()

        notes_data = JSONParser().parse(request)

        notes_serializer = NotesSerializer(data=notes_data)

        if Notes.objects.filter(note=notes_data.get("note")).values():
            return JsonResponse({'message':'The note is already exist'},status=status.HTTP_400_BAD_REQUEST)
        # print(arr)
        # print(countries_data.get("name"))

        else:
            if notes_serializer.is_valid():
                notes_serializer.save(user = user)
                return JsonResponse(notes_serializer.data,status=status.HTTP_201_CREATED)
            return JsonResponse(notes_serializer.errors,status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET','PUT','DELETE','PATCH'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def notes_description(request,pk):
    try:
        user = request.user
        ''' Sort the notes list based on note id and check if that particular note 
        belongs to that user or not'''
        Notes.objects.get(Q(pk=pk),Q(user=user))

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

        '''check if user is already exist in system with same username or email'''
        if User.objects.filter(Q(username=username) | Q(email=email)):
            return JsonResponse({'message':'account already exist'},status=status.HTTP_400_BAD_REQUEST)
        elif user_serializer.is_valid():
            user = User.objects.create_user(username,email,password)
            user.save()
            return JsonResponse(user_serializer.data,status=status.HTTP_201_CREATED)
        return JsonResponse(user_serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        

