from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import (TokenObtainPairView,TokenRefreshView,TokenVerifyView)
from Api_User.views import (RegisterView, LoginView, LogoutView, 
                            CreatePostView, DetailPostView, UpdatePostView, DeletePostView, 
                            # MyPostListView, 
                            AllPostListView,ImageView,PostCommentListView,
                            CreateCommentView, CommentEditView, CommentDeleteView)
from Api_Admin.views import (RegisterSuperuserView, AdminPostListView, AdminPostDetailView, AdminPostDeleteView, 
                             AdminPostCommentListView, AdminDeleteCommentView)

urlpatterns = [
    path('admin/', admin.site.urls),

# Login Authentication 
    path('api/user/register/',RegisterView.as_view()),
    path('api/login/', LoginView.as_view()),
    path('api/logout/', LogoutView.as_view()),

# Blog Post
    path('api/user/post/create/', CreatePostView.as_view()),
    path('api/user/post/<int:pk>/', DetailPostView.as_view()),
    path('api/user/post/update/<int:pk>/', UpdatePostView.as_view()),
    path('api/user/post/delete/<int:pk>/', DeletePostView.as_view()),
    
    # path('api/user/post/my-list/', MyPostListView.as_view()),
    path('api/user/post/all-list/', AllPostListView.as_view()),
    
    path('api/user/post/add-image/', ImageView.as_view(), name='image-post'),
    
    path('api/user/post/<int:pk>/comment/', CreateCommentView.as_view()),
    path('aoi/user/post/<int:pk>/all-comments/', PostCommentListView.as_view()),
    path('api/user/post/comment/edit/<int:pk>/', CommentEditView.as_view()),
    path('api/user/post/comment/delete/<int:pk>/', CommentDeleteView.as_view()),

# ADMIN
    # Create superuser
    path('api/register/superuser/',RegisterSuperuserView.as_view()),

    path('api/admin/post/list/', AdminPostListView.as_view()),
    path('api/admin/post/<int:pk>/', AdminPostDetailView.as_view()),
    path('api/admin/post/delete/<int:pk>/', AdminPostDeleteView.as_view()),

    path('api/admin/post/<int:pk>/comments/', AdminPostCommentListView.as_view()),
    path('api/admin/comment/delete/<int:pk>/', AdminDeleteCommentView.as_view()),

# Token Related Urls
    path('token-generate/', TokenObtainPairView.as_view()),
    path('token-verify/', TokenVerifyView.as_view()),
    path('token-refresh/',TokenRefreshView.as_view()),
]
