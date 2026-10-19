from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView

from quickstart.serializers import ApplicationSerializer
from services.file_upload_service import upload_file


class ApplicationView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def __init__(self):
        super(ApplicationView, self).__init__()
        self.serializer_class = ApplicationSerializer
        self.serialized_data = None
        self.lang = 'en'

    def _validate_request(self):
        serializer = self.serializer_class(data=self.request.data)

        if not serializer.is_valid():
            self.serialized_data = serializer.validated_data
            return Response({ "message": "Request is valid."})

        return None

    def _process_application(self):
        files = self.request.FILES

        for file in files.values():
            file_url = upload_file(file=file)



        return None

    def _process(self):
        self.lang = self.request.headers.get("Accept-Language", "en")

        # Validate the request data
        if output := self._validate_request():
            return output

        if output := self._process_application():
            return output

        return Response({"message": "Application is running."})

    def post(self, request):
        return self._process()