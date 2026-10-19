from unittest.mock import patch

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase

from quickstart.models import ApplicationData, FileSystemData


class ApplicationViewTests(TestCase):
    def test_post_does_not_require_csrf_cookie(self):
        client = Client(enforce_csrf_checks=True)

        with patch(
            "quickstart.views.application_view.upload_file",
            return_value="https://example.com/nid-front.jpg",
        ):
            response = client.post(
                "/file-upload/v1/application/",
                {
                    "first_name": "Ada",
                    "last_name": "Lovelace",
                    "nid_front": SimpleUploadedFile("nid-front.jpg", b"document"),
                },
            )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Application is running."})
        application = ApplicationData.objects.get(first_name="Ada")
        self.assertEqual(application.nid_front, "https://example.com/nid-front.jpg")
        self.assertEqual(application.file_system_data.count(), 1)
        self.assertEqual(
            application.file_system_data.get().filename,
            "nid-front.jpg",
        )

    def test_invalid_application_is_rejected(self):
        response = self.client.post(
            "/file-upload/v1/application/",
            {"last_name": "Lovelace"},
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(ApplicationData.objects.count(), 0)
        self.assertEqual(FileSystemData.objects.count(), 0)
