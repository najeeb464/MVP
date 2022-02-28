from django.urls import path
from section.views import SectionListView,SectionDetailView,SubSectionListView,SubSectionDetailView,DeleteSectionParentChoices
from section.schema import schema
from graphene_django.views import GraphQLView
urlpatterns = [
    path("section/"                                         ,SectionListView.as_view()              ,name="section-list"),
    path("section/<id>/detail/"                             ,SectionDetailView.as_view()            ,name="section-detail"),
    path("section/<menu_id>/subsection/"                    ,SubSectionListView.as_view()           ,name="subsection-list"),
    path("section/<menu_id>/subsection/<id>/detail/"        ,SubSectionDetailView.as_view()         ,name="subsection-detail"),
    path("section/<menu_id>/subsection/<id>/detail/"        ,DeleteSectionParentChoices.as_view()   ,name="delete_parent-choices"),
    path("graphql/"                                          ,GraphQLView.as_view(graphiql=True     ,schema=schema))

]