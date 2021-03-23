import django
from django.shortcuts import render

from datacenter.models import Visit, get_duration, format_duration


def storage_information_view(request):
    visits = Visit.objects.filter(leaved_at=None)
    non_closed_visits = []
    for visit in visits:
        non_closed_visits.append({
            "who_entered": visit.passcard.owner_name,
            "entered_at": django.utils.timezone.localtime(visit.entered_at),
            "duration": format_duration(get_duration(visit))
        })

    context = {
        "non_closed_visits": non_closed_visits,
    }
    return render(request, 'storage_information.html', context)
