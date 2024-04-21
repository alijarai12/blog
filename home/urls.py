from django.urls import path
from home import views

urlpatterns = [
    path('bloglist/', views.BlogListView.as_view(), name='list-view'),
    path('blog/', views.BlogView.as_view(), name='blog'),
    path('blogcomment/', views.BlogCommentView.as_view(), name='comment-view'),
    path('blogcomment/<int:id>/', views.BlogCommentView.as_view(), name='comment-view'),

    # path('view/',views.BlogView.as_view(), name='blogview'),
    # path('<int:pk>/', views.BlogDetailAPIView.as_view(), name='BlogDetailAPIView'),
    # path('list/', views.BlogListView.as_view(), name='list-view'),
]

