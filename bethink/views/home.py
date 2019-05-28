from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.shortcuts import render

from bethink.models.card import Card
from django.contrib.auth.decorators import login_required

import datetime
NUM_OF_POSTS = 100


@login_required
def home(request):
    first_name = ''
    last_name = ''
    # notify_worker(repeat=10)
    # sent_tg_task(repeat=10)
    username = request.user
    if request.user.groups.filter(name='sa').exists():
        card_list = Card.objects.all()
    else:
        user = User.objects.get(username=username)
        first_name = user.first_name
        last_name = user.last_name
        card_list = Card.objects.filter(user=user)

    card_list = card_list.order_by('-pub_date')

    paginator = Paginator(card_list, NUM_OF_POSTS)  # Show NUM_OF_PAGES posts per page
    page = request.GET.get('page')

    cards = paginator.get_page(page)
    datetime_now = datetime.datetime.now(datetime.timezone.utc)
    return render(request, 'bethink/home.djt', {'cards': cards,
                                                'first_name': first_name,
                                                'last_name': last_name,
                                                'datetime_now': datetime_now})
