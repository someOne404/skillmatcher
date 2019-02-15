from django.shortcuts import render
from django.http import HttpResponse
# from .models import Post


def index(request):
	if request.user.is_authenticated:
		response = HttpResponse("Hello, logged in")
	else:
		return render(request, './social_match/index.html')
	return response

	