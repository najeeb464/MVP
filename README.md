# Environment SETUP
1)First create  virtual environment on your local system.You have two option either create using pip venv module using the listed link
https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/
or using anaconda virtual environment setup

2) Activate your environment 
3) install dependencies using 
    - pip3 install -r requirements.txt
4) python manage.py migrate
5) python manage.py runserver
6)python manage.py test
# Technologies used
- Django RestFramework
- Graphene-Django ( GraphQL functionality to  Django)

# Business Logic and Api Design
 For  section and subsection problem I only use one table Section ,this table has self reference ForeignKey .In case of Main section parent field is null and in case of  subsection parent field reference the section instance

 # Section APIS 
 ## List  and Create: GET | POST 
    -response of GET request show only those section whos parent field are null and they all are level 0 
    -creation of section only requires title fields
    -parent key in this case should be null so i make this read_only 
    -all other fields are either read_only or automatically calculated
###  URL     /section/
###  http://127.0.0.1:8080/section/

## Detail,Update and Destroy GET | PUT | PATCH | DELETE
 - In update of Section api ,end user can change title of the section or he/she can change  this section to  subsection.
 - if the user make the section to subsection this instance will not show in this detail api because in case of section apis i mantain i  check parent is null 
 -- when a user update section to subsection the backend  always check that the instance and parent should not be same 

### http://127.0.0.1:8080/section/1/detail/

# SUBSECTION APIS
## LIST-CREATE GET | POST
-- it will show all the subsection of particular section
-- on create request (POST) use only pass title in parameter,parent field value will get from url
    
# URL section/<menu_id>/subsection/
# http://127.0.0.1:8080/section/1/subsection/

 ## Detail,Updateand delete 
-- in case of delete we have multiple scenario option are listed bellow 
    [(0,"DELETE_ALL_SUBSECTION"),(1,"DELETE_ME_MAKE_SUBSECTION_ORPHAN"),(2,"DELETE_ME_MAKE_MY_SUBSECTION_LEVELUP")]
    so you can pass 0,1 or 2 to pass any one of these option in query_staring. if you dont want to pass  the 
    backend will delete the current instance only 
### URL  /section/<menu_id>/subsection/<id>/detail/
### http://127.0.0.1:8080/section/1/subsection/2/detail/

# GRAPH QL Api Interface #
 url for graphql interface
### /graphql/
###  http://127.0.0.1:8000/graphql/

## Section ##
    query{
    allSection{
        id,
        title
    }
    }
## Section detail ##
    query{
    sectionDetail (id:1){
        title,
        id
    }
    }

## Section create ##
mutation {
  createSection(title:"section graphql"){
    section{
      title
    }
  }
}
## Section update ##
mutation{
  updateSection(id:7,title:"update section test"){
    section{
      title
    }
  }
}
if you want to give parent to section and make this subsection
mutation{
  updateSection(id:7,title:"update section test",parent:1){
    section{
      title
    }
  }
}

## Section delete ##
mutation{
  deleteSection(id:2){
    section{
      title
    }
  }
}

## subsection api ##
    query{
        subsection (id:1){
            title,
            id
        }
    }
## subsection create ##
    mutation {
    createSubsection(title:"test2",parent:1){
    subsection{
        title
    }
    }
    }
## subsection update ##
mutation{
updateSubsection(id:3,title:"update subsection",parent:1){
  section{
    title,
    id
  }
}
}
## subsection delete ##
mutation{
  deleteSubsection(id:2){
    section{
      title
    }
  }
}
### if you want to delete all subsection that have section id 2  ###
mutation{
  deleteSubsection(id:2,option=0){
    section{
      title
    }
  }
}
### if you want to delete only the section having id 2 ###

mutation{
  deleteSubsection(id:2,option=1){
    section{
      title
    }
  }
}

### if you want to delete  section having id 2  and make all his subsection on the same level (level up the section to parent level ) ###
mutation{
  deleteSubsection(id:2,option=1){
    section{
      title
    }
  }
}








