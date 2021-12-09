# Create your views here.
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from TravelBooking.forms import AdminLoginForm, CustLoginForm, AdminRegisterForm, CustRegisterForm
from TravelBooking.models import ADMINS, CUSTOMERS


def object_to_json(obj):
    return dict([(kk, obj.__dict__[kk]) for kk in obj.__dict__.keys() if kk != "_state"])

# USER
def login(request):
    return render(request, 'index.html')


@csrf_exempt
@require_http_methods("POST")
def admin_login(request):
    response = {}
    if request.session.get('is_login', None):
        response['msg'] = 'this administer.py has logined'
        response['error_num'] = 1
        response['adminID'] = request.session.get('adminID')
        return JsonResponse(response)

    if request.method == 'POST':
        login_form = AdminLoginForm(request.POST)
        response['msg'] = 'please check '
        response['error_num'] = 1

        if login_form.is_valid():
            adminID = login_form.cleaned_data['adminID']
            password = login_form.cleaned_data['password']
            try:
                admin = ADMINS.objects.get(adminID=adminID)
                if admin.password == password:
                    request.session['is_login'] = True
                    request.session['adminID'] = admin.adminID
                    request.session['name'] = admin.adminName

                    response['msg'] = 'login successfully'
                    response['error_num'] = 0
                    return JsonResponse(response)
                else:
                    response['msg'] = 'login failed: wrong password'
                    response['error_num'] = 2
            except Exception as e:
                response['msg'] = str(e)
                response['error_num'] = 3
        else:
            response['msg'] = 'form is not valid'
            response['error_num'] = 1
        return JsonResponse(response)

    return JsonResponse(response)


@csrf_exempt
@require_http_methods("POST")
def cust_login(request):
    response = {}
    if request.session.get('is_login', None):
        response['msg'] = 'this customer has logined'
        response['error_num'] = 1
        response['custID'] = request.session.get('csutID')
        return JsonResponse(response)

    if request.method == 'POST':
        login_form = CustLoginForm(request.POST)
        response['msg'] = 'please check '

        if login_form.is_valid():
            custID = login_form.cleaned_data['custID']
            password = login_form.cleaned_data['password']
            try:
                customer = CUSTOMERS.objects.get(custID=custID)
                if customer.password == password:
                    request.session['is_login'] = True
                    request.session['custID'] = customer.custID
                    request.session['name'] = customer.custName

                    response['msg'] = 'login successfully'
                    response['error_num'] = 0
                    return JsonResponse(response)
                else:
                    response['msg'] = 'login failed: wrong password'
                    response['error_num'] = 2
            except Exception as e:
                response['msg'] = str(e)
                response['error_num'] = 3

        return JsonResponse(response)

    return JsonResponse(response)


@csrf_exempt
@require_http_methods("POST")
def admin_register(request):
    response = {}

    if request.method == "POST":
        print(request.POST)
        register_form = AdminRegisterForm(request.POST)
        response['msg'] = 'please check content!'
        response['error_num'] = 1

        if register_form.is_valid():
            adminID = register_form.cleaned_data['adminID']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            name = register_form.cleaned_data['adminName']
            if password1 != password2:
                response['msg'] = 'password is not consistent！'
                return JsonResponse(response)
            else:
                same_admin = {}
                try:
                    same_admin = ADMINS.objects.get(adminID=adminID)
                    response['msg'] = 'this adminID has existed！'
                    response['error_num'] = 2
                    return JsonResponse(response)

                except Exception as e:

                    new_admin = ADMINS(
                        adminID=adminID,
                        adminName=name,
                        password=password1
                    )
                    response['msg'] = 'register successfully!'
                    response['error_num'] = 3
                    new_admin.save()
                return JsonResponse(response)
        else:
            response['msg'] = 'form is not valid'
            response['error_num'] = 2
        return JsonResponse(response)
    return JsonResponse(response)


@csrf_exempt
@require_http_methods("POST")
def cust_register(request):
    response = {}
    print(request.POST)
    if request.method == "POST":
        register_form = CustRegisterForm(request.POST)
        response['msg'] = 'please check content!'
        response['error_num'] = 1

        if register_form.is_valid():
            custID = register_form.cleaned_data['custID']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            name = register_form.cleaned_data['custName']
            if password1 != password2:
                response['msg'] = 'password is not consistent！'
                return JsonResponse(response)
            else:
                same_admin = {}
                try:
                    same_customer = CUSTOMERS.objects.get(custID=custID)
                    response['msg'] = 'this custID has existed！'
                    response['error_num'] = 2
                    return JsonResponse(response)

                except Exception as e:

                    new_cust = CUSTOMERS(
                        custID=custID,
                        custName=name,
                        password=password1,
                        balance=0
                    )
                    response['msg'] = 'register successfully!'
                    response['error_num'] = 3
                    new_cust.save()
                return JsonResponse(response)
        else:
            response['msg'] = 'form is not valid'
            response['error_num'] = 2
        return JsonResponse(response)
    return JsonResponse(response)


@csrf_exempt
@require_http_methods(['GET'])
def logout(request):
    response = {}
    try:
        if not request.session.get('is_login'):
            response['msg'] = 'have not login'
            response['error_num'] = 0
            return JsonResponse(response)
        request.session.flush()
        response['msg'] = 'logout successfully'
        response['error_num'] = 1
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 2
    return JsonResponse(response)