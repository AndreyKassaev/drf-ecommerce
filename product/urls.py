from django.urls import path, include
from .views import (
    ProductList,
    CreateProduct, 
    UpdateProduct, 
    DeleteProduct, 
    ProductDetail, 
    ProductListOfSelectedCategory,
    ProductListOfSelectedAuthor,
    CategoriesList,
    SingleCategory,
    CategoriesListNoPagination,
    title_unique,
    ProductListOfMyArt
)

urlpatterns = [
    path('list/', ProductList.as_view()),
    path('list/category/<title>/', ProductListOfSelectedCategory.as_view()),
    path('list/author/<name>/', ProductListOfSelectedAuthor.as_view()),
    path('create/', CreateProduct.as_view()),
    path('update/<pk>/', UpdateProduct.as_view()),
    path('detail/<title>/', ProductDetail.as_view()),
    path('delete/<pk>/', DeleteProduct.as_view()),
    path('categories-list/', CategoriesList.as_view()),
    path('categories-list-no-pagination/', CategoriesListNoPagination.as_view()),
    path('single-category/<title>/', SingleCategory.as_view()),
    path('title-unique/<title>', title_unique),
    path('my-art/', ProductListOfMyArt.as_view())
]