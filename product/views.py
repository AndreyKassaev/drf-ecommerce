from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView, RetrieveAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status



from .serializers import ProductListSerializer, CreateProductSerializer, ProductCategorySerializer, UpdateProductSerializer
from .models import Product, ProductCategory
from .pagination import ProductPagination

from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(['GET'])
def title_unique(request, title):
    try:
        product = Product.objects.get(title=title)
        return Response(True)
    except:
        return Response(False)        

class DeleteProduct(DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer
    permission_classes = [IsAuthenticated, ]

class ProductDetail(RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer
    lookup_field= 'title'

class CreateProduct(APIView):
    def post(self, request):
        es = CreateProductSerializer(data=request.data)
        if es.is_valid():
            category_str = request.data['categories']
            category_list = category_str.split(",")

            # It's supposed to accept multiple categories but it works uncorrect
            # qs_str_list = []

            # for x in category_list:
            #     qs_str_list.append(f'Q(title="{x}")')

            # qs_str = " | ".join(qs_str_list)

            # f = open('product/createproduct.py', 'w+')
            # f.writelines(['from .models import Product, ProductCategory\n',
            # 'from django.db.models import Q\n',
            # 'def category_qs():\n',
            # '    qs = ProductCategory.objects.filter(%s)\n' % qs_str,
            # '    return qs'
            # ])
            # f.close()

            # from . import createproduct
            # cat_qs = createproduct.category_qs()

            # exec(open('product/createproduct.py').read())

            cat_qs = ProductCategory.objects.filter(title=category_list[0])

            es.save(author=self.request.user.author, categories=cat_qs)

            return Response(status=status.HTTP_201_CREATED)
        return Response(data=es.errors, status=status.HTTP_400_BAD_REQUEST)
    permission_classes = [IsAuthenticated, ]

class UpdateProduct(UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = UpdateProductSerializer
    permission_classes = [IsAuthenticated,]

    def get_queryset(self):
        author = self.request.user.author.id
        qs = Product.objects.filter(author__id=author)
        return qs

    
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class ProductList(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title','=author__name', '=categories__title']
    ordering_fields = ['price', 'date_created', 'date_updated']
    ordering = ['-date_created']
    pagination_class = ProductPagination

class ProductListOfSelectedCategory(ListAPIView):
    serializer_class = ProductListSerializer
    lookup_url_kwarg = 'title'
    pagination_class = ProductPagination
    filter_backends = [OrderingFilter]
    ordering_fields = ['price']
    ordering = ['-date_created']

    def get_queryset(self):
        title = self.kwargs.get(self.lookup_url_kwarg)
        qs = Product.objects.filter(categories__title=title)
        return qs

class ProductListOfSelectedAuthor(ListAPIView):
    serializer_class = ProductListSerializer
    lookup_url_kwarg = 'name'
    pagination_class = ProductPagination
    filter_backends = [OrderingFilter]
    ordering_fields = ['price']
    ordering = ['-date_created']

    def get_queryset(self):
        name = self.kwargs.get(self.lookup_url_kwarg)
        qs = Product.objects.filter(author__name=name)
        return qs

class ProductListOfMyArt(ListAPIView):
    serializer_class = ProductListSerializer

    def get_queryset(self):
        author = self.request.user.author.id
        qs = Product.objects.filter(author__id=author)
        return qs

class CategoriesList(ListAPIView):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer
    pagination_class = ProductPagination

class CategoriesListNoPagination(ListAPIView):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer

class SingleCategory(RetrieveAPIView):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer
    lookup_field= 'title'

   

