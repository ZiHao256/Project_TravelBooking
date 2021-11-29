from django.db import models


# Create your models here.

class ADMINS(models.Model):
    adminID = models.IntegerField(null=False, unique=True, primary_key=True)
    adminName = models.CharField(null=False, max_length=50)
    password = models.CharField(null=False, max_length=50)


class CUSTOMERS(models.Model):
    custID = models.IntegerField(null=False, unique=True, primary_key=True)
    custName = models.CharField(null=False, max_length=50)
    password = models.CharField(null=False, max_length=50)
    balance = models.IntegerField(null=False)

    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(balance=(models.F("balance")-0)), name='check_balance')
        ]


class LOCATIONS(models.Model):
    riskchoices = {
        (u'高', u'高'),
        (u'中', u'中'),
        (u'低', u'低')
    }
    location = models.CharField(null=False, unique=True, max_length=50, primary_key=True)
    riskLevel = models.CharField(null=False, choices=riskchoices, max_length=50, default='低')


class FLIGHTS(models.Model):
    flightNum = models.CharField(null=False, unique=True, max_length=50, primary_key=True)
    price = models.IntegerField(null=False)
    numSeats = models.IntegerField(null=False)
    numAvail = models.IntegerField(null=False)
    FromCity = models.ForeignKey('LOCATIONS', on_delete=models.CASCADE, null=False, related_name='FromCity')
    ArivCity = models.ForeignKey('LOCATIONS', on_delete=models.CASCADE, null=False, related_name='ArivCity')
    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(price=(models.F("price")-0)), name='check_f_price')
        ]


class HOTELS(models.Model):
    location = models.ForeignKey('LOCATIONS', on_delete=models.CASCADE, null=False, primary_key=True)
    price = models.IntegerField(null=False)
    numRooms = models.IntegerField(null=False)
    numAvail = models.IntegerField(null=False)
    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(price=(models.F("price")-0)), name='check_h_price')
        ]


class BUS(models.Model):
    location = models.ForeignKey('LOCATIONS', on_delete=models.CASCADE, null=False, primary_key=True)
    price = models.IntegerField(null=False)
    numSeats = models.IntegerField(null=False)
    numAvail = models.IntegerField(null=False)
    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(price=(models.F("price")-0)), name='check_b_price')
        ]


class RES_FLIGHT(models.Model):
    resvKey = models.IntegerField(null=False, unique=True, primary_key=True)
    custID = models.ForeignKey('CUSTOMERS', on_delete=models.CASCADE, null=False)
    flightNum = models.ForeignKey('FLIGHTS', on_delete=models.CASCADE, null=False)


class RES_HOTEL(models.Model):
    resvKey = models.IntegerField(null=False, unique=True, primary_key=True)
    custID = models.ForeignKey('CUSTOMERS', on_delete=models.CASCADE, null=False)
    hotelLocation = models.ForeignKey('LOCATIONS', on_delete=models.CASCADE, null=False)


class RES_BUS(models.Model):
    resvKey = models.IntegerField(null=False, unique=True, primary_key=True)
    custID = models.ForeignKey('CUSTOMERS', on_delete=models.CASCADE, null=False)
    busLocation = models.ForeignKey('LOCATIONS', on_delete=models.CASCADE, null=False)
