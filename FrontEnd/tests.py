from django.test import TestCase


class test_frontend_calls(TestCase):

    def test_index(self):
        response = self.client.get("/FrontEnd/")
        print response
        pass

    def test_show(self):
        response = self.client.get("/FrontEnd/1")
        print response
