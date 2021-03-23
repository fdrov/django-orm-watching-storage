import django

from datacenter.models import Passcard, format_duration, get_duration, is_visit_long, get_stayed
from datacenter.models import Visit
from django.shortcuts import render


def passcard_info_view(request, passcode):
    visits = Visit.objects.filter(passcard__passcode=passcode)
    this_passcard_visits = []
    for visit in visits:
        this_passcard_visits.append({
            "entered_at": django.utils.timezone.localtime(visit.entered_at),
            "duration": format_duration(get_stayed(visit)),
            "is_strange": is_visit_long(visit)
        })

    context = {
        "passcard": Passcard.objects.get(passcode=passcode),
        "this_passcard_visits": this_passcard_visits
    }
    return render(request, 'passcard_info.html', context)
