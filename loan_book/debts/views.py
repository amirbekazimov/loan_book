from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Debt
from .serializers import DebtSerializer


class DebtListCreateView(APIView):
    """
    GET: Retrieve the list of debts.
    POST: Create a new debt.
    """

    def get(self, request):
        if request.user.is_shop_owner:
            debts = Debt.objects.filter(creditor=request.user)
        else:
            debts = Debt.objects.filter(customer=request.user)

        serializer = DebtSerializer(debts, many=True)
        return Response(serializer.data)

    def post(self, request):
        if not request.user.is_shop_owner:
            return Response({"error": "Only shop owners can create debts."}, status=status.HTTP_403_FORBIDDEN)

        serializer = DebtSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DebtDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk, user):
        debt = Debt.objects.filter(pk=pk, customer=user).first()
        if not debt:
            debt = Debt.objects.filter(pk=pk, creditor=user).first()
        return debt

    def get(self, request, pk):
        debt = self.get_object(pk, request.user)
        if debt is None:
            return Response({"error": "Debt not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = DebtSerializer(debt)
        return Response(serializer.data)

    def put(self, request, pk):
        if not request.user.is_shop_owner:
            return Response({"error": "Only shop owners can edit debts."}, status=status.HTTP_403_FORBIDDEN)

        debt = self.get_object(pk, request.user)
        if debt is None:
            return Response({"error": "Debt not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = DebtSerializer(debt, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        if not request.user.is_shop_owner:
            return Response({"error": "Only shop owners can edit debts."}, status=status.HTTP_403_FORBIDDEN)

        debt = self.get_object(pk, request.user)
        if debt is None:
            return Response({"error": "Debt not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = DebtSerializer(debt, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        if not request.user.is_shop_owner:
            return Response({"error": "Only shop owners can delete debts."}, status=status.HTTP_403_FORBIDDEN)

        debt = self.get_object(pk, request.user)
        if debt is None:
            return Response({"error": "Debt not found"}, status=status.HTTP_404_NOT_FOUND)

        debt.delete()
        return Response({"message": "Debt deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class MyDebtsView(APIView):
    """
    GET: Retrieve the list of debts where the current user is the customer.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        debts = Debt.objects.filter(customer=request.user)
        serializer = DebtSerializer(debts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
