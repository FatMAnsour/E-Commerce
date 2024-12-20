from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.mixins import *
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet,GenericViewSet
from rest_framework.permissions import *
from .models import Product,Collection,Review,Cart,CartItem
from rest_framework.filters import SearchFilter,OrderingFilter
from .serializers import *
from .permission import *
from .filters import ProductFilter

# Create your views here.
class ProductViewset(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class= ProductSerializer
    permission_classes=[IsAdminOrReadOnly]
    filter_backends=[DjangoFilterBackend,SearchFilter,OrderingFilter]
    filterset_class=ProductFilter
    search_fields=['title','description']
    ordering_fields=['unit_price','last_update']
        
class CollectionViewset(ModelViewSet):
    queryset = Collection.objects.annotate(products_count=Count('products')).all()
    serializer_class = CollectionSerializer
    permission_classes=[IsAdminOrReadOnly]

class ReviewViewset(ModelViewSet):
    serializer_class=ReviewSerializer

    def  get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs["product_pk"])
    def get_serializer_context(self):
        return {"product_id":self.kwargs["product_pk"]}

class CartViewset(DestroyModelMixin,CreateModelMixin,RetrieveModelMixin,GenericViewSet):
   queryset = Cart.objects.prefetch_related('items__product').all()
   serializer_class = CartSerializer

class CartItemViewset(ModelViewSet): 
    http_method_names=['get','post','patch','delete']
    
    def get_serializer_class(self):
        if self.request.method=='POST':
            return AddCartItemsSerializers
        elif self.request.method=='PATCH':
            return UpdateCartItemSerializer
        return CartItemsSerializer
    def get_serializer_context(self):
        return {'cart_id': self.kwargs['cart_pk']}
    
    def get_queryset(self):
        return CartItem.objects\
            .filter(cart_id=self.kwargs['cart_pk'])\
            .select_related('product')
    
class CustomerViewset(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAdminUser]

    @action(detail=True, permission_classes =[ViewCustomerHistoryPermission])
    def history(self,request,pk):
        return Response("ok")
    
    @action(detail=False ,methods=['GET','PUT'],permission_classes = [IsAuthenticated])
    def me(self,request):
        # return Response(request.user.id)
        customer = Customer.objects.get(user_id = request.user.id)
        if request.method == 'GET':
            serializer = CustomerSerializer(customer)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = CustomerSerializer(customer,data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

class OrderViewset(ModelViewSet):
    http_method_names = ['get','patch','delete','head','options']    
    def get_permissions(self):
        if self.request.method in ['PATCH','DELETE']:
         return [IsAdminUser()]
        return [IsAuthenticated()]
    
    
    def create(self, request, *args, **kwargs):
        serializer = CreateOrderSerializer(
            data = request.data,
            context = {'user_id': self.request.user.id}
            )
        
        serializer.is_valid(raise_exception = True)
        order = serializer.save()
        serializer = OrderSerializer(order)
        return Response(serializer.data)

    def get_serializer_class(self):
        if self.request.method=='POST':
            return CreateOrderSerializer
        elif self.request.method=='PATCH':
            return UpdataOrderSerializer
        return OrderSerializer
    
    
    def get_queryset(self):
       if self.request.user.is_staff:
           return Order.objects.all()
       customer_id= Customer.objects.only('id').get(user_id =self.request.user.id)
       Order.objects.filter(customer_id=customer_id)

    
     
