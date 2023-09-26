from django.test import TestCase, Client
from main.models import Product


class mainTest(TestCase):
    def test_main_url_is_exist(self):
        response = Client().get('/main/')
        self.assertEqual(response.status_code, 200)

    def test_main_using_main_template(self):
        response = Client().get('/main/')
        self.assertTemplateUsed(response, 'main.html')


class modelTest(TestCase):

    def create_model(self):
        return Product.objects.create(name="test", amount=101, description="test")

    def test_model(self):
        subject = self.create_model()
        self.assertTrue(isinstance(subject, Product))
        self.assertEqual(subject.__unicode__(), subject)
