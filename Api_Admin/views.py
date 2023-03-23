from rest_framework import generics
from rest_framework.permissions import IsAdminUser
from django.contrib.auth.models import User
from Api_User.models import PostModel, CommentModel
from .serializers import RegisterSuperuserSerializer,AdminPostSerializer, AdminPostCommentListSerializer, AdminCommentSerializer

# REGISTER SUPERUSER VIEW
class RegisterSuperuserView(generics.CreateAPIView):
    permission_classes = [IsAdminUser]
    queryset = User.objects.all()
    serializer_class = RegisterSuperuserSerializer

# POST LIST VIEW
class AdminPostListView(generics.ListAPIView):
    permission_classes = [IsAdminUser]
    queryset = PostModel.objects.all()
    serializer_class = AdminPostSerializer

# POST DETAIL VIEW
class AdminPostDetailView(generics.RetrieveAPIView):
    permission_classes = [IsAdminUser]
    queryset = PostModel.objects.all()
    serializer_class = AdminPostSerializer

# POST DELETE VIEW
class AdminPostDeleteView(generics.DestroyAPIView):
    permission_classes = [IsAdminUser]
    queryset = PostModel.objects.all()
    serializer_class = AdminPostSerializer


# POST COMMENT LIST VIEW
class AdminPostCommentListView(generics.RetrieveAPIView):
    permission_classes = [IsAdminUser]
    queryset = PostModel.objects.all()
    serializer_class = AdminPostCommentListSerializer

# DELETE COMMENT VIEW
class AdminDeleteCommentView(generics.DestroyAPIView):
    permission_classes = [IsAdminUser]
    queryset = CommentModel.objects.all()
    serializer_class = AdminCommentSerializer