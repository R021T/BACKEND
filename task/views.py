from rest_framework import status
from rest_framework.views import APIView,Response
from rest_framework.permissions import IsAuthenticated
from .models import User,task_table
from .serializers import UserSerializer,TaskSerializer
from datetime import datetime
from django.contrib.auth import authenticate,login,logout

# Create your views here.
class loginapi(APIView):
    
    def get(self,request):
        if request.user.is_authenticated:
            return Response({'response':'Already logged in'},status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'response':'Enter username and password'},status=status.HTTP_200_OK)
    
    def post(self,request):
        if request.user.is_authenticated:
            return Response({'response':'Already logged in'},status=status.HTTP_401_UNAUTHORIZED)
        else:
            username=request.data.get('username')
            password=request.data.get('password')
            user=authenticate(request,username=username,password=password)
            if user is not None:
                login(request,user)
                return Response({'response':'Logged in successfully'},status=status.HTTP_200_OK)
            else:
                return Response({'response':'Invalid credentials'},status=status.HTTP_401_UNAUTHORIZED)
        
class signupapi(APIView):

    def get(self,request):
        if request.user.is_authenticated:
            return Response({'response':'Already logged in'},status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'response':'Enter first_name, last_name, username and password'},status=status.HTTP_200_OK)
    
    def post(self,request):
        if request.user.is_authenticated:
            return Response({'response':'Already logged in'},status=status.HTTP_401_UNAUTHORIZED)
        else:
            serialized_data = UserSerializer(data=request.data)
            if serialized_data.is_valid():
                serialized_data.save()
                return Response({'response':'Account created successfully'},status=status.HTTP_200_OK)
            else:
                return Response({'response':serialized_data.errors},status=status.HTTP_204_NO_CONTENT)
        
class logoutapi(APIView):

    def get(self,request):
        if request.user.is_authenticated:
            logout(request)
            return Response({'response':'Logged out successfully'},status=status.HTTP_200_OK)
        else:
            return Response({'response':'Not logged in'},status=status.HTTP_401_UNAUTHORIZED)

class taskapi(APIView):

    def get(self,request):
        if request.user.is_authenticated:
            display=task_table.objects.filter(username__username=request.user.username)
            response=TaskSerializer(display,many=True).data
            return Response({'response':response},status=status.HTTP_200_OK)
        else:
            return Response({'response':'Not logged in'},status=status.HTTP_401_UNAUTHORIZED)

    def post(self,request):
        if request.user.is_authenticated:
            task=request.data.get('task')
            deadline=request.data.get('deadline')
            if(task is None or deadline is None):
                return Response({'response':'Invalid task or deadline'},status=status.HTTP_204_NO_CONTENT)
            else:
                name=User.objects.get(username=request.user.username)
                task_table.objects.create(username=name,task=task,deadline=deadline)
                return Response({'response':'Task added successfully'},status=status.HTTP_200_OK)
        else:
            return Response({'response':'Not logged in'},status=status.HTTP_401_UNAUTHORIZED)
        
    def put(self,request):
        if request.user.is_authenticated:
            id=0
            id=request.data.get('id')
            task=request.data.get('task')
            deadline=request.data.get('deadline')
            if(id==0 or (task is None and deadline is None)):
                return Response({'response':'Invalid ID, task or deadline'},status=status.HTTP_204_NO_CONTENT)
            else:
                database=task_table.objects.filter(id=id)
                if(database is None):
                    return Response({'response':'Task not found'},status=status.HTTP_404_NOT_FOUND)
                else:
                    if(task is None):
                        update=task_table.objects.get(id=id)
                        database=task_table(id=id,task=update.task,deadline=deadline)
                        database.save()
                        return Response({'response':'Deadline updated successfully'},status=status.HTTP_200_OK)
                    else:
                        update=task_table.objects.get(id=id)
                        database=task_table(id=id,task=task,deadline=update.deadline)
                        database.save()
                        return Response({'response':'Task updated successfully'},status=status.HTTP_200_OK)
        else:
            return Response({'response':'Not logged in'},status=status.HTTP_401_UNAUTHORIZED)
        
    def delete(self,request):
        if request.user.is_authenticated:
            id=0
            id=request.data.get('id')
            if(id==0):
                return Response({'response':'Invalid ID'},status=status.HTTP_204_NO_CONTENT)
            else:
                database=task_table.objects.filter(id=id)
                if(database is None):
                    return Response({'response':'Task not found'},status=status.HTTP_404_NOT_FOUND)
                else:
                    database.delete()
                    return Response({'response':'Task deleted successfully'},status=status.HTTP_200_OK)
        else:
            return Response({'response':'Not logged in'},status=status.HTTP_401_UNAUTHORIZED)

class expiredapi(APIView):

    def get(self,request):
        if request.user.is_authenticated:
            name=User.objects.get(username=request.user.username)
            display=task_table.objects.filter(deadline__lt=datetime.now(),username=name)
            response=TaskSerializer(display,many=True).data
            if(response is None):
                return Response({'response':'No expired tasks'},status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({'response':response},status=status.HTTP_200_OK)
        else:
            return Response({'response':'Not logged in'},status=status.HTTP_401_UNAUTHORIZED)
