from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from .models import CustomUser
from .serializers import CustomUserSerializer

class CustomUserList(APIView):
    permission_classes = [permissions.IsAuthenticated]

    #override method-level permissions
    def get_permissions(self):
        if self.request.method == 'POST':
            return []  #allow anyone to create a user
        return [permissions.IsAuthenticated()]  #all other methods require auth

    def get(self, request):
        user = request.user
    #everyone authenticated can see mentors
        mentors = CustomUser.objects.filter(user_type="mentor")
    #everyone can see themselves
        self_user = CustomUser.objects.filter(id=user.id)
    #Mentors can only see mentee who pledged to them
        if user.user_type == "mentor":
            mentees = CustomUser.objects.filter(pledges__fundraiser__owner=user)
        else:
            mentees = CustomUser.objects.none()
    #return users of any of the following group. We use distinct to avoid duplications.    
        users = (mentors | self_user | mentees).distinct()
        serializer = CustomUserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, _ = Token.objects.get_or_create(user=user)
            return Response(
                {
                    "user": CustomUserSerializer(user).data,
                    "token": token.key
                },
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

class CustomUserDetail(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get_object(self, pk):
        try:
            return CustomUser.objects.get(pk=pk)
        except CustomUser.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        user = self.get_object(pk)
     #Defaulting has_pledged to False
        has_pledged = False

    #Determining if the requesting mentor can see if this mentee pledged
        if request.user.user_type == "mentor" and user.user_type == "mentee":
            has_pledged = user.pledges.filter(fundraiser__owner=request.user).exists()

    #Mentee can only view themselves and mentors
        if request.user.user_type == "mentee":
            if user != request.user and user.user_type != "mentor":
                return Response(
                    {"detail": "You're not allowed to view other users."},
                    status=status.HTTP_403_FORBIDDEN
                )

    #Mentor can view any mentor, and only mentees who pledged to them
        if request.user.user_type == "mentor":
            if user.user_type == "mentee" and not has_pledged:
                return Response(
                    {"detail": "You cannot view this mentee."},
                    status=status.HTTP_403_FORBIDDEN
                )
        serializer = CustomUserSerializer(user)
        data = serializer.data
        data["has_pledged"] = has_pledged
        return Response(data)

class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)

        return Response({
            'token': token.key,
            'user_id': user.id,
            'email': user.email
        })
