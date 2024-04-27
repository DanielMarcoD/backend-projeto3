from django.shortcuts import render, redirect
from .models import Game
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import Http404
from .serializers import GameSerializer
from rest_framework import status

# Create your views here.
def index(request):
    return render(request, "meugame/index.html")
@api_view(['GET', 'POST', 'DELETE'])
def api_game(request, game_id):
    try:
        game = Game.objects.get(id=game_id)
    except Game.DoesNotExist:
        raise Http404("Note not found")

    if request.method == 'GET':
        # Serializar a nota e retornar como JSON
        serialized_game = GameSerializer(game)
        return Response(serialized_game.data)
    elif request.method == 'POST':
        # Atualizar os dados da nota
        new_game_data = request.data
        game.title = new_game_data.get('title', game.title)
        game.save()
        serialized_note = GameSerializer(game)
        return Response(serialized_note.data)
    elif request.method == 'DELETE':
        # Deletar a nota e retornar HTTP 204 No Content
        game.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
def api_games(request):
    if request.method == 'GET':
        # Recuperar todas as anotações
        games = Game.objects.all()
        # Serializar a lista de anotações
        serializer = GameSerializer(games, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        # Criar uma nova anotação a partir dos dados recebidos
        serializer = GameSerializer(data=request.data)
        if serializer.is_valid():
            all_games = Game.objects.all()
            for game in all_games:
                if game.title == serializer.validated_data['title']:
                    return Response(status=status.HTTP_409_CONFLICT)
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            # Se os dados não são válidos, retornar um erro
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

