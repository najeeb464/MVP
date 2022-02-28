from urllib import response
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from section.models import Section
from section.serializer import SectionSerializer,SubSectionSerializer

class SectionCreateTestCase(APITestCase):
    def test_can_create_section(self):
        data={"title":"Section A"}
        response=self.client.post(reverse("section-list"),data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data["title"]=""
        response=self.client.post(reverse("section-list"),data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response=self.client.post(reverse("section-list"),{})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response=self.client.post(reverse("section-list")+"11",data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        

class SectionReadTestCase(APITestCase):
    def setUp(self):
        response=self.client.post(reverse("section-list"),{"title":"Section A"})
        response=self.client.post(reverse("section-list"),{"title":"Section B"})
        response=self.client.post(reverse("section-list"),{"title":"Section C"})
        response=self.client.post(reverse("section-list"),{"title":"Section D"})
    def test_can_get_section(self):
        response=self.client.get(reverse("section-list")+"bugggg")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        response=self.client.get(reverse("section-list"))
        self.assertEqual(response.data[0]["id"],1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class SectionDetailTestCase(APITestCase):
    def setUp(self):
        response=self.client.post(reverse("section-list"),{"title":"Section A"})
        response=self.client.post(reverse("section-list"),{"title":"Section B"})
     
    def test_can_get_section(self):
        response=self.client.get(reverse("section-detail",kwargs={"id":1}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"],1)
        response=self.client.get(reverse("section-detail",kwargs={"id":2}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"],2)
        
class SectionUpdateTestCase(APITestCase):
    def setUp(self):
        response=self.client.post(reverse("section-list"),{"title":"Section A"})
        response=self.client.post(reverse("section-list"),{"title":"Section B"})
        response=self.client.post(reverse("section-list"),{"title":"Section C"})
        response=self.client.post(reverse("section-list"),{"title":"Section D"})
    def test_can_update_section(self):
        response=self.client.put(reverse("section-detail",kwargs={"id":1}),{"title":"Section updated"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"],"Section updated")
        response=self.client.get(reverse("section-detail",kwargs={"id":2}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response=self.client.put(reverse("section-detail",kwargs={"id":2}),{"title":"updated","parent":1})
        response=self.client.patch(reverse("section-detail",kwargs={"id":2}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
class SectionDeleteTestCase(APITestCase):
    def setUp(self):
        response=self.client.post(reverse("section-list"),{"title":"Section A"})
        response=self.client.post(reverse("section-list"),{"title":"Section B"})
   
    def test_can_delete_section(self):
        response=self.client.delete(reverse("section-detail",kwargs={"id":2}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        response=self.client.delete(reverse("section-detail",kwargs={"id":13300}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
        
        
class SubSectionCreateTestCase(APITestCase):
    def setUp(self):
        response=self.client.post(reverse("section-list"),{"title":"Section A"})
        response=self.client.post(reverse("section-list"),{"title":"Section B"})
    def test_can_create_section(self):
        child_A_data={"title":"Section A child"}
        child_B_data={"title":"Section B child"}
        response=self.client.post(reverse("subsection-list",kwargs={"menu_id":1}),child_A_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["parent"],1)
        self.assertEqual(response.data["level"],1)
        response=self.client.post(reverse("subsection-list",kwargs={"menu_id":2}),child_B_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["parent"],2)
        self.assertEqual(response.data["level"],1)


class SectionReadTestCase(APITestCase):
    def setUp(self):
        response=self.client.post(reverse("section-list"),{"title":"Section A"})
        response=self.client.post(reverse("section-list"),{"title":"Section B"})
        response=self.client.post(reverse("subsection-list",kwargs={"menu_id":1}),{"title":"Section A child"})
        response=self.client.post(reverse("subsection-list",kwargs={"menu_id":2}),{"title":"Section B child"})
   
    def test_can_get_section(self):
        response=self.client.get(reverse("subsection-list",kwargs={"menu_id":1}))
        self.assertEqual(response.data[0]["id"],3)
        self.assertEqual(response.status_code, status.HTTP_200_OK)