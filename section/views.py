from wsgiref import validate
from django.shortcuts import render
# Create your views here.
from section.models import Section,status_choices
from section.serializer import SectionSerializer,SubSectionSerializer
from rest_framework.generics import ListAPIView ,CreateAPIView,RetrieveUpdateDestroyAPIView,ListCreateAPIView,DestroyAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework import status
from django.db import transaction
from section.utils import PublicAPIMixin,del_choices


class SectionListView(PublicAPIMixin,ListCreateAPIView):
    serializer_class = SectionSerializer
    def get_queryset(self, *args, **kwargs):
        return Section.objects.filter(parent__isnull=True)
 
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
    
class SectionDetailView(PublicAPIMixin,RetrieveUpdateDestroyAPIView):
    serializer_class    =SectionSerializer
    lookup_field        ='id'
    def get_queryset(self, *args, **kwargs):
        self.validate_id(self.kwargs.get("id"))
        return Section.objects.filter(id=self.kwargs.get("id"),parent__isnull=True)
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


class SubSectionListView(PublicAPIMixin,ListCreateAPIView):
    serializer_class = SubSectionSerializer
    def get_queryset(self, *args, **kwargs):
        menu_id=self.kwargs.get("menu_id",None)
        self.validate_id(menu_id)
        return Section.objects.filter(parent__id=menu_id)
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class SubSectionDetailView(PublicAPIMixin,RetrieveUpdateDestroyAPIView):
    serializer_class    =SubSectionSerializer
    lookup_field        ='id'
    
    def get_queryset(self, *args, **kwargs):
        _id=self.kwargs.get("id")
        _parentId=self.kwargs.get("menu_id")
        self.validate_id(_parentId)
        self.validate_id(_id)
        return Section.objects.filter(id=_id,parent__id=_parentId)
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)
    def perform_destroy(self, instance):
        selected_option=self.request.query_params.get("option",None)
        if selected_option is not None:
            self.validate_id(selected_option)
            with transaction.atomic():
                sectionObj=Section.objects.filter(parent=instance)
                if sectionObj.exists():
                    if selected_option == 0:
                        sectionObj.delete()
                    elif selected_option==1:
                        pass
                    elif selected_option==2:
                        if instance.parent is None:
                            for obj in sectionObj:
                                obj.parent=None
                                obj.level=0
                                obj.status=status_choices[0][0]
                                obj.save()
                        else:
                            for obj in sectionObj:
                                obj.parent=instance.parent
                                obj.level=instance.level
                                obj.status=status_choices[1][0]
                                obj.save()
                instance.delete()        
        else:
            instance.delete()
            
class DeleteSectionParentChoices(PublicAPIMixin,GenericAPIView):
    def get(self, request, *args, **kwargs):
        return Response(del_choices)