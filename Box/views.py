from django.shortcuts import render
from rest_framework import generics, permissions
from .models import Box
from .serializers import BoxSerializer, BoxFullSerializer
from .permissions import IsStaffOrReadOnly, IsOwner
from django.db.models import F, ExpressionWrapper, fields

class BoxList(generics.ListAPIView):
    queryset = Box.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.user.is_staff:
            return BoxFullSerializer
        else:
            return BoxSerializer
        
    def get_queryset(self):
        queryset = Box.objects.all()

        length_more_than = self.request.query_params.get('length_more_than')
        length_less_than = self.request.query_params.get('length_less_than')
        width_more_than = self.request.query_params.get('width_more_than')
        width_less_than = self.request.query_params.get('width_less_than')
        height_more_than = self.request.query_params.get('height_more_than')
        height_less_than = self.request.query_params.get('height_less_than')
        area_more_than = self.request.query_params.get('area_more_than')
        area_less_than = self.request.query_params.get('area_less_than')
        volume_more_than = self.request.query_params.get('volume_more_than')
        volume_less_than = self.request.query_params.get('volume_less_than')
        created_by = self.request.query_params.get('created_by')
        created_before = self.request.query_params.get('created_before')
        created_after = self.request.query_params.get('created_after')

        if length_more_than:
            queryset = queryset.filter(length__gt=length_more_than)
        if length_less_than:
            queryset = queryset.filter(length__lt=length_less_than)
        if width_more_than:
            queryset = queryset.filter(width__gt=width_more_than)
        if width_less_than:
            queryset = queryset.filter(width__lt=width_less_than)
        if height_more_than:
            queryset = queryset.filter(height__gt=height_more_than)
        if height_less_than:
            queryset = queryset.filter(height__lt=height_less_than)

        if area_more_than:
            queryset = queryset.annotate(
                calculated_area=ExpressionWrapper(
                    2 * (F('length') * F('width') + F('length') * F('height') + F('height') * F('width')),
                    output_field=fields.FloatField()
                )
            ).filter(calculated_area__gt=area_more_than)

        if area_less_than:
            queryset = queryset.annotate(
                calculated_area=ExpressionWrapper(
                    2 * (F('length') * F('width') + F('length') * F('height') + F('height') * F('width')),
                    output_field=fields.FloatField()
                )
            ).filter(calculated_area__lt=area_less_than)

        if volume_more_than:
            queryset = queryset.annotate(
                calculated_volume=ExpressionWrapper(
                    (F('length') * F('width') * F('height')),
                    output_field=fields.FloatField()
                )
            ).filter(calculated_volume__gt=volume_more_than)

        if volume_less_than:
            queryset = queryset.annotate(
                calculated_volume=ExpressionWrapper(
                    (F('length') * F('width') * F('height')),
                    output_field=fields.FloatField()
                )
            ).filter(calculated_volume__lt=volume_less_than)   
        
        if created_by:
            queryset = queryset.filter(creator__username=created_by)
        if created_before:
            queryset = queryset.filter(created_at__lt=created_before)
        if created_after:
            queryset = queryset.filter(created_at__gt=created_after)

        return queryset

class AddBox(generics.ListCreateAPIView):
    queryset = Box.objects.all()
    serializer_class = BoxSerializer
    permission_classes = [permissions.IsAuthenticated, IsStaffOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

class BoxDetail(generics.RetrieveUpdateAPIView):
    queryset = Box.objects.all()
    serializer_class = BoxSerializer
    permission_classes = [permissions.IsAuthenticated, IsStaffOrReadOnly]

class MyBoxList(generics.ListAPIView):
    queryset = Box.objects.all()
    serializer_class = BoxFullSerializer
    permission_classes = [permissions.IsAuthenticated, IsStaffOrReadOnly]

    def get_queryset(self):
        # return Box.objects.filter(creator=self.request.user)   
        queryset = Box.objects.filter(creator=self.request.user)

        length_more_than = self.request.query_params.get('length_more_than')
        length_less_than = self.request.query_params.get('length_less_than')
        width_more_than = self.request.query_params.get('width_more_than')
        width_less_than = self.request.query_params.get('width_less_than')
        height_more_than = self.request.query_params.get('height_more_than')
        height_less_than = self.request.query_params.get('height_less_than')
        area_more_than = self.request.query_params.get('area_more_than')
        area_less_than = self.request.query_params.get('area_less_than')
        volume_more_than = self.request.query_params.get('volume_more_than')
        volume_less_than = self.request.query_params.get('volume_less_than')


        if length_more_than:
            queryset = queryset.filter(length__gt=length_more_than)
        if length_less_than:
            queryset = queryset.filter(length__lt=length_less_than)
        if width_more_than:
            queryset = queryset.filter(width__gt=width_more_than)
        if width_less_than:
            queryset = queryset.filter(width__lt=width_less_than)
        if height_more_than:
            queryset = queryset.filter(height__gt=height_more_than)
        if height_less_than:
            queryset = queryset.filter(height__lt=height_less_than)

        if area_more_than:
            queryset = queryset.annotate(
                calculated_area=ExpressionWrapper(
                    2 * (F('length') * F('width') + F('length') * F('height') + F('height') * F('width')),
                    output_field=fields.FloatField()
                )
            ).filter(calculated_area__gt=area_more_than)

        if area_less_than:
            queryset = queryset.annotate(
                calculated_area=ExpressionWrapper(
                    2 * (F('length') * F('width') + F('length') * F('height') + F('height') * F('width')),
                    output_field=fields.FloatField()
                )
            ).filter(calculated_area__lt=area_less_than)

        if volume_more_than:
            queryset = queryset.annotate(
                calculated_volume=ExpressionWrapper(
                    (F('length') * F('width') * F('height')),
                    output_field=fields.FloatField()
                )
            ).filter(calculated_volume__gt=volume_more_than)

        if volume_less_than:
            queryset = queryset.annotate(
                calculated_volume=ExpressionWrapper(
                    (F('length') * F('width') * F('height')),
                    output_field=fields.FloatField()
                )
            ).filter(calculated_volume__lt=volume_less_than)   

        return queryset
    
    
    
class BoxDelete(generics.RetrieveDestroyAPIView):
    queryset = Box.objects.all()
    serializer_class = BoxFullSerializer
    permission_classes = [permissions.IsAuthenticated, IsStaffOrReadOnly, IsOwner]

    def get_queryset(self):
        return Box.objects.filter(creator=self.request.user)