from rest_framework import serializers
from django.contrib.auth.models import User
from Api_User.models import PostModel, CommentModel

# REGISTER SUPERUSER SERIALIZER
class RegisterSuperuserSerializer(serializers.ModelSerializer):
    is_superuser = serializers.BooleanField(read_only=True)
    is_staff = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = User
        fields = ['first_name','last_name','email','username','password','is_superuser','is_staff']
        extra_kwargs = {'first_name':{'required':True},
                        'last_name':{'required':True},
                        'email':{'required':True},
                        'username':{'required':True},
                        'password':{'write_only':True, 'required':True}
                        }
    
    def create(self, validated_data):
        email = self.validated_data['email']
        username = self.validated_data['username']
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("Email Already taken. Please try another one")
        elif User.objects.filter(username=username).exists():
            raise serializers.ValidationError('Username already taken')
        else:
            user = User.objects.create_superuser(**validated_data)
            user.set_password(validated_data['password'])
            user.save()
            return user
        
# POST SERIALIZER
class AdminPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostModel
        fields = '__all__'


# ALL COMMENTS
class AdminCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentModel
        exclude = ['post']
    
    def to_representation(self, instance):
        rep = super(AdminCommentSerializer, self).to_representation(instance)
        rep['user'] = instance.user.username
        return rep


# COMMENT SERIALIZER 
class AdminPostCommentListSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = PostModel
        fields = ['id','title','content','comments']

    def get_comments(self, obj):
        comments = CommentModel.objects.filter(post=obj)
        try:
            serializer = AdminCommentSerializer(comments, many=True)
        except Exception as e:
            print(e)
        return serializer.data
    
   
