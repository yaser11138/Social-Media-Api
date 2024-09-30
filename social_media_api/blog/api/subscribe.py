from django.shortcuts import reverse
from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from drf_spectacular.views import extend_schema
from ..models import Subscribe
from ..selectors.subscribe import get_subscribe_detail, get_followers, get_followings
from ..services.subscribe import create_subscribe, delete_subscribe
from social_media_api.api.mixins import ApiAuthMixin


class SubscribeApi(ApiAuthMixin, APIView):

    class SubscribeInputSerializer(serializers.Serializer):
        email = serializers.EmailField()

    class SubscribeOutputSerializer(serializers.ModelSerializer):
        url = serializers.SerializerMethodField()
        subscriber = serializers.SerializerMethodField()
        target = serializers.SerializerMethodField()

        class Meta:
            model = Subscribe
            fields = ["subscriber", "target", "url"]

        def get_target(self, obj):
            return obj.target.email

        def get_subscriber(self, obj):
            return obj.subscriber.email

        def get_url(self, obj):
            request = self.context.get("request")
            path = reverse("api:blog:subscribe-detail", args=[obj.uuid])
            return request.build_absolute_uri(path)

    @extend_schema(request=SubscribeInputSerializer, responses=SubscribeOutputSerializer)
    def post(self, request):
        subscribe_data = self.SubscribeInputSerializer(data=request.data)
        subscribe_data.is_valid(raise_exception=True)
        try:
            subscribe = create_subscribe(
                subscriber=request.user,
                target_email=subscribe_data.validated_data["email"]
            )
        except Exception as e:
            return Response(data={"errors": f"Something went wrong {e}"}, status=status.HTTP_400_BAD_REQUEST)

        return Response(data=self.SubscribeOutputSerializer(instance=subscribe, context={"request": request}).data, status=status.HTTP_201_CREATED)

    @extend_schema(responses=SubscribeOutputSerializer)
    def get(self, request):
        users_following = get_followings(user=request.user)
        user_followers = get_followers(user=request.user)
        users_following_data = self.SubscribeOutputSerializer(instance=users_following, many=True, context={"request": request}).data
        user_followers_data = self.SubscribeOutputSerializer(instance=user_followers, many=True, context={"request": request}).data
        subscribe_data = {
            "users_following": users_following_data,
            "user_followers": user_followers_data
        }
        return Response(data=subscribe_data,status=status.HTTP_200_OK)


class SubscribeDetailApi(ApiAuthMixin, APIView):
    class SubscribeDetailOutputSerializer(serializers.ModelSerializer):
        duration = serializers.SerializerMethodField("get_duration")
        subscriber = serializers.SerializerMethodField()
        target = serializers.SerializerMethodField()


        class Meta:
            model = Subscribe
            fields = ["target", "subscriber", "created_at", "duration"]

        def get_duration(self, obj):
            return timezone.now() - obj.created_at

        def get_target(self, obj):
            return obj.target.email

        def get_subscriber(self, obj):
            return obj.subscriber.email


    def get(self, request, uuid):
        try:
            subscribe = get_subscribe_detail(uuid=uuid)
        except Exception as e:
            return Response(data={"error": f"Subscribe Not Found {e}"}, status=status.HTTP_404_NOT_FOUND)
        return Response(
            data=self.SubscribeDetailOutputSerializer(instance=subscribe, context={"request": request}).data,
            status=status.HTTP_200_OK
        )

    def delete(self, request, uuid):
        try:
            delete_subscribe(uuid=uuid, user=request.user)
        except Exception as e:
            return Response(data={"error": f"Subscribe Not Found {e} "}, status=status.HTTP_404_NOT_FOUND)
        return Response(data={"success": "subscription deleted"}, status=status.HTTP_200_OK)




