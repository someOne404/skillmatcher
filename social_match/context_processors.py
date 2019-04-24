from .models import *
from notifications.models import *

def add_variable_to_context(request):
    if request.user.is_authenticated:
        request_user = User.objects.get(id=request.user.id)
        notifications = Notification.objects.filter(recipient=request_user)
    else:
        notifications = []
    return{
        'notifications': notifications
    }