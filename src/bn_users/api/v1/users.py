from rest_framework.filters import SearchFilter
from rest_framework.viewsets import ModelViewSet

from .serializers.users import UserSerializer
from ...models import User


class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    filter_backends = (SearchFilter,)
    search_fields = ('first_name', 'last_name', 'email', 'inn')
