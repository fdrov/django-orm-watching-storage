from django.shortcuts import render
import django
from datacenter.models import Passcard, Visit, get_duration, format_duration

def storage_information_view(request):
    # Программируем здесь

    visits = Visit.objects.filter(leaved_at=None)
    non_closed_visits = []
    for visit in visits:
        non_closed_visits.append({
            "who_entered": visit.passcard.owner_name,
            "entered_at": django.utils.timezone.localtime(visit.entered_at),
            "duration": format_duration(get_duration(visit))
        })

    context = {
        "non_closed_visits": non_closed_visits,  # не закрытые посещения
    }
    return render(request, 'storage_information.html', context)
