# -*- coding: UTF-8 -*-
from django.core.cache import cache


def setAnswerCache(answer, id, timeout=100):
	cache.set(id, answer, timeout)


def solveChallengeCache(answer, id):
	result = False
	if cache.get(id) == answer:
		result = True
		# usuario.add_success()
	cache.set(id, None)
	return result


def removekey(d, key):
	r = dict(d)
	del r[key]
	return r