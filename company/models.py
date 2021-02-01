from django.db import models

# Create your models here.


class Address(models.Model):
    StateChoice = [('AL', 'Alabama'),
                   ('AK', 'Alaska'),
                   ('AZ', 'Arizona'),
                   ('AR', 'Arkansas'),
                   ('CA', 'California'),
                   ('CO', 'Colorado'),
                   ('CT', 'Connecticut'),
                   ('DE', 'Delaware'),
                   ('DC', 'District of Columbia'),
                   ('FL', 'Florida'),
                   ('GA', 'Georgia'),
                   ('HI', 'Hawai\'i'),
                   ('ID', 'Idaho'),
                   ('IL', 'Illinois'),
                   ('IN', 'Indiana'),
                   ('IA', 'Iowa'),
                   ('KS', 'Kansas'),
                   ('KY', 'Kentucky'),
                   ('LA', 'Louisiana'),
                   ('ME', 'Maine'),
                   ('MD', 'Maryland'),
                   ('MA', 'Massachusetts'),
                   ('MI', 'Michigan'),
                   ('MN', 'Minnesota'),
                   ('MS', 'Mississippi'),
                   ('MO', 'Missouri'),
                   ('MT', 'Montana'),
                   ('NE', 'Nebraska'),
                   ('NV', 'Nevada'),
                   ('NH', 'New Hampshire'),
                   ('NJ', 'New Jersey'),
                   ('NM', 'New Mexico'),
                   ('NY', 'New York'),
                   ('NC', 'North Carolina'),
                   ('ND', 'North Dakota'),
                   ('OH', 'Ohio'),
                   ('OK', 'Oklahoma'),
                   ('OR', 'Oregon'),
                   ('PA', 'Pennsylvania'),
                   ('PR', 'Puerto Rico'),
                   ('RI', 'Rhode Island'),
                   ('SC', 'South Carolina'),
                   ('SD', 'South Dakota'),
                   ('TN', 'Tennessee'),
                   ('TX', 'Texas'),
                   ('UT', 'Utah'),
                   ('VT', 'Vermont'),
                   ('VA', 'Virgina'),
                   ('WA', 'Washington'),
                   ('WV', 'West Virginia'),
                   ('WI', 'Wisconsin'),
                   ('WY', 'Wyoming')]
    state = models.CharField(max_length=255, choices=StateChoice)
    city = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    street2 = models.CharField(max_length=255, null=True)
    zipCode = models.PositiveIntegerField(max_length=5)

    def __str__(self):
        return self.street + ' ' + self.street2 + ' ' + self.city + ' ' + self.state


class WarehouseCustomer(models.Model):
    storageRate = models.DecimalField(max_digits=5, decimal_places=2)
    DisposalRate = models.DecimalField(max_digits=5, decimal_places=2)


class Customer(models.Model):
    firstName = models.CharField(max_length=255)
    lastName = models.CharField(max_length=255)
    CustAddress = models.ForeignKey(Address, related_name='CustAddress', on_delete=models.CASCADE)
    warCust = models.ForeignKey(WarehouseCustomer, related_name='warCust', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.firstName + ' ' + self.lastName


class Warehouse(models.Model):
    #Create a link to a warehouse administrator perhaps
    whName = models.CharField(max_length=255)
    regularFTE = models.PositiveIntegerField()
    TotalFTE = models.PositiveIntegerField()
    shelfXYZ = models.PositiveIntegerField()
    whAddress = models.ForeignKey(Address, related_name='whAddress', on_delete=models.CASCADE)

    def __str__(self):
        return self.whName


class Employee(models.Model):
    #Add various HR values
    addID = models.ForeignKey(Address, related_name='addID', on_delete=models.CASCADE)
    firstName = models.CharField(max_length=255)
    lastName = models.CharField(max_length=255)
    SSN = models.CharField(max_length=255)
    hireDate = models.DateField()


class ContingentWorker(models.Model):
    #Add various HR values
    hireDate = models.DateField()
    conName = models.CharField(max_length=255)
    WorkStart = models.DateField()
    workEnd = models.DateField()
    FTE = models.DecimalField(max_digits=3, decimal_places=2)
    workSchedule = models.CharField(max_length=255)
    payRate = models.DecimalField(max_digits=5, decimal_places=2)
    ContEmpRef = models.ForeignKey(Employee, related_name='ContEmpRef', on_delete=models.CASCADE, null=True)
    whCon = models.ForeignKey(Warehouse, related_name='whCon', on_delete=models.CASCADE)


class Position(models.Model):
    #Add compensation information
    posName = models.CharField(max_length=255)
    FTE = models.DecimalField(max_digits=3, decimal_places=2)
    workSchedule = models.CharField(max_length=255)
    payRate = models.DecimalField(max_digits=5, decimal_places=2)
    empRef = models.ForeignKey(Employee, related_name='empRef', on_delete=models.CASCADE, null=True)
    whPos = models.ForeignKey(Warehouse, related_name='whPos', on_delete=models.CASCADE)


class Invoice(models.Model):
    #consolidate dates, create distinct status values, handle amount paid better
    invDate = models.DateField()
    saleType = models.CharField(max_length=255)
    fulfillmentDate = models.DateField(null=True)
    DatePaid = models.DateField(null=True)
    InvoiceStatus = models.CharField(max_length=255)
    amountPaid = models.DecimalField(max_digits=10, decimal_places=2)
    #amountRemaining
    payingCust = models.ForeignKey(Customer, related_name='payingCust', on_delete=models.CASCADE)
    LastUpdated = models.DateField(null=True)
    #Add a reference to Order and a reference to a customer
    #total amount
    #paid?


class Orders(models.Model):
    #distinct values for status
    orderStatus = models.CharField(max_length=255)
    DateRequested = models.DateField()
    orderingCust = models.ForeignKey(Customer, related_name='orderingCust', on_delete=models.CASCADE)
    invRef = models.ForeignKey(Invoice, related_name='invRef', on_delete=models.CASCADE)


class Item(models.Model):
    itemName = models.CharField(max_length=255)
    description = models.TextField(max_length=1000)
    inventoryRate = models.DecimalField(max_digits=5, decimal_places=2)
    itemValue = models.DecimalField(max_digits=5, decimal_places=2)
    saleRate = models.DecimalField(max_digits=5, decimal_places=2)
    VolumeReq = models.PositiveIntegerField()

    def __str__(self):
        return self.itemName


class Shelf(models.Model):
    xLoc = models.PositiveIntegerField()
    yLoc = models.PositiveIntegerField()
    zLoc = models.PositiveIntegerField()
    shelfCapacity = models.PositiveIntegerField()
    capacityUsed = models.PositiveIntegerField(null=True)
    StorageType = models.CharField(max_length=255)
    storedItem = models.ForeignKey(Item, related_name='storedItem', on_delete=models.CASCADE, null=True)
    whLoc = models.ForeignKey(Warehouse, related_name='whLoc', on_delete=models.CASCADE)


class LineItem(models.Model):
    #Need to fix how dates work for this, maintain fixed status types
    LIchoices = [('Store', 'Store'), ('Purchase', 'Purchase'), ('FireSale', 'Fire Sale'), ('Disposal', 'Disposal')]
    lineItemType = models.CharField(max_length=255, choices=LIchoices)
    shippingLoc = models.ForeignKey(Address,related_name='shippingLoc', on_delete=models.CASCADE)
    dateRequested = models.DateField()
    itemID = models.ForeignKey(Item, related_name='itemID', on_delete=models.CASCADE)
    lineItemStatus = models.CharField(max_length=255)
    amount = models.PositiveIntegerField()
    ordRefMain = models.ForeignKey(Orders, related_name='ordRefMain', on_delete=models.CASCADE)
    refWHouse = models.ForeignKey(Warehouse, related_name='refWHouse', on_delete=models.CASCADE, null=True)
    #Add Warehouse to the lineItem
    #Set status to picklist options
    #might need to set a warehouse that this is sent or picked up from


class Store(models.Model):
    storeName = models.CharField(max_length=255)
    location = models.ForeignKey(Address, related_name='location', on_delete=models.CASCADE)
    dateOpened = models.DateField()
    refCust = models.ForeignKey(Customer, related_name='refCust', on_delete=models.CASCADE)

    def __str__(self):
        return self.storeName

#Give stores an itemList
# #irrelevant
# class StoreOwned(models.Model):
#     refStore = models.ForeignKey(Store, related_name='refStore', on_delete=models.CASCADE)
#     refCust = models.ForeignKey(Customer, related_name='refCust', on_delete=models.CASCADE)


class OrderAction(models.Model):
    #Action needs fixed items, amount moved will take many changes
    batchNumber = models.PositiveIntegerField(default=0)
    refEmp = models.ForeignKey(Employee, related_name='refEmp', on_delete=models.CASCADE)
    refLineItem = models.ForeignKey(LineItem, related_name='refLineItem', on_delete=models.CASCADE)
    refShelf = models.ForeignKey(Shelf, related_name='refShelf', on_delete=models.CASCADE, null=True)
    fulfillmentStart = models.DateTimeField(null=True)
    Action = models.CharField(max_length=255)
    fulfillmentEnd = models.DateTimeField(default='2100-01-01')
    amountMoved = models.PositiveIntegerField(default=0)
    #Probably need to add an "number of item moved"
    #This is technically a lineItemAction

#unnecessary
# class OrderList(models.Model):
#     LineItemRef = models.ForeignKey(LineItem, related_name='LineItemRef', on_delete=models.CASCADE)
#     ordRefMain = models.ForeignKey(Orders, related_name='ordRefMain', on_delete=models.CASCADE)

#I have not decided if an invList is unnecessary yet#


class FulfillmentManager(models.Model):
    mgrRef = models.ForeignKey(Employee, related_name='mgrRef', on_delete=models.CASCADE)
    ordRefFul = models.ForeignKey(Orders, related_name='ordRefFul', on_delete=models.CASCADE)
    timeAssigned = models.DateTimeField()
    timeFulfilled = models.DateTimeField()


#Added an intermediary shelf table
class ShelfMovement(models.Model):
    actionRef = models.ForeignKey(OrderAction, related_name='actionRef', on_delete=models.CASCADE)
    shelfRef = models.ForeignKey(Shelf, related_name='shelfRef', on_delete=models.CASCADE)
    amtMoved = models.PositiveIntegerField()


class StoreInventory(models.Model):
    #Allow for changes
    amount = models.PositiveIntegerField(default=0)
    refItem = models.ForeignKey(Item, related_name='refItem', on_delete=models.CASCADE)
    refStore = models.ForeignKey(Store, related_name='refStore', on_delete=models.CASCADE)


class StoreOrder(models.Model):
    #Allow for removal and such
    endCust = models.ForeignKey(Customer, related_name='endCust', on_delete=models.CASCADE)
    itemOrd = models.ForeignKey(Item, related_name='itemOrd', on_delete=models.CASCADE)
    amtOrd = models.PositiveIntegerField()
    strOrdSts = models.CharField(max_length=255)
#
# CustID does not need to be on Invoices
#
#Okay, remove the intermediate models in

# class CustOrders(models.Model):
#     customerRef = models.ForeignKey(Customer, related_name='customerRef', on_delete=models.CASCADE)
#     orderRef = models.ForeignKey(Orders, related_name='orderRef', on_delete=models.CASCADE)
