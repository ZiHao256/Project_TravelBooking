from django import forms


class CustLoginForm(forms.Form):
    custID = forms.IntegerField()
    password = forms.CharField()


class AdminLoginForm(forms.Form):
    adminID = forms.IntegerField()
    password = forms.CharField()


class AdminRegisterForm(forms.Form):
    adminName = forms.CharField()
    adminID = forms.IntegerField()
    password1 = forms.CharField()
    password2 = forms.CharField()


class CustRegisterForm(forms.Form):
    custName = forms.CharField()
    custID = forms.IntegerField()
    password1 = forms.CharField()
    password2 = forms.CharField()


class CustChangeForm(forms.Form):
    custName = forms.CharField()
    custID = forms.IntegerField()
    password = forms.CharField()
    balance = forms.IntegerField()


class AdminChangeForm(forms.Form):
    adminName = forms.CharField()
    adminID = forms.IntegerField()
    password = forms.CharField()


class LOCATIONSForm(forms.Form):
    location = forms.CharField()
    riskLevel = forms.CharField()


class FLIGHTSForm(forms.Form):
    flightNum = forms.CharField()
    price = forms.IntegerField()
    numSeats = forms.IntegerField()
    numAvail = forms.IntegerField()
    FromCity = forms.CharField()
    ArivCity = forms.CharField()


class HOTELSForm(forms.Form):
    location = forms.CharField()
    price = forms.IntegerField()
    numRooms = forms.IntegerField()
    numAvail = forms.IntegerField()


class BUSESForm(forms.Form):
    location = forms.CharField()
    price = forms.IntegerField()
    numSeats = forms.IntegerField()
    numAvail = forms.IntegerField()


class RES_FLIGHT_Form(forms.Form):
    resvKey = forms.IntegerField()
    # custID = forms.IntegerField(label='custID')
    flightNum = forms.CharField()


class RES_HOTEL_Form(forms.Form):
    resvKey = forms.IntegerField()
    # custID = forms.IntegerField(label='custID')
    hotelLocation = forms.CharField()


class RES_BUS_Form(forms.Form):
    resvKey = forms.IntegerField()
    # custID = forms.IntegerField(label='custID')
    busLocation = forms.CharField()
