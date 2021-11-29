from django import forms


class CustLoginForm(forms.Form):
    custID = forms.IntegerField(label="user_id")
    password = forms.CharField(label="password", max_length=50, widget=forms.PasswordInput)


class AdminLoginForm(forms.Form):
    adminID = forms.IntegerField(label="user_id")
    password = forms.CharField(label="password", max_length=50, widget=forms.PasswordInput)


class AdminRegisterForm(forms.Form):
    name = forms.CharField(label="name", max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
    adminID = forms.IntegerField(label="admin_id", widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label="password", max_length=256,
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="ensure password", max_length=256,
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class CustRegisterForm(forms.Form):
    name = forms.CharField(label="name", max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
    custID = forms.IntegerField(label="admin_id", widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label="password", max_length=256,
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="ensure password", max_length=256,
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    # balance = forms.IntegerField(label="balance", widget=forms.TextInput(attrs={'class': 'form-control'}))


class LOCATIONSForm(forms.Form):
    location = forms.CharField(label="location",  max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
    riskLevel = forms.CharField(label='riskLevel',  max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))


class FLIGHTSForm(forms.Form):
    flightNum = forms.CharField(label="flightNum",  max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
    price = forms.IntegerField(label='price')
    numSeats = forms.IntegerField(label='numSeats')
    numAvail = forms.IntegerField(label='numAvail')
    FromCity = forms.CharField(label="location",  max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
    ArivCity = forms.CharField(label="location",  max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))



class HOTELSForm(forms.Form):
    location = forms.CharField(label="location",  max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
    price = forms.IntegerField(label='price')
    numRooms = forms.IntegerField(label='numRooms')
    numAvail = forms.IntegerField(label='numAvail')


class BUSESForm(forms.Form):
    location = forms.CharField(label="location",  max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
    price = forms.IntegerField(label='price')
    numSeats = forms.IntegerField(label='numSeats')
    numAvail = forms.IntegerField(label='numAvail')


class RES_FLIGHT_Form(forms.Form):
    resvKey = forms.IntegerField(label='resvKey')
    custID = forms.IntegerField(label='custID')
    flightNum = forms.CharField(label="location",  max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))


class RES_HOTEL_Form(forms.Form):
    resvKey = forms.IntegerField(label='resvKey')
    custID = forms.IntegerField(label='custID')
    hotelLocation = forms.CharField(label="location",  max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))


class RES_BUS_Form(forms.Form):
    resvKey = forms.IntegerField(label='resvKey')
    custID = forms.IntegerField(label='custID')
    busLocation = forms.CharField(label="location",  max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))


