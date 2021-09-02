from rest_framework import serializers
from air_quality.models import Air_quality

class Air_QualitySerialization(serializers.Serializer):
    id = serializers.IntegerField()
    date = serializers.DateField()
    pm25 = serializers.FloatField()
    pm10 = serializers.FloatField()
    temp = serializers.FloatField()
    aqi = serializers.FloatField()

    def create(self, validated_data):
        """
        Create and return a new `Air_quality` instance, given the validated data.
        """
        return Air_quality.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        instance.id = validated_data.get('id', instance.id)
        instance.date = validated_data.get('date', instance.date)
        instance.pm25 = validated_data.get('pm25', instance.pm25)
        instance.pm10 = validated_data.get('pm10', instance.pm10)
        instance.temp = validated_data.get('temp', instance.temp)
        instance.aqi = validated_data.get('aqi', instance.aqi)
        instance.save()
        return instance