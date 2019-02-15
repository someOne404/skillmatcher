from django.shortcuts import render
from django.http import HttpResponse
# from .models import Post


def index(request):
	return render(request, './social_match/index.html')