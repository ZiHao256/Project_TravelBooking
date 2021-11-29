# Create your views here.
import json
from datetime import datetime

from django.core import serializers
from django.http import JsonResponse, QueryDict
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from TravelBooking.forms import *
from TravelBooking.models import *


def object_to_json(obj):
    return dict([(kk, obj.__dict__[kk]) for kk in obj.__dict__.keys() if kk != "_state"])


@require_http_methods(["GET"])
def show_customers(request):
    response = {}
    try:

        if request.GET.get('custID') is not None:
            customer = CUSTOMERS.objects.get(custID=request.GET.get('custID'))
            response['list'] = object_to_json(customer)
            total = 1
            response['error_num'] = -1
        else:
            # 返回值增加了分页，把数据分成每页pagesize个数据
            customer = CUSTOMERS.objects.all()
            listall = json.loads(serializers.serialize("json", customer))
            total = int(len(listall))
            pagesize = int(request.GET.get('pagesize'))
            pagenum = int(request.GET.get('pagenum'))
            # print(pagesize, pagenum)
            if pagesize > total:
                pagesize = total
            sort_ls = [listall[i:i + pagesize] for i in range(0, len(listall), pagesize)]
            response['list'] = sort_ls[pagenum - 1]
            response['error_num'] = 0
        response['msg'] = 'success'
        response['total'] = total
    except  Exception as e:
        response['msg'] = str(e)
        print(str(e))
        response['error_num'] = 1
    return JsonResponse(response)


@require_http_methods(["GET"])
def show_admins(request):
    response = {}
    try:
        if request.GET.get('adminID') is not None:
            admin = ADMINS.objects.get(adminID=request.GET.get('adminID'))
            response['list'] = object_to_json(admin)
            total = 1
            response['error_num'] = -1
        else:
            # 返回值增加了分页，把数据分成每页pagesize个数据
            admins = ADMINS.objects.all()
            listall = json.loads(serializers.serialize("json", admins))
            total = int(len(listall))
            pagesize = int(request.GET.get('pagesize'))
            pagenum = int(request.GET.get('pagenum'))
            # print(pagesize, pagenum)
            if pagesize > total:
                pagesize = total
            sort_ls = [listall[i:i + pagesize] for i in range(0, len(listall), pagesize)]
            response['list'] = sort_ls[pagenum - 1]
            response['error_num'] = 0
        response['msg'] = 'success'
        response['total'] = total
    except  Exception as e:
        response['msg'] = str(e)
        print(str(e))
        response['error_num'] = 1
    return JsonResponse(response)


# 管理LOCATION
@csrf_exempt
@require_http_methods(['POST'])
def add_location(request):
    response = {}
    try:
        location_form = LOCATIONSForm(request.POST)
        if location_form.is_valid():
            loc_name = location_form.cleaned_data['location']
            try:
                LOCATIONS.objects.get(location=loc_name)
                response['msg'] = 'location exsited'
                response['error_num'] = 1
            except:

                l = LOCATIONS(
                    location=loc_name,
                    riskLevel=location_form.cleaned_data['riskLevel']
                )
                response['msg'] = 'successfully'
                response['error_num'] = 0
        else:
            response['msg'] = 'form is not valid'
            response['error_num'] = 1
    except  Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 2
    return JsonResponse(response)


@csrf_exempt
@require_http_methods(['DELETE'])
def delete_location(request):
    response = {}
    DELETE = QueryDict(request.body)
    loc_name = DELETE.get('location')
    print(loc_name)
    location = LOCATIONS.objects.get(location=loc_name)
    location.delete()
    response['msg'] = 'delete location successfully'
    response['error_num'] = 0
    return JsonResponse(response)


@require_http_methods(['GET'])
def show_location(request):
    response = {}
    try:
        location = {}
        if request.GET.get('location') is not None:
            loc = LOCATIONS.objects.get(location=request.GET.get('location'))
            response['list'] = object_to_json(loc)
            total = 1
            response['error_num'] = -1
        else:
            # 返回值增加了分页，把数据分成每页pagesize个数据
            locs = LOCATIONS.objects.all()
            listall = json.loads(serializers.serialize("json", locs))
            total = int(len(listall))
            pagesize = int(request.GET.get('pagesize'))
            pagenum = int(request.GET.get('pagenum'))
            # print(pagesize, pagenum)
            if pagesize > total:
                pagesize = total
            sort_ls = [listall[i:i + pagesize] for i in range(0, len(listall), pagesize)]
            response['list'] = sort_ls[pagenum - 1]
            response['error_num'] = 0
        response['msg'] = 'success'
        response['total'] = total
    except  Exception as e:
        response['msg'] = str(e)
        print(str(e))
        response['error_num'] = 1
    return JsonResponse(response)


@csrf_exempt
@require_http_methods(['POST'])
def change_location(request):
    response = {}
    try:
        location_form = LOCATIONSForm(request.POST)
        if location_form.is_valid():
            loc_name = location_form.cleaned_data['location']
            try:
                location = LOCATIONS.objects.get(location=loc_name)
                location.riskLevel = location_form.cleaned_data['riskLevel']
                location.save()
                response['msg'] = 'successfully'
                response['error_num'] = 0
            except Exception as e:
                response['msg'] = 'location does not exsited'
                response['error_num'] = 1
        else:
            response['msg'] = 'form is not valid'
            response['error_num'] = 2

    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 3
    return JsonResponse(response)


# 管理 FLIGHT

@csrf_exempt
@require_http_methods(['POST'])
def add_flight(request):
    response = {}
    try:
        flight_form = FLIGHTSForm(request.POST)
        if flight_form.is_valid():
            flightNum = flight_form.cleaned_data['flightNum']
            try:
                FLIGHTS.objects.get(flightNum=flightNum)
                response['msg'] = 'flight exsited'
                response['error_num'] = 1
            except:

                flight = FLIGHTS(
                    flightNum=flightNum,
                    price=flight_form.cleaned_data['price'],
                    numSeats=flight_form.cleaned_data['numSeats'],
                    numAvial=flight_form.cleaned_data['numAvial'],
                    FromCity=flight_form.cleaned_data['FromCity'],
                    ArivCity=flight_form.cleaned_data['ArivCity']
                )
                flight.save()
                response['msg'] = 'successfully'
                response['error_num'] = 0
        else:
            response['msg'] = 'form is not valid'
            response['error_num'] = 1
    except  Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 2
    return JsonResponse(response)


@csrf_exempt
@require_http_methods(['DELETE'])
def delete_flight(request):
    response = {}
    DELETE = QueryDict(request.body)
    flightNum = DELETE.get('flightNum')
    print(flightNum)
    flight = FLIGHTS.objects.get(flightNum=flightNum)
    flight.delete()
    response['msg'] = 'delete flight successfully'
    response['error_num'] = 0
    return JsonResponse(response)


@require_http_methods(['GET'])
def show_flight(request):
    response = {}
    try:

        if request.GET.get('flightNum') is not None:
            flight = FLIGHTS.objects.get(flightNum=request.GET.get('flightNum'))
            response['list'] = object_to_json(flight)
            total = 1
            response['error_num'] = -1
        else:
            # 返回值增加了分页，把数据分成每页pagesize个数据
            flights = FLIGHTS.objects.all()
            listall = json.loads(serializers.serialize("json", flights))
            total = int(len(listall))
            pagesize = int(request.GET.get('pagesize'))
            pagenum = int(request.GET.get('pagenum'))
            # print(pagesize, pagenum)
            if pagesize > total:
                pagesize = total
            sort_ls = [listall[i:i + pagesize] for i in range(0, len(listall), pagesize)]
            response['list'] = sort_ls[pagenum - 1]
            response['error_num'] = 0
        response['msg'] = 'success'
        response['total'] = total
    except  Exception as e:
        response['msg'] = str(e)
        print(str(e))
        response['error_num'] = 1
    return JsonResponse(response)


@csrf_exempt
@require_http_methods(['POST'])
def change_flight(request):
    response = {}
    try:
        flight_form = FLIGHTSForm(request.POST)
        if flight_form.is_valid():
            flightNum = flight_form.cleaned_data['flightNum']
            try:
                flight = FLIGHTS.objects.get(flightNum=flightNum)
                flight.price = flight_form.cleaned_data['price']
                flight.numSeats = flight_form.cleaned_data['numSeats']
                flight.numAvial = flight_form.cleaned_data['numAvial']
                flight.FromCity = flight_form.cleaned_data['FromCity']
                flight.ArivCity = flight_form.cleaned_data['ArivCity']
                flight.save()
                response['msg'] = 'successfully'
                response['error_num'] = 0
            except Exception as e:
                response['msg'] = 'flight does not exsited'
                response['error_num'] = 1
        else:
            response['msg'] = 'form is not valid'
            response['error_num'] = 2

    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 3
    return JsonResponse(response)


# 管理 HOTEL

@csrf_exempt
@require_http_methods(['POST'])
def add_hotel(request):
    response = {}
    try:
        hotel_form = HOTELSForm(request.POST)
        if hotel_form.is_valid():
            hotel_loc = hotel_form.cleaned_data['location']
            try:
                HOTELS.objects.get(location=hotel_loc)
                response['msg'] = 'hotel exsited'
                response['error_num'] = 1
            except:

                hotel = HOTELS(
                    location=hotel_loc,
                    price=hotel_form.cleaned_data['price'],
                    numRooms=hotel_form.cleaned_data['numRooms'],
                    numAvail=hotel_form.cleaned_data['numAvail']
                )
                hotel.save()
                response['msg'] = 'successfully'
                response['error_num'] = 0
        else:
            response['msg'] = 'form is not valid'
            response['error_num'] = 1
    except  Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 2
    return JsonResponse(response)


@csrf_exempt
@require_http_methods(['DELETE'])
def delete_hotel(request):
    response = {}
    DELETE = QueryDict(request.body)
    hotel_loc = DELETE.get('location')
    print(hotel_loc)
    hotel = HOTELS.objects.get(location=hotel_loc)
    hotel.delete()
    response['msg'] = 'delete hotel successfully'
    response['error_num'] = 0
    return JsonResponse(response)


@require_http_methods(['GET'])
def show_hotel(request):
    response = {}
    try:

        if request.GET.get('location') is not None:
            hotel = HOTELS.objects.get(location=request.GET.get('location'))
            response['list'] = object_to_json(hotel)
            total = 1
            response['error_num'] = -1
        else:
            # 返回值增加了分页，把数据分成每页pagesize个数据
            hotels = HOTELS.objects.all()
            listall = json.loads(serializers.serialize("json", hotels))
            total = int(len(listall))
            pagesize = int(request.GET.get('pagesize'))
            pagenum = int(request.GET.get('pagenum'))
            # print(pagesize, pagenum)
            if pagesize > total:
                pagesize = total
            sort_ls = [listall[i:i + pagesize] for i in range(0, len(listall), pagesize)]
            response['list'] = sort_ls[pagenum - 1]
            response['error_num'] = 0
        response['msg'] = 'success'
        response['total'] = total
    except  Exception as e:
        response['msg'] = str(e)
        print(str(e))
        response['error_num'] = 1
    return JsonResponse(response)


@csrf_exempt
@require_http_methods(['POST'])
def change_hotel(request):
    response = {}
    try:
        hotel_form = HOTELSForm(request.POST)
        if hotel_form.is_valid():
            hotel_loc = hotel_form.cleaned_data['location']
            try:
                hotel = HOTELS.objects.get(location=hotel_loc)
                hotel.price = hotel_form.cleaned_data['price']
                hotel.numRooms = hotel_form.cleaned_data['numRooms']
                hotel.numAvail = hotel_form.cleaned_data['numAvail']
                hotel.save()
                response['msg'] = 'successfully'
                response['error_num'] = 0
            except Exception as e:
                response['msg'] = 'hotel does not exsited'
                response['error_num'] = 1
        else:
            response['msg'] = 'form is not valid'
            response['error_num'] = 2

    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 3
    return JsonResponse(response)


# 管理 BUS

@csrf_exempt
@require_http_methods(['POST'])
def add_bus(request):
    response = {}
    try:
        bus_form = BUSESForm(request.POST)
        if bus_form.is_valid():
            bus_loc = bus_form.cleaned_data['location']
            try:
                BUS.objects.get(location=bus_loc)
                response['msg'] = 'bus exsited'
                response['error_num'] = 1
            except:

                bus = BUS(
                    location=bus_loc,
                    price=bus_form.cleaned_data['price'],
                    numSeats=bus_form.cleaned_data['numSeats'],
                    numAvail=bus_form.cleaned_data['numAvail']
                )

                bus.save()
                response['msg'] = 'successfully'
                response['error_num'] = 0
        else:
            response['msg'] = 'form is not valid'
            response['error_num'] = 1
    except  Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 2
    return JsonResponse(response)


@csrf_exempt
@require_http_methods(['DELETE'])
def delete_bus(request):
    response = {}
    DELETE = QueryDict(request.body)
    bus_loc = DELETE.get('location')
    print(bus_loc)
    bus = BUS.objects.get(location=bus_loc)
    bus.delete()
    response['msg'] = 'delete bus successfully'
    response['error_num'] = 0
    return JsonResponse(response)


@require_http_methods(['GET'])
def show_bus(request):
    response = {}
    try:

        if request.GET.get('location') is not None:
            bus = BUS.objects.get(location=request.GET.get('location'))
            response['list'] = object_to_json(bus)
            total = 1
            response['error_num'] = -1
        else:
            # 返回值增加了分页，把数据分成每页pagesize个数据
            buses = BUS.objects.all()
            listall = json.loads(serializers.serialize("json", buses))
            total = int(len(listall))
            pagesize = int(request.GET.get('pagesize'))
            pagenum = int(request.GET.get('pagenum'))
            # print(pagesize, pagenum)
            if pagesize > total:
                pagesize = total
            sort_ls = [listall[i:i + pagesize] for i in range(0, len(listall), pagesize)]
            response['list'] = sort_ls[pagenum - 1]
            response['error_num'] = 0
        response['msg'] = 'success'
        response['total'] = total
    except  Exception as e:
        response['msg'] = str(e)
        print(str(e))
        response['error_num'] = 1
    return JsonResponse(response)


@csrf_exempt
@require_http_methods(['POST'])
def change_bus(request):
    response = {}
    try:
        bus_form = BUSESForm(request.POST)
        if bus_form.is_valid():
            bus_loc = bus_form.cleaned_data['location']
            try:
                bus = BUS.objects.get(location=bus_loc)
                bus.price = bus_form.cleaned_data['price']
                bus.numSeats = bus_form.cleaned_data['numSeats']
                bus.numAvail = bus_form.cleaned_data['numAvail']
                bus.save()
                response['msg'] = 'successfully'
                response['error_num'] = 0
            except Exception as e:
                response['msg'] = 'hotel does not exsited'
                response['error_num'] = 1
        else:
            response['msg'] = 'form is not valid'
            response['error_num'] = 2

    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 3
    return JsonResponse(response)