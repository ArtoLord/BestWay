from django.db import models
from .logic.models import Node


class GraphNode(models.Model):
    id = models.AutoField(primary_key=True)
    lon = models.FloatField()
    lat = models.FloatField()

    @property
    def node(self):
        return Node(self.id, self.lon, self.lat)
