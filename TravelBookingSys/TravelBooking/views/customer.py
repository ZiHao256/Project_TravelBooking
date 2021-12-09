# Create your views here.
import json
from datetime import datetime

from django.core import serializers
from django.db.models import Q, F
from django.forms.models import model_to_dict
from django.http import JsonResponse, response
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from TravelBooking.forms import *
from TravelBooking.models import *


def object_to_json(obj):
    return dict([(kk, obj.__dict__[kk]) for kk in obj.__dict__.keys() if kk != "_state"])


@csrf_exempt
@require_http_methods(['GET'])
def deposit(request):
    response = {}
    try:
        custID = request.session.get('custID')
        customer = CUSTOMERS.objects.get(custID=custID)
        print(request.GET.get('balance'))
        print(type(request.GET.get('balance')))
        customer.balance += int(request.GET.get('balance'))
        customer.save()
        response['msg'] = '充值成功'
        response['error_num'] = 0
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)


# 预定FLIGHT, BUS, HOTEL
@csrf_exempt
@require_http_methods(['POST'])
def reserve_flight(request):
    response = {}
    if not request.session.get('is_login', None):
        response['msg'] = 'you must login'
        response['error_num'] = 1
        return JsonResponse(response)
    try:
        res_flight_form = RES_FLIGHT_Form(request.POST)
        if res_flight_form.is_valid():
            custID = request.session.get('custID')
            flightNum = res_flight_form.cleaned_data['flightNum']
            flight = FLIGHTS.objects.get(flightNum=flightNum)
            customer = CUSTOMERS.objects.get(custID=request.session.get('custID'))
            # 剩余座位是否足够
            if flight.numAvail > 0:
                flight.numAvail -= 1
                # 余额是否足够
                if customer.balance - flight.price >= 0:
                    customer.balance -= flight.price
                    res_flight = RES_FLIGHT(
                        custID=CUSTOMERS.objects.get(custID=custID),
                        flightNum=FLIGHTS.objects.get(flightNum=flightNum),
                        resStatus='已预约',
                        buildTime=datetime.now()
                    )
                    res_flight.save()
                    flight.save()
                    customer.save()

                    res_key = res_flight.resvKey
                    res_flightNum = res_flight.flightNum_id
                    res_from = FLIGHTS.objects.get(flightNum=res_flightNum).FromCity_id
                    res_to = FLIGHTS.objects.get(flightNum=res_flightNum).ArivCity_id
                    response['msg'] = '预约 ' + str(res_key) + ' flight(' + str(res_flightNum) + ') from ' + str(
                        res_from) + ' to ' + str(res_to) + ' 成功'
                    response['error_num'] = 0
                else:
                    response['msg'] = '余额不足！'
                    response['error_num'] = 1
            else:
                response['msg'] = '座位已满！'
                response['error_num'] = 1
        else:
            response['msg'] = 'form is not valid'
            response['error_num'] = 0
            JsonResponse(response)
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)


@csrf_exempt
@require_http_methods(['POST'])
def reserve_hotel(request):
    response = {}
    if not request.session.get('is_login', None):
        response['msg'] = 'you must login'
        response['error_num'] = 1
        return JsonResponse(response)
    try:
        res_hotel_form = RES_HOTEL_Form(request.POST)
        if res_hotel_form.is_valid():
            custID = request.session['custID']
            hotel_loc = res_hotel_form.cleaned_data['hotelLocation']
            hotel = HOTELS.objects.get(location=hotel_loc)
            customer = CUSTOMERS.objects.get(custID=custID)
            # 剩余房间是否足够
            if hotel.numAvail > 0:
                hotel.numAvail -= 1
                # 余额是否足够
                if customer.balance-hotel.price >0:
                    customer.balance -= hotel.price
                    res_hotel = RES_HOTEL(
                        custID=CUSTOMERS.objects.get(custID=custID),
                        hotelLocation=LOCATIONS.objects.get(location=hotel_loc),
                        resStatus='已预约',
                        buildTime=datetime.now()
                    )
                    customer.save()
                    hotel.save()
                    res_hotel.save()
                    response['msg'] = '预约 hotel 成功'
                    response['error_num'] = 0
                else:
                    response['msg'] = '余额不足'
                    response['error_num'] = 1
            else:
                response['msg'] = '座位已满'
                response['error_num'] = 1
        else:
            response['msg'] = 'form is not valid'
            response['error_num'] = 1
            JsonResponse(response)
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)


@csrf_exempt
@require_http_methods(['POST'])
def reserve_bus(request):
    response = {}
    if not request.session.get('is_login', None):
        response['msg'] = 'you must login'
        response['error_num'] = 1
        return JsonResponse(response)
    try:
        res_bus_form = RES_BUS_Form(request.POST)
        if res_bus_form.is_valid():
            custID = request.session['custID']
            bus_loc = res_bus_form.cleaned_data['busLocation']

            bus = BUS.objects.get(location=bus_loc)
            customer = CUSTOMERS.objects.get(custID=custID)
            if bus.numAvail > 0:
                bus.numAvail -= 1
                if customer.balance - bus.price > 0:
                    customer.balance -= bus.price
                    res_bus = RES_BUS(
                        custID=CUSTOMERS.objects.get(custID=custID),
                        busLocation=LOCATIONS.objects.get(location=bus_loc),
                        resStatus='已预约',
                        buildTime=datetime.now()
                    )
                    bus.save()
                    customer.save()
                    res_bus.save()
                    resKey = res_bus.resvKey
                    res_loc = res_bus.busLocation_id
                    response['msg'] = '预约 ' + str(resKey) + ' bus to ' + str(res_loc) + ' 成功'
                    response['error_num'] = 0
                else:
                    response['msg'] = '余额不足'
                    response['error_num'] = 1
            else:
                response['msg'] = '座位已满'
                response['error_num'] = 1
        else:
            response['msg'] = 'form is not valid'
            response['error_num'] = 0
            JsonResponse(response)
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)


# 展示flight, hotel, bus订单
@require_http_methods(['GET'])
def show_res_flight(request):
    response = {}
    print(request.session.get('custID'))
    try:
        if request.GET.get('resvKey') is not None:
            res_flight = RES_FLIGHT.objects.get(resvKey=request.GET.get('resvKey'))
            response['list'] = object_to_json(res_flight)

        else:
            res_flight = RES_FLIGHT.objects.filter(custID=request.session.get('custID'))
            listall = json.loads(serializers.serialize("json", res_flight))
            total = int(len(listall))
            pagesize = int(request.GET.get('pagesize'))
            pagenum = int(request.GET.get('pagenum'))
            # print(pagesize, pagenum)
            if pagesize > total:
                pagesize = total
            sort_ls = [listall[i:i + pagesize] for i in range(0, len(listall), pagesize)]
            response['list'] = sort_ls[pagenum - 1]
            response['total'] = total
        response['error_num'] = 0
        response['msg'] = 'success'
    except Exception as e:
        if str(e) == 'range() arg 3 must not be zero':
            response['msg'] = 'success'
            response['error_num'] = 0
        else:
            response['msg'] = str(e)
            response['error_num'] = 1
    return JsonResponse(response)


@require_http_methods(['GET'])
def show_res_hotel(request):
    response = {}
    try:
        if request.GET.get('resvKey') is not None:
            res_flight = RES_FLIGHT.objects.get(resvKey=request.GET.get('resvKey'))
            response['list'] = object_to_json(res_flight)

        else:
            res_hotel = RES_HOTEL.objects.filter(custID=request.session.get('custID'))
            listall = json.loads(serializers.serialize("json", res_hotel))
            total = int(len(listall))
            pagesize = int(request.GET.get('pagesize'))
            pagenum = int(request.GET.get('pagenum'))
            # print(pagesize, pagenum)
            if pagesize > total:
                pagesize = total
            sort_ls = [listall[i:i + pagesize] for i in range(0, len(listall), pagesize)]
            response['list'] = sort_ls[pagenum - 1]
            response['total'] = total
        response['error_num'] = 0
        response['msg'] = 'success'
    except Exception as e:
        if str(e) == 'range() arg 3 must not be zero':
            response['msg'] = 'success'
            response['error_num'] = 0
        else:
            response['msg'] = str(e)
            response['error_num'] = 1
    return JsonResponse(response)


@require_http_methods(['GET'])
def show_res_bus(request):
    response = {}
    try:
        if request.GET.get('resvKey') is not None:
            res_bus = RES_BUS.objects.get(resvKey=request.GET.get('resvKey'))
            response['list'] = object_to_json(res_bus)

        else:
            res_bus = RES_BUS.objects.filter(custID=request.session.get('custID'))
            listall = json.loads(serializers.serialize("json", res_bus))
            total = int(len(listall))
            pagesize = int(request.GET.get('pagesize'))
            pagenum = int(request.GET.get('pagenum'))
            # print(pagesize, pagenum)
            if pagesize > total:
                pagesize = total
            sort_ls = [listall[i:i + pagesize] for i in range(0, len(listall), pagesize)]
            response['list'] = sort_ls[pagenum - 1]
            response['total'] = total
        response['error_num'] = 0
        response['msg'] = 'success'
    except Exception as e:
        if str(e) == 'range() arg 3 must not be zero':
            response['msg'] = 'success'
            response['error_num'] = 0
        else:
            response['msg'] = str(e)
            response['error_num'] = 1
    return JsonResponse(response)


# 开始flight, hotel, bus订单
@csrf_exempt
@require_http_methods(['POST'])
def start_res_flight(request):
    response = {}
    print(request.POST)
    try:
        res_flight_form = RES_FLIGHT_Form(request.POST)
        response['msg'] = 'check'
        if res_flight_form.is_valid():
            res_flight = RES_FLIGHT.objects.get(resvKey=res_flight_form.cleaned_data['resvKey'])
            if res_flight.resStatus == '已预约':
                res_flight.resStatus = '订单已开始'
                res_flight.startTime = datetime.now()
                res_flight.save()

                res_key = res_flight.resvKey
                res_flightNum = res_flight.flightNum_id
                res_from = FLIGHTS.objects.get(flightNum=res_flightNum).FromCity_id
                res_to = FLIGHTS.objects.get(flightNum=res_flightNum).ArivCity_id

                response['msg'] = '预约 ' + str(res_key) + ' flight(' + str(res_flightNum) + ') from ' + str(
                    res_from) + ' to ' + str(res_to) + ' 开始'
                response['error_num'] = 0
            else:
                response['msg'] == '当前订单不是已预约'
                response['error_num'] = 1
        else:
            response['msg'] = 'form is not valid'
            response['error_num'] = 1
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1

    return JsonResponse(response)


@csrf_exempt
@require_http_methods(['POST'])
def start_res_hotel(request):
    response = {}
    try:
        res_hotel_form = RES_HOTEL_Form(request.POST)
        response['msg'] = 'check'
        if res_hotel_form.is_valid():
            res_hotel = RES_HOTEL.objects.get(resvKey=res_hotel_form.cleaned_data['resvKey'])
            if res_hotel.resStatus == '已预约':
                res_hotel.resStatus = '订单已开始'
                res_hotel.startTime = datetime.now()
                res_hotel.save()
                response['msg'] = 'res_hotel starts successfully'
                response['error_num'] = 0
            else:
                response['msg'] = '该订单不是已预约'
                response['error_num'] = 1
        else:
            response['msg'] = 'form is not valid'
            response['error_num'] = 1
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1

    return JsonResponse(response)


@csrf_exempt
@require_http_methods(['POST'])
def start_res_bus(request):
    response = {}
    try:
        res_bus_form = RES_BUS_Form(request.POST)
        response['msg'] = 'check'
        if res_bus_form.is_valid():
            res_bus = RES_BUS.objects.get(resvKey=res_bus_form.cleaned_data['resvKey'])
            if res_bus.resStatus == '已预约':
                res_bus.resStatus = '订单已开始'
                res_bus.startTime = datetime.now()
                res_bus.save()

                res_bus_resKey = res_bus.resvKey
                res_bus_loc = res_bus.busLocation_id
                response['msg'] = '预约 ' + str(res_bus_resKey) + ' bus to ' + str(res_bus_loc) + ' starts successfully'
                response['error_num'] = 0
            else:
                response['msg'] = '该订单不是已预约'
                response['error_num'] = 1
        else:
            response['msg'] = 'form is not valid'
            response['error_num'] = 1
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1

    return JsonResponse(response)


# 结束flight, hotel, bus订单
@csrf_exempt
@require_http_methods(['POST'])
def end_res_flight(request):
    response = {}
    try:
        res_flight_form = RES_FLIGHT_Form(request.POST)
        if res_flight_form.is_valid():
            res_flight = RES_FLIGHT.objects.get(resvKey=res_flight_form.cleaned_data['resvKey'])
            if res_flight.resStatus == '订单已开始':
                res_flight.endTime = datetime.now()
                res_flight.resStatus = '订单已完成'

                flight = FLIGHTS.objects.get(flightNum=res_flight.flightNum_id)
                flight.numAvail += 1

                flight.save()
                res_flight.save()

                res_key = res_flight.resvKey
                res_flightNum = res_flight.flightNum_id
                res_from = FLIGHTS.objects.get(flightNum=res_flightNum).FromCity_id
                res_to = FLIGHTS.objects.get(flightNum=res_flightNum).ArivCity_id
                response['msg'] = '预约 ' + str(res_key) + ' flight(' + str(res_flightNum) + ') from ' + str(
                    res_from) + ' to ' + str(res_to) + ' 完成'
                response['error_num'] = 0
            else:
                response['msg'] = '当前订单不是已开始'
                response['error_num'] = 1
        else:
            response['msg'] = 'form is not valid'
            response['error_num'] = 1
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1

    return JsonResponse(response)


@csrf_exempt
@require_http_methods(['POST'])
def end_res_hotel(request):
    response = {}
    try:
        res_hotel_form = RES_HOTEL_Form(request.POST)
        if res_hotel_form.is_valid():
            res_hotel = RES_HOTEL.objects.get(resvKey=res_hotel_form.cleaned_data['resvKey'])
            if res_hotel.resStatus == '订单已开始':
                res_hotel.endTime = datetime.now()
                res_hotel.resStatus = '订单已完成'

                hotel = HOTELS.objects.get(location=res_hotel.hotelLocation_id)
                hotel.numAvail += 1

                hotel.save()
                res_hotel.save()

                resvKey = res_hotel.resvKey
                response['msg'] = 'res_hotel ' + str(resvKey) + ' ends successfully'
                response['error_num'] = 0
            else:
                response['msg'] = '当前订单不是已开始'
                response['error_num'] = 1
        else:
            response['msg'] = 'form is not valid'
            response['error_num'] = 1
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1

    return JsonResponse(response)


@csrf_exempt
@require_http_methods(['POST'])
def end_res_bus(request):
    response = {}
    try:
        res_bus_form = RES_BUS_Form(request.POST)
        if res_bus_form.is_valid():
            res_bus = RES_BUS.objects.get(resvKey=res_bus_form.cleaned_data['resvKey'])
            if res_bus.resStatus == '订单已开始':
                res_bus.endTime = datetime.now()
                res_bus.resStatus = '订单已完成'

                bus = BUS.objects.get(location=res_bus.busLocation_id)
                bus.numAvail += 1

                bus.save()
                res_bus.save()

                resvKey = res_bus.resvKey
                resv_loc = res_bus.busLocation_id
                response['msg'] = '预定 ' + str(resvKey) + ' bus to ' + str(resv_loc) + ' ends successfully'
                response['error_num'] = 0
            else:
                response['msg'] = '当前订单不是已开始'
                response['error_num'] = 1
        else:
            response['msg'] = 'form is not valid'
            response['error_num'] = 1
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1

    return JsonResponse(response)


# 旅游路线
@require_http_methods(['GET'])
def show_lines(request):
    response = {}
    try:
        if request.session.get('is_login'):

            resvKey = int(request.GET.get('resvKey'))
            custID = request.session.get('custID')
            res_flights = RES_FLIGHT.objects.filter(Q(custID=custID) and Q(resvKey__gte=resvKey))

            complete_line_list = []  # 完整的路线
            incomplete_line_list = []  # 不完整的路线
            line = []  # 旅游路线
            result = []
            count = 1  # 记录已加入路线的res个数

            line.append(str(FLIGHTS.objects.get(flightNum=res_flights[0].flightNum_id).FromCity_id))
            line.append(str(FLIGHTS.objects.get(flightNum=res_flights[0].flightNum_id).ArivCity_id))
            result.append(res_flights[0])

            for i in res_flights:
                flight = FLIGHTS.objects.get(flightNum=i.flightNum_id)
                if flight.FromCity_id == line[len(line) - 1]:
                    line.append(flight.ArivCity_id)
                    result.append(i)

            if line[len(line) - 1] == line[0]:
                is_complete = 1
            else:
                is_complete = 0

            listall = json.loads(serializers.serialize("json", result))
            total = int(len(listall))
            pagesize = int(request.GET.get('pagesize'))
            pagenum = int(request.GET.get('pagenum'))

            if pagesize > total:
                pagesize = total
            sort_ls = [listall[i:i + pagesize] for i in range(0, len(listall), pagesize)]

            response['is_complete'] = is_complete
            response['line'] = line
            response['list'] = sort_ls[pagenum - 1]
            response['msg'] = 'successfully'
            response['error_num'] = 0
        else:
            response['msg'] = 'you must login'
            response['error_num'] = 1
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1

    return JsonResponse(response)
