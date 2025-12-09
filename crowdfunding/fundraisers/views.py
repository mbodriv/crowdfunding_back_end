from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.http import Http404
from .models import Fundraiser, Pledge, BookingTime
from .serializers import FundraiserSerializer, PledgeSerializer, FundraiserDetailSerializer, BookingTimeSerializer
from .permissions import IsOwnerOrReadOnly, IsMenteeOrReadOnly, IsBookingOwnerOrReadOnly

class FundraiserList(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    def get(self,request):
        fundraisers = Fundraiser.objects.all()
        serializer = FundraiserSerializer(fundraisers, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = FundraiserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED)
        return Response(
                serializer.errors,
                status = status.HTTP_400_BAD_REQUEST
            )

class FundraiserDetail (APIView):
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly]
        
    def get_object(self,pk):
        try:
            fundraiser = Fundraiser.objects.get(pk=pk)
            self.check_object_permissions(self.request, fundraiser)
            return fundraiser
        except Fundraiser.DoesNotExist:
            raise Http404
            
    def get(self,request, pk):
            fundraiser = self.get_object(pk)
            serializer = FundraiserDetailSerializer(fundraiser)
            return Response(serializer.data)
    
    def put(self, request, pk):
        fundraiser = self.get_object(pk)
        serializer = FundraiserDetailSerializer(
            instance = fundraiser,
            data = request.data,
            partial = True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(
            serializer.errors,
            status = status.HTTP_400_BAD_REQUEST
        )
    
    def delete(self, request, pk):
        fundraiser = self.get_object(pk)
        fundraiser.is_active = False
        fundraiser.save()
        return Response(
            {"detail": "Profile deactivated successfully"},
            status = status.HTTP_200_OK
        )
    
class PledgeList(APIView):
    permission_classes = [permissions.IsAuthenticated, IsMenteeOrReadOnly]

    def get(self, request):
        pledges = Pledge.objects.all()
        serializer = PledgeSerializer(pledges, many=True)
        return Response(serializer.data)

    def post(self, request):
       serializer = PledgeSerializer(data=request.data)
       if serializer.is_valid():
           serializer.save(mentee=request.user)
           return Response(
               serializer.data,
               status=status.HTTP_201_CREATED
           )
       return Response(
           serializer.errors,
           status=status.HTTP_400_BAD_REQUEST
       )
    
class PledgeDetail(APIView):
    permission_classes = [permissions.IsAuthenticated, IsMenteeOrReadOnly]
        
    def get_object(self,pk):
        try:
            pledges = Pledge.objects.get(pk=pk)
            self.check_object_permissions(self.request, pledges)
            return pledges
        except Pledge.DoesNotExist:
            raise Http404
            
    def get(self,request, pk):
            pledges = self.get_object(pk)
            serializer = PledgeSerializer(pledges)
            return Response(serializer.data)
    
    def put(self, request, pk):
        pledges = self.get_object(pk)
        serializer = PledgeSerializer(
            instance = pledges,
            data = request.data,
            partial = True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(
            serializer.errors,
            status = status.HTTP_400_BAD_REQUEST
        )
class BookingTimeList(APIView):
    
    permission_classes = [permissions.IsAuthenticated, IsBookingOwnerOrReadOnly]
    
    def get(self, request):
        booking_time = BookingTime.objects.all()
        serializer = BookingTimeSerializer(booking_time, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = BookingTimeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class BookingTimeDetail(APIView):

    permission_classes = [permissions.IsAuthenticated, IsBookingOwnerOrReadOnly]

    def get_object(self,pk):
        try:
            booking_time=BookingTime.objects.get(pk=pk)
            self.check_object_permissions(self.request, booking_time)
            return booking_time
        except BookingTime.DoesNotExist:
            raise Http404
    
    def get (self, request, pk):
        booking_time=self.get_object(pk)
        serializer = BookingTimeSerializer(booking_time)
        return Response(serializer.data)
    
    def put(self, request, pk):
        booking_time=self.get_object(pk)
        serializer = BookingTimeSerializer(
            instance = booking_time,
            data = request.data,
            partial = True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    