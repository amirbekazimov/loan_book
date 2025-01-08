from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# from .serializers import UserSerializer

from .models import Debt
from .serializers import DebtSerializer


class DebtListCreateView(APIView):
    """
    GET: Retrieve the list of debts.
    POST: Create a new debt.
    """

    def get(self, request):
        debts = Debt.objects.all()
        serializer = DebtSerializer(debts, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = DebtSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DebtDetailView(APIView):
    """
        GET: Retrieve the debt details.
        PUT: Fully update the debt.
        PATCH: Partially update the debt.
        DELETE: Delete the debt.
    """

    def get_object(self, pk):
        try:
            return Debt.objects.get(pk=pk)
        except Debt.DoesNotExist:
            return None

    def get(self, request, pk):
        debt = self.get_object(pk)
        if debt is None:
            return Response({"error": "Debt not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = DebtSerializer(debt)
        return Response(serializer.data)

    def put(self, request, pk):
        debt = self.get_object(pk)
        if debt is None:
            return Response({"error": "Debt not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = DebtSerializer(debt, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        debt = self.get_object(pk)
        if debt is None:
            return Response({"error": "Debt not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = DebtSerializer(debt, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        debt = self.get_object(pk)
        if debt is None:
            return Response({"error": "Debt not found"}, status=status.HTTP_404_NOT_FOUND)
        debt.delete()
        return Response({"message": "Debt deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class MyDebtsView(APIView):
    """
    GET: Retrieve the list of debts where the current user is the customer.
    """

    def get(self, request):
        # Get all debts where the current user is the customer
        debts = Debt.objects.filter(customer=request.user)
        serializer = DebtSerializer(debts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)