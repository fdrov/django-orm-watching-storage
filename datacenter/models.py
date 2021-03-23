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
    entered_at = django.utils.timezone.localtime(visit.entered_at)
    return django.utils.timezone.localtime()-entered_at


def get_stayed(visit):
    return visit.leaved_at - visit.entered_at


def format_duration(duration):
    days, seconds = duration.days, duration.seconds
    hours = days * 24 + seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    if days:
        return f'{days} д. {hours} ч. {minutes} мин.'
    return f'{hours} ч. {minutes} мин.'


def is_visit_long(visit, minutes=60):
    if visit.leaved_at:
        duravion = (visit.leaved_at - visit.entered_at).total_seconds()
        return duravion > (minutes * 60)