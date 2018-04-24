from datetime import datetime

from game_room.models import Room


def scan_room():
    now = datetime.now()
    Room.objects.filter(start_time__lte=now, status=1).update(status=2)
    Room.objects.filter(end_time__lte=now, status=2).update(status=3)
