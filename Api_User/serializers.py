from rest_framework import serializers
from django.contrib.auth.models import User
from Api_User.models import ImageModel
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _

import smtplib
from email.mime.text import MIMEText
from socket import gaierror

# REGISTRATION SERIALIZER
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name','last_name','email','username','password']
        extra_kwargs = {'first_name':{'required':True},'last_name':{'required':True},'email':{'required':True},'username':{'required':True},'password':{'write_only':True, 'required':True}}
    
    def create(self, validated_data):
        email = self.validated_data['email']
        username = self.validated_data['username']
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("Email Already taken. Please try another one")
        elif User.objects.filter(username=username).exists():
            raise serializers.ValidationError('Username already taken')
        else:
            user = User.objects.create(**validated_data)
            user.set_password(validated_data['password'])
            user.save()

            try:
                email_from = 'admin@gmail.com'
                email_to = 'jerin@gmail.com'
                email_subject = 'Registration mail'
                email_body = f"""
                First Name : {user.first_name}\n
                Last Name : {user.last_name}\n
                Email : {user.email}\n
                Username : {user.username}\n
                password : {self._validated_data['password']}\n
                Registration  sucessfull. Please Login with this above credentials
                
                """
                message = MIMEText(email_body)
                message['From'] = email_from
                message['To'] = email_to
                message['Subject'] = email_subject
                smtp_server = 'smtp.mailtrap.io'
                smpt_port = 465
                smtp_username = 'c9afbb9b64a4fe'
                smtp_password = '99d9eb81e7a8ee'
                server = smtplib.SMTP(smtp_server, smpt_port)
                server.starttls()
                server.login(smtp_username, smtp_password)
                server.sendmail(email_from, email_to, message.as_string())
                server.quit()
                print('Mail send successfully..')

                return user
            
            except (gaierror, ConnectionRefusedError):
                print('\n Failed to connect to the server. Check your internet connection.\n')

            except smtplib.SMTPServerDisconnected as s:
                print('\nInvalid credentials...!\n',s)
            except Exception as e:
                print('\nSomething went wrong...!\n',e)

# LOGIN SERIALIZER
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(label=_("Password"),style={'input_type': 'password'},trim_whitespace=False,max_length=128,write_only=True)
    
    def validate(self, data):
        username = data.get('username')
        password = data.get('password')
        if username and password:
            user = authenticate(request=self.context.get('request'),username=username, password=password)
            if not user:
                raise serializers.ValidationError("Invalid username or password.", code='authorization')
        else:
            raise serializers.ValidationError("Username and Password required", code='authorization')
        data['user'] = user
        return data

 
# IMAGE SERIALIZER
class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageModel
        fields = ['post','image']
        extra_kwargs = {'post':{'required':True},'image':{'required':True}}

    
    def create(self, validated_data):
        user = self.context.get('user')
        image = ImageModel.objects.create(user=user, **validated_data)
        image.save()
        return image
    

  
