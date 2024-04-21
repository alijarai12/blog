from rest_framework.response import Response
from home.serializers import BlogSerializer
from home.models import BlogPost
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.core.paginator import Paginator
from rest_framework.authentication import BasicAuthentication
from rest_framework.generics import ListAPIView


class BlogListView(ListAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogSerializer


class BlogDetailAPIView(APIView):

    def get_object(self, pk):
        try:
            return BlogPost.objects.get(pk=pk)
        except BlogPost.DoesNotExist:
            return None

    def get(self, request, pk, *args, **kwargs):
        post = self.get_object(pk)
        if post is None:
            return Response(
                {"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = BlogSerializer(post)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BlogView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [BasicAuthentication]

    def get(self, request):
        try:
            blog = BlogPost.objects.filter(user=request.user)

            serializer = BlogSerializer(blog, many=True)

            return Response(
                {"data": serializer.data, "message": "blog fetched"},
                status=status.HTTP_201_CREATED,
            )

        except Exception as e:
            return Response(
                {"data": serializer.errors, "message": "wrong"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def post(self, request):
        try:
            data = request.data
            data["user"] = request.user.id
            serializer = BlogSerializer(data=data)

            if not serializer.is_valid():
                return Response(
                    {"data": serializer.errors, "message": "something wrong"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            serializer.save()

            return Response(
                {"data": serializer.data, "message": "blog created"},
                status=status.HTTP_201_CREATED,
            )

        except Exception as e:
            return Response(
                {"data": serializer.errors, "message": "something wrong"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def patch(self, request):
        try:
            data = request.data
            blog = BlogPost.objects.filter(id=data.get("id"))

            if not blog.exists():
                return Response(
                    {"data": {}, "message": "invalid blog id"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if request.user != blog[0].user:
                return Response(
                    {"data": {}, "message": "you are not authorized to this"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            serializer = BlogSerializer(blog[0], data=data, partial=True)

            if not serializer.is_valid():
                return Response(
                    {"data": serializer.errors, "message": "something wrong"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            serializer.save()

            return Response(
                {"data": serializer.data, "message": "blog updated"},
                status=status.HTTP_201_CREATED,
            )

        except Exception as e:
            return Response(
                {"data": {}, "message": "something wrong"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def delete(self, request):
        try:
            data = request.data
            blog = BlogPost.objects.filter(id=data.get("id"))

            if not blog.exists():
                return Response(
                    {"data": {}, "message": "invalid blog id"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if request.user != blog[0].user:
                return Response(
                    {"data": {}, "message": "you are not authorized to this"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            serializer = BlogSerializer(blog[0], data=data, partial=True)

            blog[0].delete()

            return Response(
                {"data": {}, "message": "blog deleted"}, status=status.HTTP_201_CREATED
            )

        except Exception as e:
            return Response(
                {"data": {}, "message": "wrong"}, status=status.HTTP_400_BAD_REQUEST
            )
