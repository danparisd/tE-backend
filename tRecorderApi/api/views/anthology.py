from api.models import Anthology
from api.serializers import AnthologySerializer
from django.utils.decorators import method_decorator
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import SuspiciousOperation


@method_decorator(name='list', decorator=swagger_auto_schema(
    operation_description="Return list of anthologies based on given query string",
    manual_parameters=[
        openapi.Parameter(
            name='id', in_=openapi.IN_QUERY,
            type=openapi.TYPE_INTEGER,
            description="Id of an anthology",
        ), openapi.Parameter(
            name='slug', in_=openapi.IN_QUERY,
            type=openapi.TYPE_STRING,
            description="An Anthology slug",
        ),
    ]
))
class AnthologyViewSet(viewsets.ModelViewSet):
    queryset = Anthology.objects.all()
    serializer_class = AnthologySerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def build_params_filter(self, query):
        pk = query.get("id", None)
        slug = query.get("slug", None)

        filter = {}
        if pk is not None:
            filter["id"] = pk
        if slug is not None:
            filter["slug__iexact"] = slug
        return filter

    def get_queryset(self):
        queryset = Anthology.objects.all()
        if self.request.query_params:
            filter = self.build_params_filter(self.request.query_params)
            if filter:
                return queryset.filter(**filter)
            else:
                raise SuspiciousOperation
        return queryset
