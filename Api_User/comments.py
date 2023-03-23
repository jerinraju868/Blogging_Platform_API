from rest_framework import serializers
from django.contrib.auth.models import User
from Api_User.models import CommentModel, PostModel
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _


# CREATE COMMENT SERIALIZER
class CreateCommentSerialiser(serializers.ModelSerializer):
    class Meta:
        model = CommentModel
        fields = ['post','comment']
        extra_kwargs = {'post':{'required':True},'comment':{'required':True}}
    
    def create(self, validated_data):
        user = self.context.get('user')
        comment = CommentModel.objects.create(user=user, **validated_data)
        comment.save()
        return comment

# EDIT COMMENT SERIALIZER
class EditCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentModel
        fields = ['comment']

# DELETE COMMENT SERIALIZER
class DeleteCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentModel
        fields = '__all__'
    
# ALL COMMENT LIST SERIALIZER
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentModel
        fields = ['user','comment','updated_at']

# ALL COMMENTS UNDER A POST SERIALIZER
class PostCommentListSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = PostModel
        fields = ['id','title','content','comments']

    def get_comments(self, obj):
        comments = CommentModel.objects.filter(post=obj)
        try:
            serializer = CommentSerializer(comments, many=True)
        except Exception as e:
            print(e)
        return serializer.data