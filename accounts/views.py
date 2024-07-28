import decimal

from rest_framework import generics, pagination
from rest_framework.response import Response
from rest_framework.decorators import api_view
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django_filters import rest_framework as filters

from accounts.models import Account, Transaction
from accounts.serializers import AccountSerializer, TransactionSerializer


class CustomPageNumberPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
        """
        Override this method to include custom pagination information in the response.
        """
        return Response({
            'count': self.page.paginator.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'first': self.get_first_link(),
            'last': self.get_last_link(),
            'results': data
        })

    def get_first_link(self):
        if self.page.number > 1:
            return self._get_link(1)
        return None

    def get_last_link(self):
        if self.page.number < self.page.paginator.num_pages:
            return self._get_link(self.page.paginator.num_pages)
        return None

    def _get_link(self, page_number):
        request = self.request
        url = request.build_absolute_uri()
        query_params = request.query_params.copy()
        query_params['page'] = page_number
        return f"{url}?{query_params.urlencode()}"


class AccountListCreateView(generics.ListCreateAPIView):
    """
    View for listing and creating accounts.
    """

    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    pagination_class = CustomPageNumberPagination

    @swagger_auto_schema(
        operation_description="Retrieve a list of accounts or create a new account",
        responses={200: AccountSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Create a new account",
        request_body=AccountSerializer,
        responses={201: AccountSerializer}
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class AccountDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    View for retrieving, updating, and deleting an account by ID.
    """

    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    @swagger_auto_schema(
        operation_description="Retrieve, update, or delete an account by ID",
        responses={200: AccountSerializer}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


@swagger_auto_schema(
    method='post',
    operation_description="Deposit money into an account",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'amount': openapi.Schema(type=openapi.TYPE_NUMBER, description='Amount to deposit')
        },
        required=['amount']
    ),
    responses={200: 'Deposit successful'}
)
@api_view(['POST'])
def deposit(request, pk):
    """
    View for depositing money into an account.

    Args:
    pk (int): The ID of the account.
    """

    account = Account.objects.get(pk=pk)
    amount = decimal.Decimal(request.data.get('amount'))
    if amount <= 0:
        return Response({'status': 'Invalid amount'}, status=400)
    account.balance += amount
    account.save()
    Transaction.objects.create(account=account, amount=amount, transaction_type=Transaction.DEPOSIT)
    return Response({'status': 'deposit successful'})


@swagger_auto_schema(
    method='post',
    operation_description="Withdraw money from an account",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'amount': openapi.Schema(type=openapi.TYPE_NUMBER, description='Amount to withdraw')
        },
        required=['amount']
    ),
    responses={200: 'Withdrawal successful', 400: 'Insufficient funds'}
)
@api_view(['POST'])
def withdraw(request, pk):
    """
    View for withdrawing money from an account.

    Args:
    pk (int): The ID of the account.
    """

    account = Account.objects.get(pk=pk)
    amount = decimal.Decimal(request.data.get('amount'))
    if amount <= 0:
        return Response({'status': 'Invalid amount'}, status=400)
    if account.balance >= amount:
        account.balance -= amount
        account.save()
        Transaction.objects.create(account=account, amount=-amount, transaction_type=Transaction.WITHDRAWAL)
        return Response({'status': 'withdrawal successful'})
    else:
        return Response({'status': 'insufficient funds'}, status=400)


@swagger_auto_schema(
    method='post',
    operation_description="Transfer money between accounts",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'from_iban': openapi.Schema(type=openapi.TYPE_STRING, description='IBAN of the sender account'),
            'to_iban': openapi.Schema(type=openapi.TYPE_STRING, description='IBAN of the receiver account'),
            'amount': openapi.Schema(type=openapi.TYPE_NUMBER, description='Amount to transfer')
        },
        required=['from_iban', 'to_iban', 'amount']
    ),
    responses={200: 'Transfer successful', 400: 'Insufficient funds'}
)
@api_view(['POST'])
def transfer(request):
    """
    View for transferring money between accounts.
    """

    from_iban = request.data.get('from_iban')
    to_iban = request.data.get('to_iban')
    amount = decimal.Decimal(request.data.get('amount'))
    if amount <= 0:
        return Response({'status': 'Invalid amount'}, status=400)
    try:
        from_account = Account.objects.get(iban=from_iban)
        to_account = Account.objects.get(iban=to_iban)
    except Account.DoesNotExist:
        return Response({'status': 'Account not found'}, status=404)

    if from_account.balance >= amount:
        from_account.balance -= amount
        to_account.balance += amount
        from_account.save()
        to_account.save()
        Transaction.objects.create(account=from_account, amount=-amount, transaction_type=Transaction.TRANSFER)
        Transaction.objects.create(account=to_account, amount=amount, transaction_type=Transaction.TRANSFER)
        return Response({'status': 'transfer successful'})
    else:
        return Response({'status': 'insufficient funds'}, status=400)


class TransactionFilter(filters.FilterSet):
    """
    Filter for listing transactions by type and date range.
    """
    transaction_type = filters.ChoiceFilter(choices=Transaction.TRANSACTION_TYPES)
    start_date = filters.DateFilter(field_name='date', lookup_expr='gte')
    end_date = filters.DateFilter(field_name='date', lookup_expr='lte')

    class Meta:
        model = Transaction
        fields = ['transaction_type', 'start_date', 'end_date']


class TransactionListView(generics.ListAPIView):
    """
    View for listing transactions of a specific account with sorting, filtering, and pagination.
    """
    serializer_class = TransactionSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = TransactionFilter
    pagination_class = CustomPageNumberPagination

    @swagger_auto_schema(
        operation_description="Retrieve a list of transactions for a specific account with sorting, filtering, and pagination.",
        responses={200: TransactionSerializer(many=True)},
        manual_parameters=[
            openapi.Parameter('ordering', openapi.IN_QUERY, description="Order by date (e.g., '-date' for descending)",
                              type=openapi.TYPE_STRING),
            openapi.Parameter('transaction_type', openapi.IN_QUERY, description="Filter by transaction type",
                              type=openapi.TYPE_STRING),
            openapi.Parameter('start_date', openapi.IN_QUERY, description="Filter by start date (e.g., '2024-01-01')",
                              type=openapi.TYPE_STRING, example='2024-01-01'),
            openapi.Parameter('end_date', openapi.IN_QUERY, description="Filter by end date (e.g., '2024-12-31')",
                              type=openapi.TYPE_STRING, example='2024-12-31'),
            openapi.Parameter('page', openapi.IN_QUERY, description="Page number", type=openapi.TYPE_INTEGER,
                              example=1),
            openapi.Parameter('page_size', openapi.IN_QUERY, description="Number of items per page",
                              type=openapi.TYPE_INTEGER, example=10),
        ]
    )
    def get(self, request, *args, **kwargs):
        ordering = request.query_params.get('ordering', '-date')
        self.queryset = self.filter_queryset(self.get_queryset()).order_by(ordering)
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        account_id = self.kwargs['pk']
        return Transaction.objects.filter(account_id=account_id)
