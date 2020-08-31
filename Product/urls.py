from django.conf import settings
from django.urls import path, include
from . import views

#from .views import ProductDetailView,CreateProductAPIView,DestroyProductAPIView, ProductListAPIView,VariationListView ,GroupProductDetailView ,CategoryListAPIView ,CategoryAPIView , CreateCategoryAPIView , DestroyCategoryAPIView
#from .views import CategoryListAPIView , CategoryRetrieveAPIView

app_name = 'Product'

urlpatterns = [

    path("create/", views.insert_specific_product_value),
    path('delete/<int:product_id>/', views.delete_product_value),
    path('edit/<int:product_id>/', views.get_update_product_value),
    path('products_detail/', views.get_all_product),
    path('category_detail/', views.get_all_product_category),
    path('category/create/', views.insert_specific_category_value),
    path('category/edit/<int:category_id>', views.get_update_category_value),
    path('category/delete/<int:category_id>', views.get_update_category_value),
    path('group/detail/', views.get_all_group_product),
    path('group/create/', views.insert_specific_group_product_value),
    path('group/edit/<int:gp_id>', views.get_update_group_product_value),
    path('group/delete/<int:gp_id>', views.delete_group_product_value),
    path('list/' , views.ListProductView.as_view()),
    
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
