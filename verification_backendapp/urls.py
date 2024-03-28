# user_management/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet,UserLoginView,StoreListingsByWarehouseType,ReconcileDataViewSet,login,callback

router = DefaultRouter()
#router.register(r'users', UserViewSet)


# user_management/urls.py

router = DefaultRouter()
#router.register(r'users', UserViewSet)


router.register(r'users', UserViewSet)
#router.register(r'roles', RoleViewSet)
#router.register(r'groups', GroupViewSet)
#router.register(r'vendors', VendorsViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('azure-login/login', login, name='azure'),
    path('azure-login/callback', callback, name='azure'),
    path('users/login', UserLoginView.as_view(), name='user-login'),
    path('warehouse/listing', StoreListingsByWarehouseType.as_view(), name='warehouse'),
    path('reconcilesalesdata', ReconcileDataViewSet.as_view(), name='reconciledata')
    #path('vendors/assign-vendor/', AssignVendorView.as_view(), name='assign-vendor'),
    
]
