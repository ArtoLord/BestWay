from rest_framework_dataclasses.serializers import DataclassSerializer
from .logic.models import Node
from rest_framework import serializers


class NodeSerializer(DataclassSerializer):
    class Meta:
        exclude = ["id"]
        dataclass = Node


class PathQuerySerializer(serializers.Serializer):
    start = NodeSerializer()
    target = NodeSerializer()
    path_len = serializers.FloatField()


class WaySerializer(serializers.Serializer):
    nodes = NodeSerializer(many=True)
    path_len = serializers.FloatField()
