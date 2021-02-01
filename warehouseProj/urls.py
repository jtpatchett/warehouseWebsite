"""warehouseProj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/dev/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from company import views

urlpatterns = [
    url(r'^home/$', views.home, name='home'),
    url(r'^WarehouseCustomerManagement/$', views.adminHome, name='adminHome'),
    url(r'^newCust/$', views.new_cust, name='new_cust'),
    url(r'^viewCustInfoSubmit/$', views.cust_info, name='cust_info'),
    url(r'^customer/(?P<pk>\d+)/$', views.cust_info_page, name='cust_info_page'),
    url(r'^getCustPricing/$', views.get_custPricing, name='get_custPricing'),
    url(r'^createOrder/$', views.create_order, name='create_order'),
    url(r'^CustomerPortal/$', views.customer_portal, name='customer_portal'),
    url(r'^addlineItem/$', views.add_lineitem, name='add_lineitem'),
    url(r'^addNewItem/$', views.create_item, name='create_item'),
    url(r'^processLineItem/$', views.process_LineItem, name='process_LineItem'),
    url(r'^viewCustomerOrders/$', views.view_CustOrders, name='view_CustOrders'),
    url(r'^viewCustomerInventory/$', views.view_CustInventory, name='view_CustInventory'),
    url(r'^viewInventory/$', views.view_Inventory, name='view_Inventory'),
    url(r'^viewDailyOrders/$', views.view_DailyOrders, name='view_DailyOrders'),
    url(r'^addEmployee/$', views.add_Employee, name='add_Employee'),
    url(r'^enableStore/$', views.add_Store, name='add_Store'),
    url(r'^sendInvoice/$', views.send_Invoice, name='send_Invoice'),
    url(r'^getBalance/$', views.get_Balance, name='get_Balance'),
    url(r'^endUserSite/$', views.endUserSite, name='endUserSite'),
    url(r'^createAccount/$', views.create_Account, name='create_Account'),
    url(r'^createStoreOrder/$', views.create_StoreOrder, name='create_StoreOrder'),
    url(r'^changeStoreInventory/$', views.change_StoreInventory, name='change_StoreInventory'),
    url(r'^checkStoreOrderStatus/$', views.check_StoreOrderStatus, name='check_StoreOrderStatus'),
    url(r'^viewStoreInventory/$', views.view_StoreInventory, name='view_StoreInventory'),
    url(r'^viewEndUsers/$', views.view_EndUsers, name='view_EndUsers'),
    url(r'^viewEndOrders/$', views.view_EndOrders, name='view_EndOrders'),
    url(r'^setOrdActWH/$', views.set_OrdWH, name='set_OrdWH'),
    url(r'^shipLineItem/$', views.ship_LineItem, name='ship_LineItem'),
    url(r'^payInvoice/$', views.pay_Invoice, name='pay_Invoice'),
    url(r'^addEmployee/$', views.add_Employee, name='add_Employee'),
    url(r'^addPosition/$', views.add_Position, name='add_Position'),
    url(r'^addContingent/$', views.add_Contingent, name='add_Contingent'),
    url(r'^viewCustInvoice/$', views.view_CustInvoice, name='view_CustInvoice'),
    path('admin/', admin.site.urls),
]
