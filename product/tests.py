from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from .models import Type
# Create your tests here.
class ProductTestCase(TestCase):
    def setUp(self):
        type = Type.objects.create(name="FEFEF Pencil")
        type.save()

    def test_created_type(self):
        qs = Type.objects.filter(name="FEFEF Pencil")
        self.assertEquals(qs.count(), 1)

    def test_product_api_get_success(self):
        url = reverse('api-product:product_index')
        print(url)
        res = self.client.get(url, format='json')
        print(res)
        self.assertEquals(res.status_code, status.HTTP_200_OK)

    # def test_product_api_get_success(self):