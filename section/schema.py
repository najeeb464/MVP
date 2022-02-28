from random import choices
from turtle import title
import graphene
from graphene_django import DjangoObjectType,DjangoListField
from graphql import GraphQLError

from django.db import transaction
from section.utils import del_choices
from section.models import Section,status_choices



class SectionType(DjangoObjectType):
    class Meta:
        model=Section
        field=("id","title","parent","level")
        
class Query(graphene.ObjectType):
    all_section         =DjangoListField(SectionType)
    section_detail      =graphene.Field(SectionType,id=graphene.Int())
    subsection          =graphene.List(SectionType,id=graphene.Int())
    subsection_detail   =graphene.Field(SectionType,parent=graphene.Int(),id=graphene.Int())
    
    
    def resolve_all_section(root,info):
        return Section.objects.filter(parent__isnull=True)
    
    def resolve_section_detail(root,info,id=None):
        return Section.objects.get(id=id,parent__isnull=True)
    
    def resolve_subsection(root,info,id):
        return Section.objects.filter(parent__id=id)
    
    def resolve_subsection_detail(root,info,id,parent_id):
        return Section.objects.filter(id=id,parent__id=parent_id)
    
class CreateSection(graphene.Mutation):
    class Arguments:
        title=graphene.String(required=True)
    section=graphene.Field(SectionType)
    @classmethod
    def mutate(cls,root,info,title):
        section=Section(title=title)
        section.save()
        return CreateSection(section=section)
class SectionUpdate(graphene.Mutation):
    class Arguments:
        id=graphene.ID()
        title=graphene.String()
        parent=graphene.ID()
    section=graphene.Field(SectionType)
    
    @classmethod
    def mutate(cls,root,info,id,title,parent=None):
        try:
            sectionObj=Section.objects.get(id=id)
            sectionObj.title=title if title is not None else sectionObj.title
            if parent:
                parent_obj=Section.objects.get(id=parent)
                if parent==id:
                    raise Exception({"section":"you can not reference same  section with same submenu"})
                sectionObj.parent=parent_obj
               
            sectionObj.save()
        except Section.DoesNotExist:
            raise Exception({"section":"Invalid section "})
        except Exception as ex:
            raise Exception({str(ex)})
        if sectionObj.parent:
            sectionObj.status=status_choices[1][0]
            sectionObj.level=sectionObj.parent.level+1 if sectionObj.parent else 1
            sectionObj.submenu_status=Section.objects.filter(parent=parent).exists()
        else:
            sectionObj.status=status_choices[0][0]
            sectionObj.level=0
        
        sectionObj.save()
        return SectionUpdate(section=sectionObj)
    
class SubSectionCreate(graphene.Mutation):
    class Arguments:
        title=graphene.String(required=True)
        parent=graphene.ID(required=True)
        
    subsection=graphene.Field(SectionType)
    @classmethod
    def mutate(cls,root,info,title,parent):
        try:
            parentObj=Section.objects.get(id=parent)
        except Section.DoesNotExist:
            raise Exception({"section":"Invalid section "})
        sectionObj=Section(title=title,parent=parentObj)
        sectionObj.save()
        return SubSectionCreate(subsection=sectionObj)
    
class SubSectionUpdate(graphene.Mutation):
    class Arguments:
        id=graphene.ID()
        title=graphene.String()
        parent=graphene.ID()
    section=graphene.Field(SectionType)
    @classmethod
    def mutate(cls,root,info,id,title,parent=None):
        try:
            sectionObj=Section.objects.get(id=id)
            sectionObj.title=title if title is not None else sectionObj.title
            if parent:
                parent_obj=Section.objects.get(id=parent)
                if parent==id:
                    raise Exception({"section":"you can not reference same  section with same submenu"})
                sectionObj.parent=parent_obj
                
            sectionObj.save()
        except Section.DoesNotExist:
            raise Exception({"section":"Invalid section "})
        except Exception as ex:
            raise Exception(str(ex))
        if sectionObj.parent:
            sectionObj.status=status_choices[1][0]
            sectionObj.level=sectionObj.parent.level+1 if sectionObj.parent else 1
            sectionObj.submenu_status=Section.objects.filter(parent=parent).exists()
        else:
            sectionObj.status=status_choices[0][0]
            sectionObj.level=0
        sectionObj.save()
        return SectionUpdate(section=sectionObj)
    
class SectionDelete(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
    section = graphene.Field(SectionType)
    def mutate(self, info, id):
        try:
            section=Section.objects.get(id=id)
            section.delete()
        except:
            raise Exception({"section":"Invalid section "})
        return SectionDelete(section=section)

class SubSectionDelete(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        option=graphene.Int()
    section = graphene.Field(SectionType)
    def mutate(self, info, id,option):
        try:
            instance=Section.objects.get(id=id)
        except Section.DoesNotExist:
            raise Exception({"section":"Invalid section"})
        selected_option=option
        if selected_option is not None:
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
        return SectionDelete(section=instance)
    
    
class Mutation(graphene.ObjectType):
    create_section=CreateSection.Field()
    update_section=SectionUpdate.Field()
    delete_section=SectionDelete.Field()
    
    create_subsection=SubSectionCreate.Field()
    update_subsection=SubSectionUpdate.Field()
    delete_subsection=SubSectionDelete.Field()
schema=graphene.Schema(query=Query,mutation=Mutation)