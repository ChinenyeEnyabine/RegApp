from rest_framework import status, viewsets
from rest_framework.response import Response
from .serializers import DataSerializer, AirtimeSerializer, ElectricitySerializer, CabletvSerializer
from .models import BillOperation

class BillOperationViewSet(viewsets.ModelViewSet):
    queryset = BillOperation.objects.all()

    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)
        # Determine which serializer to use based on the request data
        if request.method == 'POST':
            if 'dataplan' in request.data:
                self.serializer_class = DataSerializer
            elif 'rechargeplan' in request.data:
                self.serializer_class = AirtimeSerializer
            elif 'meterno' in request.data:
                self.serializer_class = ElectricitySerializer
            elif 'selectbouquet' in request.data:
                self.serializer_class = CabletvSerializer
            else:
                # Explicitly raise an error for clarity and error handling
                raise ValueError("Invalid request data. Missing required fields.")

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
