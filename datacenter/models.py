from django.db import models
import datetime
import django


class Passcard(models.Model):
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    passcode = models.CharField(max_length=200, unique=True)
    owner_name = models.CharField(max_length=255)

    def __str__(self):
        if self.is_active:
            return self.owner_name
        return f'{self.owner_name} (inactive)'


class Visit(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    passcard = models.ForeignKey(Passcard)
    entered_at = models.DateTimeField()
    leaved_at = models.DateTimeField(null=True)

    def __str__(self):
        return "{user} entered at {entered} {leaved}".format(
            user=self.passcard.owner_name,
            entered=self.entered_at,
            leaved= "leaved at " + str(self.leaved_at) if self.leaved_at else "not leaved"
        )


def get_duration(visit):
    if visit.leaved_at:
        return visit.leaved_at - visit.entered_at
    else:
        return django.utils.timezone.localtime() - visit.entered_at


def format_duration(duration):
    days, seconds = duration.days, duration.seconds
    hours = days * 24 + seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    if days:
        return f'{days} д. {hours} ч. {minutes} мин.'
    return f'{hours} ч. {minutes} мин. {seconds} сек.'


def is_visit_long(visit, minutes=60):
    if visit.leaved_at:
        duration = (visit.leaved_at - visit.entered_at).total_seconds()
        return duration > (minutes * 60)
    else:
        duration = (django.utils.timezone.localtime() - visit.entered_at).total_seconds()
        return duration > (minutes * 60)


def is_person_strange(any_visit):
    all_person_visits = Visit.objects.filter(passcard__owner_name=any_visit.passcard.owner_name)
    is_strange = False
    for visit in all_person_visits:
        if is_visit_long(visit):
            is_strange = True
            break
    return is_strange
