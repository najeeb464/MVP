from django.db import models

# Create your models here.
status_choices=[('0',"MAIN"),("1","SUB")]
class Section(models.Model):
    title               =models.CharField(max_length=250)
    parent              =models.ForeignKey('self',null=True,blank=True,related_name="section_parent",on_delete=models.SET_NULL)
    status              =models.CharField(choices=status_choices,max_length=120,default=status_choices[0][0],null=True,blank=True)
    submenu_status      =models.BooleanField(default=False)
    level               =models.IntegerField(default=0)
    created_at          =models.DateTimeField(auto_now_add=True)
    updated_at          =models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    def display_status(self):
        if self.status=="0":
            return status_choices[0][1]
        else:
            return status_choices[1][1]