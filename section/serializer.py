from rest_framework import serializers
from section.models import Section,status_choices

class SectionSerializer(serializers.ModelSerializer):
    submenu_count   =serializers.SerializerMethodField()
    status          =serializers.CharField(label="status",read_only=True,source='display_status')

    def get_submenu_count(self,obj):
        qs=Section.objects.filter(parent=obj)
        return qs.count()
    
    class Meta:
        model=Section
        fields=["id","title","parent","status","submenu_status","submenu_count","level"]
        read_only_fields=("id","status","submenu_status")
        
    def __init__(self, instance=None, *args, **kwargs):
        super().__init__(instance=instance,*args, **kwargs)
        request = self.context.get('request')
        if request and (request.method == 'POST' or request.method == 'PATCH' or request.method == 'PUT'):
            self.Meta.depth = 0
        else:
            self.Meta.depth = 1
        if instance and hasattr(instance,"pk"):
            self.fields["parent"].read_only=False
            self.fields["parent"].required=False
        else:
            self.fields["parent"].read_only=True
       
            
    def create(self, validated_data):
        return super().create(validated_data)
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
    
    def validate(self, attrs):
        if self.instance and hasattr(self.instance,"pk"):
            parent=attrs.get("parent",None)
            if parent and parent.id==self.instance.id:
                raise serializers.ValidationError({"parent":"you can not reference same  section with same submenu"})
        return super().validate(attrs)
    
    
    def save(self,*args,**kwargs):
        instance=super().save(*args,**kwargs)
        if instance.parent is None:
            instance.status=status_choices[0][0]
            instance.level=0
        else:
            instance.status=status_choices[1][0]
            instance.level=instance.parent.level+1
        instance.submenu_status=Section.objects.filter(parent=instance).exists()
        instance.save()
        return instance

class SubSectionSerializer(serializers.ModelSerializer):
    submenu_count=serializers.SerializerMethodField()
    def get_submenu_count(self,obj):
        qs=Section.objects.filter(parent=obj)
        return qs.count()
    class Meta:
        model=Section
        fields=["id","title","parent","status","level","submenu_count"]
        extra_kwargs={
                "parent":{"required":False},
                "status":{"required":False},
                }
    def validate(self,attrs):
        parent=attrs.get("parent",None)
        if self.instance is None and hasattr(self.instance,"pk") ==False:
            if parent:
                pass
            else:
                menu_id = self.context['request'].parser_context['kwargs']['menu_id']
                try:
                    sectionObj=Section.objects.get(id=menu_id)
                    attrs["parent"]=sectionObj
                except Section.DoesNotExist:
                    raise serializers.ValidationError({"parent":"Invalid parent choice"})
        else:
            if parent and parent.id==self.instance.id:
                raise serializers.ValidationError({"parent":"you can not reference same  section with same submenu"})
        return super().validate(attrs)
    
    def __init__(self, instance=None, *args, **kwargs):
        super().__init__(instance=instance,*args, **kwargs)
        request = self.context.get('request')
        if request and (request.method == 'POST' or request.method == 'PUT'):
            self.Meta.depth = 0
        else:
            self.Meta.depth = 1
    def save(self,*args,**kwargs):
        instance=super().save(*args,**kwargs)
        if instance.parent is None:
            instance.status=status_choices[0][0]
            instance.level=0
        else:
            instance.status=status_choices[1][0]
            instance.level=instance.parent.level+1
        instance.submenu_status=Section.objects.filter(parent=instance).exists()
        instance.save()
        return instance

