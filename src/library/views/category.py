# from rest_framework.decorators import api_view
# from rest_framework.request import Request
# from rest_framework.response import Response
# from rest_framework import status
#
# from src.library.models import Category
# from src.library.serializers import CategorySerializer
from django.db.models import Count
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
# @api_view(['GET'])
# def get_all_categories(request: Request) -> Response:
#     response = Category.objects.all()
#
#     serializer = CategorySerializer(
#         response,
#         many=True
#     )
#
#     return Response(
#         data=serializer.data,
#         status=status.HTTP_200_OK
#     )
#
#
# @api_view(['POST'])
# def create_new_category(request: Request) -> Response:
#     raw_data = request.data # RAW JSON DATA FROM FORM | RAW JSON
#
#     serializer = CategorySerializer(data=raw_data)
#
#     if serializer.is_valid():
#         serializer.save()
#
#         return Response(
#             data=serializer.data,
#             status=status.HTTP_201_CREATED
#         )
#     return Response(
#         data=serializer.errors,
#         status=status.HTTP_400_BAD_REQUEST
#     )


from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.mixins import (
    UpdateModelMixin,
    RetrieveModelMixin
)
from rest_framework.decorators import action

from src.library.dtos.category import CategoryDTO
from src.library.models import Category



class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategoryDTO

    @action(methods=['get'], detail=False, url_path='statistic')
    def get_category_statistic(self, request: Request) -> Response:
        qs = Category.objects.annotate(
            books_count=Count('books')
        )

        data = [
            {
                'id': obj.id,
                'title': obj.title,
                'books_count': obj.books_count,
            }
            for obj in qs
        ]

        return Response(
            data=data,
            status=status.HTTP_200_OK
        )

    @action(methods=['get'], detail=False, url_path='custom-method')
    def custom_method(self, request: Request) -> Response:
        return Response(
            data={'message': 'Custom method works!'},
        )
