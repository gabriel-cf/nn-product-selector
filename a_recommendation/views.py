import json
from django.shortcuts import render
from django.http import JsonResponse
from .api import getRecommendationResponseJSON
def a_recommendation(request):
     u_username = request.GET.get('u_username')
     json_o = getRecommendationResponseJSON(u_username)
     if not json_o:
         return JsonResponse({}, status=204)
     return JsonResponse(json_o)
