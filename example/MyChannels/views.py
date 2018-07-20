# Create your views here.

from django.shortcuts import render


# room_name_json': mark_safe(json.dumps(room_name), ),
def room(request, room_name):
    context = {
        'data': {
            'room_name_json': room_name,
            "user": request.GET.get('user', '')
        }
    }
    return render(request, 'MyChannels/room.html', context=context)
