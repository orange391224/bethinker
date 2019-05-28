from django.urls import path
from bethink.views.home import home
from bethink.views.card import CardView, CardCreate, CardUpdate, CardDelete, card_new, card_edit
from bethink.views.profile import update_profile
from bethink.views.register_task import reg_tg_sender, tg_sender_debug

app_name = 'bethink'
urlpatterns = [
    # ex: /bethink/
    path('', home, name='home'),
    # ex: /bethink/profile
    # path('<str:username>', home, name='user_profile'),
    path('profile/', update_profile, name='user_profile'),
    # рег таска
    path('reg_task/', reg_tg_sender),
    #
    path('dbg/', tg_sender_debug),
    # ex: /bethink/card/5/
    path('card/<int:pk>/', CardView.as_view(), name='card'),
    # ex: /bethink/post/create/
    path('card/create/', CardCreate.as_view(), name='create_card'),
    # ex  /bethink/card/new/
    path('card/new/', card_new, name='card_new'),
    # ex: /bethink/card/5/update/
    path('card/create/<int:pk>/update', CardUpdate.as_view(), name='update_card'),
    path('post/<int:pk>/edit/', card_edit, name='card_edit'),
    # ex: /bethink/card/5/delete/
    path('post/<int:pk>/delete/', CardDelete.as_view(), name='delete_card'),
]
