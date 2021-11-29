from django.conf.urls import url

from TravelBooking.views.user import *
from TravelBooking.views.customer import *
from TravelBooking.views.administer import *

urlpatterns = [
    # USER
    url(r'^admin_login$', admin_login),
    url(r'^admin_register$', admin_register),
    url(r'^cust_login$', cust_login),
    url(r'^cust_register$', cust_register),
    url(r'^logout$', logout),

    # ADMIN
    url(r'^show_customers$', show_customers),
    url(r'^show_admins$', show_admins),
    url(r'^add_location$', add_location),
    url(r'^delete_location$',delete_location),
    url(r'^show_location$', show_location),
    url(r'^change_location$', change_location),

    url(r'^add_bus$', add_bus),
    url(r'^delete_bus$', delete_bus),
    url(r'^show_bus$', show_bus),
    url(r'^change_bus$', change_bus),

    url(r'^add_flight$', add_flight),
    url(r'^delete_flight$', delete_flight),
    url(r'^show_flight$', show_flight),
    url(r'^change_flight$', change_flight),

    url(r'^add_hotel$', add_hotel),
    url(r'^delete_hotel$', delete_hotel),
    url(r'^show_hotel$', show_hotel),
    url(r'^change_hotel$', change_hotel),
]