from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView

from quickstart.models import ApplicationData
from quickstart.serializers import ApplicationSerializer
from services.file_upload_service import upload_file, create_file_records


class ApplicationView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def __init__(self):
        super(ApplicationView, self).__init__()
        self.serializer_class = ApplicationSerializer
        self.serialized_data = None
        self.FILE_FIELDS = ["nid_front", "nid_back", "passport", "signature"]
        self.lang = 'en'

    def _validate_request(self):
        serializer = self.serializer_class(data=self.request.data)

        if not serializer.is_valid():
            return Response({ "message": "Request is not valid."}, status=status.HTTP_400_BAD_REQUEST)

        self.serialized_data = serializer.validated_data

        return None

    def _process_application(self):
        files = self.request.FILES

        uploaded = {}
        for field in self.FILE_FIELDS:
            document = files[field]
            uploaded[field] = (document.name, upload_file(file=document))

        application = ApplicationData.objects.create_application_obj(
            **self.serialized_data,
            **{field: url for field, (_, url) in uploaded.items()}
        )

        if not application:
            return Response({"message": "Failed to create application."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        create_file_records(application=application, files=uploaded)

        return None

    def _process(self):
        self.lang = self.request.headers.get("Accept-Language", "en")

        # Validate the request data
        if output := self._validate_request():
            return output

        if output := self._process_application():
            return output

        return Response({"message": "Application created successfully."}, status=status.HTTP_201_CREATED)

    def post(self, request):
        return self._process()