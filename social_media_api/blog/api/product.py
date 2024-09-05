from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.views import extend_schema

from ..models import Product
from ..selectors.product import get_products
from ..services.product import create_product


class ProductView(APIView):

    class InputSerializer(serializers.Serializer):
        name = serializers.CharField(max_length=10)

    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Product
            fields = ["name", "created_at", "updated_at"]

    @extend_schema(responses=OutputSerializer)
    def get(self, request):
        queryset = get_products()
        return Response(data=self.OutputSerializer(instance=queryset, context={'request': request}, many=True).data)

    @extend_schema(request=InputSerializer(), responses=OutputSerializer)
    def post(self, request):
        query = self.InputSerializer(data=request.data)
        query.is_valid(raise_exception=True)
        try:
            product = create_product(name=query.validated_data["name"])
        except Exception as e:
            return Response(
                data=f"there is error we can't save the prodcut object details {e}",
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(data=self.OutputSerializer(instance=product, context={"request": request}).data)

