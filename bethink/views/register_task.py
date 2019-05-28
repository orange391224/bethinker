from bethink.tasks import sent_tg_task, sent_tg_task_debug
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse


@login_required
def tg_sender_debug(request):
    sent_tg_task_debug()
    return HttpResponse('debug')

@login_required
def reg_tg_sender(request):
    sent_tg_task(repeat=25)
    #sent_tg_task()
    return HttpResponse('Ok')


