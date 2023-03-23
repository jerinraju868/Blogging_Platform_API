from rest_framework import serializers
from Api_User.models import PostModel, CommentModel

# CREATE POST SERIALIZER
class CreatePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostModel
        fields = ['title','content']
        extra_kwargs = {'title':{'required':True},'content':{'required':True}}
    
    def create(self, validated_data):
        user = self.context.get('user')
        post = PostModel.objects.create(user=user,**validated_data)
        post.save()
        return post


# POST DETAIL SERIALIZER
class DetailPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostModel
        fields = ['id','title','content','updated_at']


# UPDATE POST SERIALIZER
class UpdatePostSerilaizer(serializers.ModelSerializer):
     class Meta:
        model = PostModel
        fields = ['title','content']
        extra_kwargs = {'title':{'required':True},'content':{'required':True}}
    

# DELETE POST SERIALIZER
class DeletePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostModel
        fields = '__all__'


# # MY POST LIST SERIALIZER
# class MyPostListSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = PostModel
#         fields = ['id','title','content']


# ALl POST LIST SERIALIZER
class AllPostListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostModel
        fields = ['id','title','content', 'user']
