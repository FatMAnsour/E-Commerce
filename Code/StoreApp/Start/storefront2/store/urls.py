from django.urls import path
from . import views
from rest_framework_nested import routers


router = routers.DefaultRouter()
router.register('products',views.ProductViewset,basename='products')
router.register('collections',views.CollectionViewset)
router.register('carts',views.CartViewset)
router.register('customers',views.CustomerViewset)
router.register('orders',views.OrderViewset, basename= "orders")


# router.register('cartsItems',views.CartItemViewset)



products_router = routers.NestedDefaultRouter(router,'products',lookup='product')
products_router.register('reviews',views.ReviewViewset, basename='product-review')

carts_router = routers.NestedDefaultRouter(router, 'carts', lookup='cart')
carts_router.register('items',views.CartItemViewset,basename='carts-item')
# URLConf
urlpatterns = router.urls + products_router.urls + carts_router.urls
