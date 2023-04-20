from rest_framework import status
from rest_framework import mixins, permissions, viewsets
from rest_framework.response import Response
from core.permissions import HasShop
from .models import AttributeValue
from .serializers import AttributeValueSerializer


class AttributeValueViewset(
    mixins.UpdateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet
):
    """
    Viewset to delete and update product attributes
    Available only for sellers
    """

    queryset = AttributeValue.objects.all()
    serializer_class = AttributeValueSerializer
    permission_classes = [permissions.IsAuthenticated, HasShop]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        value = request.data.get('value', None)
        if not value:
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
