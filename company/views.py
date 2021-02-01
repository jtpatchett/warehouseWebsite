
from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from django.http import HttpResponse
import decimal
from .forms import *
import datetime
from django.db.models import Q, Count, Sum



# Create your views here.

def new_cust(request):
    #Simplify form, redirect back to homepage
    if request.method == 'POST':
        firstName = request.POST['firstName']
        lastName = request.POST['lastName']
        State = request.POST['State']
        City = request.POST['City']
        Street = request.POST['Street']
        Street2 = request.POST['Street2']
        dispRate = request.POST['DispRate']
        storRate = request.POST['StorRate']
        whcust = WarehouseCustomer.objects.create(
            storageRate=storRate,
            DisposalRate=dispRate
        )
        addr = Address.objects.create(
            state=State,
            city=City,
            street=Street,
            street2=Street2
        )
        cust = Customer.objects.create(
            firstName=firstName,
            lastName=lastName,
            CustAddress=addr,
            warCust=whcust
        )
    return render(request, 'newCust.html')


def adminHome(request):
    return render(request, 'WarehouseCustomerManagement.html')


def cust_info(request):
    #Redirect back to home page, create a drop down list or searchable
    if request.method == 'POST':
        cust_id = request.POST.get('id_custID', '')
        print(cust_id)
        try:
            custvalue = Customer.objects.get(id=cust_id)
            print(cust_id, custvalue)
            return render(request, 'CustInfo.html', {'custvalue': custvalue})
        except:
            Customer.DoesNotExist
            HttpResponse('This customer does not exist')
    return render(request, 'viewCustInfoSubmit.html')


def cust_info_page(request):
    return render(request, 'CustInfo.html')


def get_custPricing(request):
    #allow searching, redirect to homepage
    if request.method == 'POST':
        cust_id = request.POST.get('id_custID', '')
        try:
            custvalue = Customer.objects.get(id=cust_id)
            whcustval = WarehouseCustomer.objects.filter(id=custvalue.warCust.id)

            newDisp = request.POST['DispRate']
            newStor = request.POST['StorRate']
            whcustval.update(
            storageRate = decimal.Decimal(newStor),
            DisposalRate = decimal.Decimal(newDisp)
            )
            return render(request, 'custForPricing.html')

        except:
            Customer.DoesNotExist
            HttpResponse('This customer does not exist')
    return render(request, 'custForPricing.html')


def create_order(request):

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data['DateRequested'])
            dateVal = form.cleaned_data['DateRequested']
            dateVal = str(dateVal).split('-')
            dateVal = datetime.date(int(dateVal[0]), int(dateVal[1]), 1)
            print(dateVal)
            if len(Invoice.objects.filter(invDate=dateVal)) == 0:
                newInv = Invoice.objects.create(
                    invDate=dateVal,
                    amountPaid=0.00,
                    payingCust=form.cleaned_data['orderingCust'],
                    InvoiceStatus='Not Sent'
                )
                newOrder = Orders.objects.create(
                    orderStatus='Not Processed',
                    orderingCust=form.cleaned_data['orderingCust'],
                    invRef=newInv,
                    DateRequested=form.cleaned_data['DateRequested'],
                )
            else:
                invVal = Invoice.objects.filter(invDate=dateVal).first()
                newOrder = Orders.objects.create(
                    orderStatus='Not Processed',
                    orderingCust=form.cleaned_data['orderingCust'],
                    invRef=invVal,
                    DateRequested=form.cleaned_data['DateRequested']
                )
        return render(request, 'newOrder.html')
    else:
        form = OrderForm()
    return render(request, 'newOrder.html', {'form': form})


def customer_portal(request):
    return render(request, 'CustomerPortal.html')


def home(request):
    return render(request, 'CustomerPortal.html')

#
#To create order/INV relationship, when an invoice is created for the previous month
#Any orders in the previous month will be added to the invoice/order relationship
#


def add_lineitem(request):
    if request.method == 'POST':
        form = AddLineItem(request.POST)
        if form.is_valid():
            print(form.cleaned_data['OrderRef'])
            if Orders.objects.filter(id=int(form.cleaned_data['OrderRef'])):
                print('yes2')
                fields = form.cleaned_data
                referencedOrder = Orders.objects.filter(id=form.cleaned_data['OrderRef'])
                referencedOrder = referencedOrder.first()
                newLI = LineItem.objects.create(
                    lineItemType=fields['lineItemType'],
                    shippingLoc=fields['shippingLoc'],
                    dateRequested=fields['dateRequested'],
                    itemID=fields['itemID'],
                    lineItemStatus='Not Assigned',
                    amount=fields['amount'],
                    ordRefMain=referencedOrder

                )
                refdItem = Item.objects.filter(id=fields['itemID'].id).first()
                print(refdItem)
                addTotal = refdItem.itemValue * int(fields['amount'])
                referencedOrder.invRef.amountPaid = referencedOrder.invRef.amountPaid + addTotal
                referencedOrder.invRef.save()
                newLI.save()
            else:
                print('Tests are for nerds')
        else:
            print('I am not crying right now')
    else:
        form = AddLineItem()
    return render(request, 'addLineItem.html', {'form': form})


def create_item(request):
    if request.method == 'POST':
        form = createItem(request.POST)
        if form.is_valid():
            newItem = form.save(commit=False)
            newItem.save()
            return render(request, 'newItem.html')
    else:
        form = createItem()
    return render(request, 'newItem.html', {'form': form})


def process_LineItem(request):
    if request.method == 'POST':
        if 'button2' in request.POST:
            form = ProcessLineItem(request.POST)
            if form.is_valid():
                acti = form.cleaned_data['Action']
                print(acti)
                refdLI = form.cleaned_data['refLineItem']
                if acti == 'Assign':
                    OrderAction.objects.create(
                        batchNumber=form.cleaned_data['batchNumber'],
                        refEmp=form.cleaned_data['refEmp'],
                        fulfillmentStart=form.cleaned_data['fulfillmentStart'],
                        refLineItem=form.cleaned_data['refLineItem'],
                        refShelf=form.cleaned_data['refShelf'],
                        Action='Assigned',
                        amountMoved=form.cleaned_data['amountMoved']
                        )
                    refdLI.lineItemStatus='Assigned'
                    refdLI.save()
                elif acti == 'Stored':
                    OrderAction.objects.create(
                        batchNumber=form.cleaned_data['batchNumber'],
                        refEmp=form.cleaned_data['refEmp'],
                        fulfillmentStart=form.cleaned_data['fulfillmentStart'],
                        refLineItem=form.cleaned_data['refLineItem'],
                        refShelf=form.cleaned_data['refShelf'],
                        Action=acti,
                        amountMoved=form.cleaned_data['amountMoved']
                        )
                    setShelf=form.cleaned_data['refShelf']
                    setShelf.StorageType = 'Inventoried'
                    setShelf.capacityUsed = form.cleaned_data['amountMoved']
                    setShelf.storedItem = form.cleaned_data['refLineItem'].itemID
                    refdLI.lineItemStatus = 'Stored'
                    refdLI.save()
                    setShelf.save()
                elif acti == 'Maintain':
                    OrderAction.objects.create(
                        batchNumber=form.cleaned_data['batchNumber'],
                        refEmp=form.cleaned_data['refEmp'],
                        fulfillmentStart=form.cleaned_data['fulfillmentStart'],
                        refLineItem=form.cleaned_data['refLineItem'],
                        refShelf=form.cleaned_data['refShelf'],
                        Action=acti,
                        amountMoved=form.cleaned_data['amountMoved']
                        )
                    setShelf = form.cleaned_data['refShelf']
                    setShelf.capacityUsed = form.cleaned_data['amountMoved']
                    setShelf.storedItem = form.cleaned_data['refLineItem'].itemID
                    refdLI.lineItemStatus = 'Maintained'
                    setShelf.StorageType = 'Maintained'
                    refdLI.save()
                    setShelf.save()
                #set shelf here
                #action = form.save(commit=False)
                #action.save()
                return render(request, 'WarehouseCustomerManagement.html')
        else:
            form1 = GetWareHouse(request.POST)
            if form1.is_valid():
                ProcessLineItem.base_fields['refLineItem'] = forms.ModelChoiceField(queryset=LineItem.objects.filter(refWHouse=form1.cleaned_data['gotWH']))
                ProcessLineItem.base_fields['refShelf'] = forms.ModelChoiceField(queryset=Shelf.objects.filter(whLoc=form1.cleaned_data['gotWH']))
                form = ProcessLineItem()
                title = 'Now Create the Order Action'
                return render(request, 'OneForm2.html', {'form': form, 'title': title})
    else:
        form = GetWareHouse()
        title = 'Enter a Warehouse to find Line Items'
        return render(request, 'OneForm.html', {'form': form, 'title': title})

# def setOAStatus(request):
#     #filter by batchID
#     if request.method == 'POST':
#         if 'button2' in request.POST:
#             form = ChangeOrderActionStatus(request.POST)
#             if form.is_valid():
#                 batchObj = form.cleaned_data['gotBatch']
#                 refdBatch = OrderAction.objects.filter(batchNumber=batchObj).first()
#                 refEmp1 = form.cleaned_data['refEmp']
#                 Action1 = form.cleaned_data['Action']
#                 fulfillmentEnd1 = form.cleaned_data['fulfillmentEnd']
#                 if Action1 == 'Shipped':
#                     refdBatch.refShelf.capacityUsed = 0
#                     refdBatch.refShelf.save()
#                 asdf = OrderAction.objects.create(
#                     batchNumber=batchObj,
#                     refEmp=refEmp1,
#                     Action=Action1,
#                     fulfillmentEnd=fulfillmentEnd1,
#                     amountMoved=refdBatch.amountMoved,
#                     refShelf=refdBatch.refShelf,
#                     refLineItem=refdBatch.refLineItem
#                 )
#                 asdf.save()
#                 return render(request, 'WarehouseCustomerManagement.html')
#
#         else:
#             form = ChangeOrderActionStatus
#     else:
#         form = ChangeOrderAction()
#         title = 'Change an Order'
#         return render(request, 'OneForm.html', {'form': form, 'title': title})


def set_OrdWH(request):
    if request.method == 'POST':
        form = SetOAWarehouse(request.POST)
        if form.is_valid():
            refdLineItem = form.cleaned_data['liobj']
            refdLineItem.refWHouse = form.cleaned_data['whobj']
            refdLineItem.lineItemStatus = 'Assigned'
            refdLineItem.save()
            return render(request, 'WarehouseCustomerManagement.html')
    else:
        form = SetOAWarehouse()
        title = 'Set Warehouse to complete Line Item'
        return render(request, 'OneForm.html', {'form': form, 'title': title})

def view_CustOrders(request):
    if request.method == 'POST':
        cust_id = request.POST.get('id_custID', '')
        try:
            custvalue = Orders.objects.raw('select * from company_orders inner join company_lineitem on '
                                           'company_lineitem.ordRefMain_id = company_orders.id inner join company_address '
                                           'on company_address.id = company_lineitem.shippingLoc_id inner join '
                                           'company_item'
                                           ' on company_item.id = company_lineitem.itemID_id where '
                                           'company_orders.orderingCust_id = %s', [cust_id])

            print('got here')
            return render(request, 'OrderInfo.html', {'custvalue': custvalue})
        except:
            return render(request, 'viewCustInfoSubmit.html')
    else:
        return render(request, 'viewCustInfoSubmit.html')


def view_CustInventory(request):
    if request.method == 'POST':
        cust_id = request.POST.get('id_custID', '')
        LIStatus = 'Stored'
        print(cust_id)
        try:
            custvalue = Orders.objects.raw('Select sum(company_lineitem.amount) as totals, '
                                           'company_item.itemName, company_orders.id from company_orders inner join company_lineitem on '
                                           'company_orders.id = company_lineitem.ordRefMain_id inner join company_item on '
                                           'company_item.id = company_lineitem.itemID_id where '
                                           'company_orders.orderingCust_id = %s and company_lineitem.lineItemStatus = %s',
                                           [cust_id, LIStatus])

            print('got here')
            return render(request, 'InventoryInfo.html', {'custvalue': custvalue})
        except:
            return render(request, 'viewCustInfoSubmit.html')
    else:
        return render(request, 'viewCustInfoSubmit.html')


def view_Inventory(request):
    custvalue = Shelf.objects.raw('Select company_shelf.id, company_item.itemName, sum(company_shelf.capacityUsed) as totals from company_shelf inner join company_item on company_item.id = company_shelf.storedItem_id where company_shelf.StorageType = \'Inventoried\' group by company_item.id')

    return render(request, 'InventoryInfo.html', {'custvalue': custvalue})

def view_DailyOrders(request):
    if request.method == 'POST':
        form = DateOrderForm(request.POST)
        if form.is_valid():
            dailyord= Orders.objects.filter(DateRequested=form.cleaned_data['DateRequested'])
            print('got here')
            print(form.cleaned_data['DateRequested'])
        return render(request, 'DailyOrderInfo.html', {'dailyord': dailyord})
    else:
        form = DateOrderForm()
        return render(request, 'getCustOrders.html', {'form': form})


def add_Employee(request):
    if request.method == "POST":
        form = AddEmployee(request.POST)
        if form.is_valid():
            newEmp = form.save(commit=False)
            newEmp.save()
        return render(request, 'addEmployees')


def add_Store(request):
    if request.method == "POST":
        form1 = EnableStore(request.POST)
        form2 = CreateAddress(request.POST)
        if form1.is_valid() and form2.is_valid():
            addr=Address.objects.create(
                city=form2.cleaned_data['city'],
                state=form2.cleaned_data['state'],
                street=form2.cleaned_data['street'],
                street2=form2.cleaned_data['street2']
            )
            addr.save()
            store = Store.objects.create(
                storeName=form1.cleaned_data['storeName'],
                location=addr,
                dateOpened=form1.cleaned_data['dateOpened'],
                refCust=form1.cleaned_data['refCust']
            )
            store.save()
        return render(request, 'TwoForm.html')
    else:
        form1 = EnableStore()
        form2 = CreateAddress()
        title = 'Add a new Store'
        return render(request, 'TwoForm.html', {'form1': form1, 'form2': form2, 'title': title})

def send_Invoice(request):
    if request.method == 'POST':
        if 'button1' in request.POST:
            print('nope here')
            form = getCustID(request.POST)
            if form.is_valid():
                cust = form.cleaned_data['cust']
                valset = Invoice.objects.filter(payingCust=cust, InvoiceStatus='Not Sent')
                InvoiceStatusUpdate().base_fields['invChoice'] = forms.ModelChoiceField(queryset=valset)
                form = InvoiceStatusUpdate()
                title = "Send Invoice"
                return render(request, 'OneForm2.html', {'form': form, 'title': title})
        else:
            print('got here')
            form = InvoiceStatusUpdate(request.POST)
            if form.is_valid():
                updInv=form.cleaned_data['invChoice']
                updInv.InvoiceStatus = form.cleaned_data['InvoiceStatus']
                updInv.save()
                return render(request, 'WarehouseCustomerManagement.html')
    else:
        form = getCustID()
        title = 'Specify a Customer for the Invoice'
        return render(request, 'OneForm.html', {'form': form, 'title': title})

def get_Balance(request):
    if request.method == 'POST':
        form = getCustID(request.POST)
        if form.is_valid():
            custFilter = form.cleaned_data['cust']
            InvFilter = Invoice.objects.filter(payingCust=custFilter)
            totals = 0
            for row in InvFilter:
                totals = totals + row.amountPaid
            cust = form.cleaned_data['cust']
            return render(request, 'viewAccountBalance.html', {'totals': totals, 'cust': cust})
    else:
        form = getCustID()
        return render(request, 'OneForm.html', {'form': form})


def endUserSite(request):
    return render(request, 'EndUser.html')


def create_Account(request):
    if request.method == 'POST':
        form = endUserCustomer(request.POST)
        if form.is_valid():
            newCust = form.save(commit=False)
            newCust.save()
            return render(request, 'EndUser.html')
    else:
        form = endUserCustomer()
        return render(request, 'OneForm.html', {'form': form})

def create_StoreOrder(request):
    if request.method == 'POST':
        form = addStoreOrder(request.POST)
        if form.is_valid():
            StoreOrder.objects.create(
                endCust=form.cleaned_data['endCust'],
                itemOrd=form.cleaned_data['itemOrd'],
                amtOrd=form.cleaned_data['amtOrd'],
                strOrdSts='Not Fulfilled'
            )
            return render(request, 'EndUser.html')
    else:
        form = addStoreOrder()
        return render(request, 'OneForm.html', {'form': form})

def check_StoreOrderStatus(request):
    if request.method == 'POST':
        form = getCustID(request.POST)
        if form.is_valid():
            custVal = form.cleaned_data['cust']
            strOrd = StoreOrder.objects.filter(endCust=custVal)
            return render(request, 'ViewStoreOrders.html', {'strOrd': strOrd})
    else:
        form = getCustID()
        return render(request, 'OneForm.html', {'form': form})

def ship_LineItem(request):
    if request.method == 'POST':
        if 'button2' in request.POST:
            form = shipOrderAction(request.POST)
            print('here')
            if form.is_valid():
                print('here2')
                refdLI = form.cleaned_data['liobj2']
                asdf=OrderAction.objects.create(
                    batchNumber=form.cleaned_data['BatchNumber'],
                    refShelf=form.cleaned_data['AssignShelf'],
                    refLineItem=form.cleaned_data['liobj2'],
                    fulfillmentStart=form.cleaned_data['fulDate'],
                    fulfillmentEnd='2100-01-01',
                    Action='Assigned',
                    amountMoved=1,
                    refEmp=form.cleaned_data['refdEmp']
                )
                refdLI.lineItemStatus = 'Shipped'
                refdLI.save()
                asdf.save()
                newShelf = form.cleaned_data['AssignShelf']
                newShelf.StorageType = 'Open'
                newShelf.capacityUsed = 0
                newShelf.storedItem = None
                newShelf.save()
                return render(request, 'WarehouseCustomerManagement.html')
        else:
            form1 = shipItem(request.POST)
            if form1.is_valid():
                lineRef = form1.cleaned_data['liobj']
                shipOrderAction.base_fields['AssignShelf'] = forms.ModelChoiceField(queryset=Shelf.objects.filter(storedItem=lineRef.itemID, StorageType='Inventoried'))
                shipOrderAction.base_fields['liobj2'] = forms.ModelChoiceField(queryset=LineItem.objects.filter(id=lineRef.id))
                form = shipOrderAction()
                return render(request, 'OneForm2.html', {'form': form})
        #Select shelves from warehouse where itemID is equal to the lineItemID
    else:
        form = shipItem()
        title = 'Select a line item to search items for'
        return render(request, 'OneForm.html', {'form': form, 'title': title})

def change_StoreInventory(request):
    if request.method == 'POST':
        form = changeItemInventory(request.POST)
        if form.is_valid():
            refdInv = StoreInventory.objects.filter(refItem=form.cleaned_data['refItem'], refStore=form.cleaned_data['refStore']).first()
            if refdInv == None:
                abc=StoreInventory.objects.create(
                    amount=form.cleaned_data['amount'],
                    refItem=form.cleaned_data['refItem'],
                    refStore=form.cleaned_data['refStore'],
                )
                abc.save()
            else:
                if form.cleaned_data['operation'] == 'Add':
                    refdInv.amount = refdInv.amount + form.cleaned_data['amount']
                elif form.cleaned_data['operation'] == 'Sub':
                    refdInv.amount = refdInv.amount - form.cleaned_data['amount']
                else:
                    refdInv.amount = form.cleaned_data['amount']
                refdInv.save()
            return render(request, 'CustomerPortal.html')
    else:
        form = changeItemInventory()
        return render(request, 'OneForm.html', {'form': form})


def view_EndUsers(request):
    custvalue= Customer.objects.filter(warCust__isnull=True)
    title = 'View End Customer Information'
    return render(request, 'EndCustView.html', {'custvalue': custvalue, 'title': title})


def view_StoreInventory(request):
    storeItems = StoreInventory.objects.all()
    title = 'Store Inventory'
    return render(request, 'StoreInventory.html', {'storeItems': storeItems, 'title': title})

def view_EndOrders(request):
    storeOrders = StoreOrder.objects.all()
    title = 'Store Orders'
    return render(request, 'ViewStoreOrders.html', {'strOrd': storeOrders, 'title': title})


def pay_Invoice(request):
    if request.method == 'POST':
        if 'button2' in request.POST:
            form1 = GetInvoice(request.POST)
            if form1.is_valid():
                print('here')
                refdInv = form1.cleaned_data['gotINV']
                refdInv.amountPaid = 0
                refdInv.invoiceStatus = 'Paid'
                refdInv.DatePaid = datetime.date.today()
                refdInv.save()
            return render(request, 'CustomerPortal.html')
        else:
            form1 = getCustID(request.POST)
            if form1.is_valid():
                refdCust = form1.cleaned_data['cust']
                title='Choose an Invoice to Pay'
                GetInvoice().base_fields['gotINV'] = forms.ModelChoiceField(queryset=Invoice.objects.filter(payingCust=refdCust, InvoiceStatus='Sent').exclude(Q(amountPaid=0)))
                form = GetInvoice()
                return render(request, 'OneForm2.html', {'form': form, 'title':title})
    else:
        form = getCustID()
        title = 'Choose a customer'
        return render(request, 'OneForm.html', {'form': form, 'title': title})


def add_Employee(request):
    if request.method == 'POST':
        form = AddEmployee(request.POST)
        if form.is_valid():
            newEmp=form.save(commit=False)
            newEmp.save()
            return render(request, 'WarehouseCustomerManagement.html')
    else:
        title='Add an Employee'
        form = AddEmployee()
        return render(request, 'OneForm.html', {'form': form, 'title': title})

def add_Position(request):
    if request.method == 'POST':
        form = AddPosition(request.POST)
        if form.is_valid():
            newEmp=form.save(commit=False)
            newEmp.save()
            return render(request, 'WarehouseCustomerManagement.html')
        return render(request, 'WarehouseCustomerManagement.html')
    else:
        title='Add a Position'
        form = AddPosition()
        return render(request, 'OneForm.html', {'form': form, 'title': title})


def add_Contingent(request):
    if request.method == 'POST':
        form = AddContingent(request.POST)
        if form.is_valid():
            newEmp=form.save(commit=False)
            newEmp.save()
            return render(request, 'WarehouseCustomerManagement.html')
    else:
        title='Add a Contingent Position'
        form = AddContingent()
        return render(request, 'OneForm.html', {'form': form, 'title': title})


def view_CustInvoice(request):
    if request.method == 'POST':
        form = getCustID(request.POST)
        if form.is_valid():
            cust = form.cleaned_data['cust']
            custInvs = Invoice.objects.filter(payingCust=cust)
            return render(request, 'viewCustInvoices.html', {'custInvs': custInvs})

    else:
        form = getCustID()
        return render(request, 'OneForm.html', {'form': form})