from rest_framework import serializers
from .models import Programmer

class ProgrammerSerializer(serializers.ModelSerializer):
    technology = serializers.SerializerMethodField()

    class Meta:
        model = Programmer
        fields = ['id', 'name', 'technology']

    def get_technology(self, obj):
        return [
            tech['name'] if isinstance(tech, dict) else tech.name 
            for tech in obj.technology
        ]

    def create(self, validated_data):
        technology_data = validated_data.pop('technology', [])
        programmer = Programmer.objects.create(**validated_data)
        programmer.set_technology_list(technology_data)
        return programmer

    def update(self, instance, validated_data):
        technology_data = validated_data.pop('technology', [])
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.set_technology_list(technology_data)
        instance.save()
        return instance
