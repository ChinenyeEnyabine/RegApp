from django.db import models


class BillOperation(models.Model):
    billtype=(
        ("recharge_card","recharge_card"),
        ("data","data"),
        ("sme_data","sme_data"),
        # ("flight_booking","flight_booking"),
        # ("car_rentage","car_rentage"),
        ("electricity","electricity"),
        ("cabletv","cabletv")
    )

    billclass=models.CharField(max_length=250,choices=billtype,default='sme_data',null=True,blank=True)
    # airtime/data
    phone_no=models.CharField(max_length=14,null=True,blank=True)
    servicetype=(
        ("mtn","mtn"),
        ("globacom","globacom"),
        ("airtel","airtel"),
        ("9mobile","9mobile")
    )
    serviceops=models.CharField(max_length=100,choices=servicetype,default='mtn',null=True,blank=True)
    amount=models.IntegerField(null=True,blank=True)
    # for data
    dataplan=models.CharField(max_length=200,null=True,blank=True)
    rechargeplan=models.CharField(max_length=200,null=True,blank=True)

    # bookflight model

    # location=models.CharField(max_length=200,null=True,blank=True)
    # destination=models.CharField(max_length=200,null=True,blank=True)
    # departdate=models.DateField(auto_now=False,null=True,blank=True)
    # selectclass=(
    #     ("economy","economy"),
    #     ("firstclass","firstclass"),
    #     ("nostop","nostop"),
    #     ("others","others")
    # )
    # flightclass=models.CharField(max_length=100,choices=selectclass,default='economy',null=True,blank=True)
    # passenger=models.IntegerField(null=True,blank=True)

    # car rentage
    # cartype=models.CharField(max_length=200,default="toyota",null=True,blank=True),
    # dropoffdate=models.DateTimeField(auto_created=False)


    # for utilty
    meterno=models.CharField(max_length=100,null=True,blank=True)

    # for cabletv
    category=(
        ("dstv","dstv"),
        ("gotv","gotv"),
        ("showmax","showmax"),
        ("startimes","startimes")
    )
    serviceops=models.CharField(max_length=100,choices=category,default='gotv',null=True,blank=True)
    smart_card=models.CharField(max_length=100,null=True,blank=True)
    selectbouquet=models.CharField(max_length=100,null=True,blank=True)





#    from django.db import models

# class Flight(models.Model):
#     departure_location = models.CharField(max_length=100)
#     destination = models.CharField(max_length=100)
#     price = models.DecimalField(max_digits=10, decimal_places=2)

# class Booking(models.Model):
#     flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
#     adults = models.IntegerField()
#     children = models.IntegerField()
#     total_amount = models.DecimalField(max_digits=10, decimal_places=2)



   



