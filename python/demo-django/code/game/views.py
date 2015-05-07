# coding=utf-8
from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader, RequestContext
from character.models import Character
from game.models import Game
from django.db import models
from random import shuffle, choice
from gamequiz.functions import setAnswerCache, solveChallengeCache


def getChallenge(request):
	t = loader.get_template('game.html')
	possible_challenges = [gameWithCharChallenge(request), charWithGameChallenge(request)]
	result = choice(possible_challenges)
	c = RequestContext(request, result)
	return HttpResponse(t.render(c))


def solveChallenge(request):
	result = "KO"
	if 'answer' in request.POST:
		if solveChallengeCache(request.POST['answer'], request.user.id):
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
	response = {'question': q, 'answers': names}
	# Guardo en caché el resultado esperado
	setAnswerCache(correct_answer_game.name, request.user.id)
	return response

def charWithGameChallenge(request, difficulty=1):
	# Elegir un juego al azar que tenga al menos
	selected_game = Game.objects.annotate(n_games=models.Count('characters')).filter(n_games__gte=1).order_by('?').first()
	possible_correct_chars = selected_game.characters.all().order_by('?')
	correct_answer_char = possible_correct_chars.first()
	incorrect_chars = Character.objects.exclude(id__in=possible_correct_chars)[:difficulty+1]
	q = u"¿Qué personaje pertenece a " + selected_game.name + "?"
	names = []
	for char in incorrect_chars:
		names.append(char.name)
	names.append(correct_answer_char.name)
	shuffle(names)
	response = {'question': q, 'answers': names}
	setAnswerCache(correct_answer_char.name, request.user.id)
	return response