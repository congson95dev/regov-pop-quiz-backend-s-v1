from django.test import TestCase


class ViewsTestCase(TestCase):
    def test_index_loads_properly(self):
        """The index page loads properly"""
        response = self.client.get('/courses/')
        self.assertEqual(response.status_code, 401)
        # self.assertEqual(len(response.context['customers']), 5)
