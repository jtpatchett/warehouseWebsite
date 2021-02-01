from django import forms
from .models import *
from django.db.models import Q


class OrderForm(forms.ModelForm):
    class Meta:
        model = Orders
        fields = ['DateRequested', 'orderingCust']

class DateOrderForm(forms.ModelForm):
    class Meta:
        model = Orders
        fields = ['DateRequested']

class AddLineItem(forms.ModelForm):
    OrderRef = forms.IntegerField()
    CustomerRef = forms.IntegerField()

    class Meta:
        model = LineItem
        fields = ['lineItemType', 'shippingLoc', 'dateRequested', 'itemID', 'amount']


class createItem(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['itemName', 'description', 'inventoryRate', 'saleRate', 'VolumeReq', 'itemValue']

#Below here these forms need to be implemented


class AddEmployee(forms.ModelForm):
#Need to add status to this form+
    class Meta:
        model = Employee
        fields = ['addID', 'firstName', 'lastName', 'SSN']


class ProcessLineItem(forms.ModelForm):
    refLineItem = forms.ModelChoiceField(queryset=LineItem.objects.all())
    refShelf = forms.ModelChoiceField(queryset=Shelf.objects.all())
    class Meta:
        model = OrderAction
        fields = ['batchNumber', 'refEmp', 'fulfillmentStart', 'amountMoved', 'Action']


class SetOAWarehouse(forms.Form):
    whobj = forms.ModelChoiceField(queryset=Warehouse.objects.all())
    liobj = forms.ModelChoiceField(queryset=LineItem.objects.filter(lineItemStatus='Not Assigned'))


class shipItem(forms.Form):
    liobj = forms.ModelChoiceField(queryset=LineItem.objects.filter(lineItemStatus='Assigned', lineItemType='Sale'))


class shipOrderAction(forms.Form):
    AssignShelf = forms.ModelChoiceField(queryset=Shelf.objects.all())
    BatchNumber = forms.IntegerField()
    liobj2 = forms.ModelChoiceField(queryset=LineItem.objects.filter(lineItemStatus='Assigned', lineItemType='Sale'))
    fulDate = forms.DateField()
    refdEmp = forms.ModelChoiceField(queryset=Employee.objects.all())


class GetInvoice(forms.Form):
    gotINV = forms.ModelChoiceField(queryset=Invoice.objects.all())


class GetWareHouse(forms.Form):
    gotWH = forms.ModelChoiceField(queryset=Warehouse.objects.all())


class ChangeOrderAction(forms.Form):
    gotBatch = forms.ModelChoiceField(queryset=OrderAction.objects.filter(Q(Action='Assigned')))
    class Meta:
        model = OrderAction
        fields = ['refEmp', 'Action', 'fulfillmentEnd']


class ChangeOrderActionStatus(forms.Form):
    gotBatch = forms.ModelChoiceField(queryset=OrderAction.objects.filter(Q(Action='Assigned')))
    class Meta:
        model = OrderAction
        fields = ['refEmp', 'Action', 'fulfillmentEnd']


class getCustID(forms.ModelForm):
    cust = forms.ModelChoiceField(queryset=Customer.objects.all())
    class Meta:
        model = Customer
        fields = []


class EnableStore(forms.ModelForm):
    class Meta:
        model = Store
        fields = ['storeName', 'dateOpened', 'refCust']


class CreateAddress(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['street', 'street2', 'city', 'state']


class InvoiceStatusUpdate(forms.Form):
    invChoice = forms.ModelChoiceField(queryset=Invoice.objects.all())
    InvoiceStatus = forms.CharField(max_length=255)
    RevisionDate = forms.DateField()

class endUserCustomer(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['firstName', 'lastName', 'CustAddress']

class addStoreOrder(forms.ModelForm):
    class Meta:
        model = StoreOrder
        fields = ['endCust', 'itemOrd', 'amtOrd']

class changeItemInventory(forms.ModelForm):
    operation = forms.CharField(max_length=255)
    class Meta:
        model = StoreInventory
        fields = ['refStore', 'refItem', 'amount']


class AddPosition(forms.ModelForm):
    class Meta:
        model = Position
        fields = ['posName', 'FTE', 'workSchedule', 'payRate', 'empRef', 'whPos']


class AddContingent(forms.ModelForm):
    class Meta:
        model = ContingentWorker
        fields = ['conName', 'FTE', 'workSchedule', 'payRate', 'ContEmpRef', 'whCon', 'workEnd', 'WorkStart']
