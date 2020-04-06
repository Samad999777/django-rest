from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from profiles_api import searlizers
from profiles_api import models
from rest_framework.authentication import TokenAuthentication
from rest_framework import filters
from profiles_api import permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.permissions import IsAuthenticated

# Create your views here.

class HelloAPiView(APIView):
    """Test APi View"""
    serializer_class= searlizers.HelloSerializer
    def get(self, request, format=None):
        """Returns a list of APIView Feature"""
        an_api=['DUMMY DATA API STFF',
        'Dummy data',
        'Dummy Data',
        'Dummy Data',]

        return Response({'message':'Hello',
        'an_apiview':an_api})

    def post(self, request):
        """Create a Hello message with our name"""
        serializer =self.serializer_class(data=request.data)

        if serializer.is_valid():
            name= serializer.validated_data.get('name')
            message=f'Hello {name}'
            return Response({'message':message})
        else:
            return Response(serializer.errors,
             status=status.HTTP_400_BAD_REQUEST)

    def put(self, request,pk=None):
        """Update handeling"""
        return Response({'method':'PUT'})

    def patch(self, request,pk=None):
        """partial Update handeling"""
        return Response({'method':'PATCH'})

    def delete(self,request,pk=None):
        """FOr deleting an object"""
        return Response({"method":'DELETE'})

class HelloViewSet(viewsets.ViewSet):
    serializer_class= searlizers.HelloSerializer


    """TEST API VIEWSET"""


    def list(self, request):
        """Return a hello method"""
        an_api=['DUMMY DATA API STFF',
        'Dummy data',
        'Dummy Data',
        'Dummy Data',]

        return Response({"message":'Hello','viewser_api':an_api})

    def create(self,request):
        serializer= self.serializer_class(data=request.data)

        if serializer.is_valid():
            name=serializer.validated_data.get('name')
            message= f'Hello {name}'
            return Response({'message':message})
        else:
            return Response(
            serializer.errors,
            status= status.HTTP_400_BAD_REQUEST
            )

    def retieve(self, request, pk=None):

        return Response({'http_methos:':'GET'})

    def update(self, request, pk=None):
        return Response({'http_methos:':'PUT'})

    def partial_update(seld, request,pk=None):
        return Response({'http_method':'PATCH'})

    def destory(self, request, pk=None):
        return Response({'http_method' : 'DELETE'})



class UserProfileViewset(viewsets.ModelViewSet):
    """Handle creating and updation profiles"""

    serializer_class= searlizers.UserProfileSerializer
    queryset= models.UserProfile.objects.all()
    authtication_classes= (TokenAuthentication,)
    permission_classes= (permissions.UpdateOwnProfile,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name','email',)


class UserLoginApiView(ObtainAuthToken):
    """Handel creating user auth tokens"""
    renderer_classes= api_settings.DEFAULT_RENDERER_CLASSES

class UserProfileFeedViewset(viewsets.ModelViewSet):
    """Handles creating ,reading and updating feed item"""
    authtication_classes=(TokenAuthentication,)
    serializer_class= searlizers.ProfileFeedItemSerializer
    queryset= models.ProfileFeedItem.objects.all()
    permission_classes= (permissions.UpdateOwnStatus,IsAuthenticated)

    def perform_create(self, serializer):
        """Set user profile to logged in user"""
        serializer.save(user_profile=self.request.user)
