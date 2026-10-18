from django.test import Client, TestCase


class ApplicationViewTests(TestCase):
    def test_post_does_not_require_csrf_cookie(self):
        client = Client(enforce_csrf_checks=True)

        response = client.post(
            "/file-upload/v1/application/",
            {"file": "application data"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Application is running."})
