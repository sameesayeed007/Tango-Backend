from django.conf import settings
from django.urls import path, include
from . import views

#from .views import ProductDetailView,CreateProductAPIView,DestroyProductAPIView, ProductListAPIView,VariationListView ,GroupProductDetailView ,CategoryListAPIView ,CategoryAPIView , CreateCategoryAPIView , DestroyCategoryAPIView
#from .views import CategoryListAPIView , CategoryRetrieveAPIView

app_name = 'Product'

urlpatterns = [

    path("serpy/product/", views.SerpyListProductAPIView.as_view()),
    path("category/", views.CategoryListAPIView.as_view()),
    path("category/<int:pk>/", views.CategoryAPIView.as_view()),
    path("list/product/", views.ListProductAPIView.as_view()),
    path("serpy/product/", views.SerpyListProductAPIView.as_view()),
    path("list-product/user/", views.ListUserProductAPIView.as_view()),
    path("create/product/", views.CreateProductAPIView.as_view()),
    path("product/<int:pk>/delete/", views.DestroyProductAPIView.as_view()),
    path("product/<str:uuid>/", views.ProductDetailView.as_view()),
    path("product/views/", views.ProductViewsAPIView.as_view()),
    #path('inventory/<int:pk>', views.VariationListView.as_view(), name='product_inventory'),
    path("create/category/", views.CreateCategoryAPIView.as_view()),
    path("group_product/",views.group_product),
    #Product comments and reviews
    path('comments_product/<int:product_id>/', views.comments_product),
    #path('comments/<int:product_ids>/', views.comm),
    path('create_comment/', views.create_comment),
    path('create_reply/', views.create_reply),
    path('edit_comment/<int:comment_id>/', views.edit_comment),
    path('edit_reply/<int:reply_id>/', views.edit_reply),
    path('delete_comment/<int:comment_id>/', views.delete_comment),
    path('delete_reply/<int:reply_id>/', views.delete_reply),
    path('reviews_product/<int:product_id>/', views.reviews_product),
    path('create_review/', views.create_review),
    path('edit_review/<int:review_id>/', views.edit_review),
    path('delete_review/<int:review_id>/', views.delete_review),
    path('ratings/<int:product_id>/',views.product_ratings,name='ratings'),
    path('upload/',views.upload_product),
    path('edit/',views.edit_product),

]
