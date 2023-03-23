from django.shortcuts import render
from django.contrib.auth import login
from Api_User.models import PostModel, ImageModel, CommentModel
from rest_framework import generics,status
from rest_framework.response import Response
from rest_framework.permissions import (AllowAny,IsAdminUser, IsAuthenticated, DjangoModelPermissions)
from .permissions import IsOwner
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import (OutstandingToken, BlacklistedToken)

from .serializers import (RegisterSerializer, LoginSerializer,ImageSerializer)
from .comments import (CreateCommentSerialiser,EditCommentSerializer, DeleteCommentSerializer, PostCommentListSerializer)
from .posts import (CreatePostSerializer, DetailPostSerializer,UpdatePostSerilaizer,DeletePostSerializer,
                    # MyPostListSerializer,
                    AllPostListSerializer)


# REGISTER VIEW
class RegisterView(generics.CreateAPIView):
    permission_classes = [AllowAny] 
    queryset = User.objects.all()
    serializer_class = RegisterSerializer


# LOGIN VIEW
class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        context = {
            'First Name':str(user.first_name),
            'Last Name':str(user.last_name),
            'Email':str(user.email),
            'Username':str(user.username),
        }
        return Response(context)


# LOGOUT VIEW
class LogoutView(generics.GenericAPIView):

    permission_classes = (IsAuthenticated,)

    def post(self, request):
        tokens = OutstandingToken.objects.filter(user_id=request.user.id)
        for token in tokens:
            t, _ = BlacklistedToken.objects.get_or_create(token=token)

        return Response(status=status.HTTP_205_RESET_CONTENT)



# CREATE POST VIEW
class CreatePostView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = PostModel.objects.all()
    serializer_class = CreatePostSerializer

    def create(self, *args, **kwargs):
        user = self.request.user
        if user.is_superuser == 0:
            serializer = CreatePostSerializer(data =self.request.data, context={'user': user})
            if serializer.is_valid():
                serializer.save()
                return Response(data=serializer.data)
            else:
                return Response(data= serializer.errors)
        else:
            return Response({'Error':'Permission Denied..!','Message':'Super user have no permission to create a post '})


# DETAIL POST VIEW
class DetailPostView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = PostModel.objects.all()
    serializer_class = DetailPostSerializer


# UPDATE POST VIEW
class UpdatePostView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated, IsOwner]
    queryset = PostModel.objects.all()
    serializer_class = UpdatePostSerilaizer

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)


# DELETE POST VIEW
class DeletePostView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated, IsOwner]
    queryset = PostModel.objects.all()
    serializer_class = DeletePostSerializer

    def perform_delete(self, serializer):
        serializer.save(user=self.request.user)


# # MY POST LIST VIEW
# class MyPostListView(generics.ListAPIView):
#     permission_classes = [IsAuthenticated,IsOwner]
#     queryset = PostModel.objects.all()
#     serializer_class = MyPostListSerializer
    
#     def get_queryset(self):
#         user = self.request.user
#         posts = PostModel.objects.filter(user=user)
#         return posts
    
#     def perform_get(self, serializer):
#         serializer.save(user=self.request.user)


# ALL POST LIST VIEW
class AllPostListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = PostModel.objects.all()
    serializer_class = AllPostListSerializer



# IMAGE VIEW
class ImageView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = ImageModel.objects.all()
    serializer_class = ImageSerializer

    def create(self, *args, **kwargs):
        user = self.request.user
        if user.is_superuser == 0:
            serializer = ImageSerializer(data =self.request.data, context={'user': user})
            if serializer.is_valid():
                serializer.save()
                return Response(data=serializer.data)
            else:
                return Response(data= serializer.errors)
        else:
            return Response({'Error':'Permission Denied..!','Message':'Super user have no permission to Add image to a post '})


# CREATE COMMENT VIEW
class CreateCommentView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = CommentModel.objects.all()
    serializer_class = CreateCommentSerialiser

    def create(self,request, *args, **kwargs):
        user = request.user
        if user.is_superuser == 0:
            serializer = CreateCommentSerialiser(data =request.data, context={'user': user})
            if serializer.is_valid():
                serializer.save()
                return Response(data=serializer.data)
            else:
                return Response(data= serializer.errors)
        else:
            return Response({'Error':'Permission Denied..!','Message':'Super user have no permission to comment a post '})


# POST COMMENTS LIS VIEW
class PostCommentListView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = PostModel.objects.all()
    serializer_class = PostCommentListSerializer


# EDIT COMMENT VIEW
class CommentEditView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated, IsOwner]
    queryset = CommentModel.objects.all()
    serializer_class = EditCommentSerializer
    
    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

# DELETE COMMENT VIEW
class CommentDeleteView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated,IsOwner]
    queryset = CommentModel.objects.all()
    serializer_class = DeleteCommentSerializer
    
    def perform_delete(self, serializer):
        serializer.save(user=self.request.user)