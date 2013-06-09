from __future__ import unicode_literals

from django.conf.urls import *

from api.resources import v1 as views

massaddpatterns = patterns('',
    url(r'^credit-cards/$', views.MassAddCreditCards.as_view(),
        name='credit_card'),
)

migratepatterns = patterns('',
    url(r'^mass_add/$', include(massaddpatterns, namespace='massadd')),
)

contentpatterns = patterns('',
    url(r'^client/$', views.Client.as_view(), name='client'),
    url(r'^credit-card/$', views.CreditCard.as_view(), name='credit_card'),
)

urlpatterns = patterns('',
    url(r'^v1/migrate/', include(migratepatterns, namespace='migrate')),
    url(r'^v1/content/', include(contentpatterns, namespace='content')),
)

