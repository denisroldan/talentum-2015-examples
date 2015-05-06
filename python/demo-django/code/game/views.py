# coding=utf-8
from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader, RequestContext
from character.models import Character
from game.models import Game
from django.db import models
from random import shuffle


def getChallenge(request):
	t = loader.get_template('game.html')
	result = gameWithCharChallenge(request)
	c = RequestContext(request, result)
	return HttpResponse(t.render(c))


def solveChallenge(request):
	result = "KO"
	if 'answer' in request.POST and 'correct_answer' in request.POST:
		if request.POST['answer'] == request.POST['correct_answer']:
			result = "OK"
	t = loader.get_template('solve.html')
	c = RequestContext(request, {'result': result})
	return HttpResponse(t.render(c))


def gameWithCharChallenge(request, difficulty=1):
	# Elegimos un char al azar que tenga al menos tantos juegos como la dificultad indique (menos uno)
	selected_char = Character.objects.annotate(chars=models.Count('game')).filter(chars__gte=difficulty).order_by('?').first()
	# Obtenemos tantos personajes del videojuego elegido, ordenados al azar, como indica la dificultad
	correct_answer_game = selected_char.game.order_by('?').first()
	# Escogemos un juego que NO contiene al personaje
	games_without_char = Game.objects.exclude(id__in=selected_char.game.all()).order_by('?')[:difficulty+1]
	q = u"¿Qué juego contiene como personaje a " + selected_char.name + "?"
	names = []  # Creamos una lista donde guardar las respuestas
	for game in games_without_char:
		names.append(game.name)
	names.append(correct_answer_game.name)  # Añadimos la respuesta correcta
	shuffle(names)  # Reordenamos las respuestas para que no siempre quede en último lugar la correcta
	# Creamos un diccionario de respuesta
	response = {'question': q, 'answers': names, 'correct_answer': correct_answer_game.name}
	return response