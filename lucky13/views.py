from django.shortcuts import render

def inactive_user(request):
    template_name = 'social_match/inactive_user.html'

    return render(request, template_name)