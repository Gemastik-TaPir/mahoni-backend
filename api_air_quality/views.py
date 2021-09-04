from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from air_quality.models import Air_quality
from air_quality.serializers import Air_QualitySerialization

@csrf_exempt
def air_quality_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        air_quality = Air_quality.objects.all()
        serializer = Air_QualitySerialization(air_quality, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = Air_QualitySerialization(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def air_quality_detail(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        air_quality = Air_quality.objects.get(pk=pk)
    except Air_quality.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = Air_QualitySerialization(air_quality)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = Air_QualitySerialization(air_quality, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        air_quality.delete()
        return HttpResponse(status=204)
