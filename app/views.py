from rest_framework.decorators import api_view
from rest_framework.response import Response
from .logic.ways import Pathfinder
from .logic.graph import NxGraph
from .serializers import PathQuerySerializer, NodeSerializer, WaySerializer
from BestWay.settings import NODES_FILENAME, GRAPH_FILENAME
from django.http import HttpResponse
from django.template import loader


"""
Это константы
Я знаю, что это антипаттерн, но кажется это 
самый приемлемый вариант в плане производительности и памяти 
"""
graph = NxGraph(GRAPH_FILENAME, NODES_FILENAME)
path_finder = Pathfinder(graph)


@api_view(["POST"])
def get_path(request):
    data = PathQuerySerializer(data=request.data)
    if not data.is_valid():
        return Response(status=400)
    start_node = data.validated_data['start']
    end_node = data.validated_data['target']
    path_len = data.validated_data['path_len']
    try:
        way = path_finder.find_path_betwen_two(start_node, end_node, path_len)
        return Response(WaySerializer({"nodes": way, "path_len": way.length()}).data)
    except ValueError as e:
        return Response( {"error": "range between target and start is more then path length"}, status=400)

def main(request):
    return HttpResponse(loader.get_template("main.html").render({}, request))
