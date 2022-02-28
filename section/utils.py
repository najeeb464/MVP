from rest_framework.exceptions import NotFound

del_choices=[(0,"DELETE_ALL_SUBSECTION"),(1,"DELETE_ME_MAKE_SUBSECTION_ORPHAN"),(2,"DELETE_ME_MAKE_MY_SUBSECTION_LEVELUP")]

class PublicAPIMixin:
    authentication_classes  =   []
    permission_classes      =   []
    
    def validate_id(self,id):
        try:
            check=int(id)
        except ValueError:
            raise NotFound("Invalid url pattern Please check url parameter")
        except:
            raise NotFound("Invalid url pattern Please check url parameter") 
        return id
    