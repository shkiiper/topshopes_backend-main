import Response as Response
from rest_framework import mixins, permissions, viewsets
from rest_framework.response import Response
from core.permissions import HasShop

from .models import AttributeValue, Attribute
from .serializers import AttributeValueSerializer, AttributeSerializer


class AttributeValueViewset(
    mixins.UpdateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet
):
    """
    Viewset to delete and update product attributes
    Awailable only for sellers
    """

    queryset = AttributeValue.objects.all()
    serializer_class = AttributeValueSerializer
    permission_classes = [permissions.IsAuthenticated, HasShop]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        # удаляем все значения, связанные с атрибутом
        instance.values.all().delete()
        return Response(serializer.data)