# django imports
from apps.account.serializers import AccountSerializer
from apps.account.models import Account

# rest imports
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.decorators import api_view

@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def register(request):
  serializer = AccountSerializer(data=request.data)
  if serializer.is_valid():
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)
  return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def profile(request):
  qs = Account.objects.get(id=request.user.id)
  serializer = AccountSerializer(qs, many=False)
  return Response(serializer.data, status=status.HTTP_200_OK)