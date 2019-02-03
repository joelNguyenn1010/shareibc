from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.authentication import SessionAuthentication
from rest_framework import permissions, views
from rest_framework.response import Response
from shareibc.pagination import CustomPagination
# Create your views here.
from .models import Product, City
from .serializers import ProductSerializer, CitySerializer, ProductIndexSerializer
# from shareibc.pagination import CustomPagination
def filepath_images(domain, filename):
    return 'http://{domain}/media/background/{filename}'.format(domain=domain, filename=filename)

class ProductCity(ListAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = CitySerializer
    queryset = City.objects.all()

class ProductAPI(ListAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = ProductIndexSerializer
    pagination_class = CustomPagination
    search_fields = ('name','type__name')
    ordering_fields = ('name', 'price','value','type__name','quantity','city')
    queryset = Product.objects.all().order_by('-date')

    def get_queryset(self):
        qs = Product.objects.filter(quantity__gt=0).order_by('-date')
        query = self.request.GET.get('p')
        cityQuery = self.request.GET.get('city')
        dateQuery = self.request.GET.get('date')
        if query is not None:
            qs = qs.filter(name__icontains=query)
        if cityQuery is not None:
            qs = qs.filter(city__name__icontains=cityQuery)
        if dateQuery is not None and dateQuery == 'date':
            qs = qs.order_by('date')
        # if dateQuery is not None and dateQuery == '-date':
        #     qs = qs.order_by('-date')
        return qs

class Images(views.APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self,request, format=None):
        return Response(filepath_images(request.META['HTTP_HOST'],'sydney_5.jpg'))

class ProductDetailsAPI(RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'id'


