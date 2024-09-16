from rest_framework.generics import GenericAPIView, CreateAPIView, DestroyAPIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from favorites.serializers.favorites.serializers import FavoriteSerializer
from favorites.models import Favorite


class FavoriteCreateView(CreateAPIView):
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated]


class FavoriteListView(GenericAPIView):
    serializer_class = FavoriteSerializer
    queryset = Favorite.objects.all()

    def get(self, request, *args, **kwargs):
        if not bool(request.user and request.user.is_authenticated):
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        queryset = self.get_queryset().filter(user_id=request.user.id)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status.HTTP_200_OK)


class FavoriteDeleteView(DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Favorite.objects.filter(user_id=self.request.user.id)


