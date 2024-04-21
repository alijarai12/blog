from rest_framework.response import Response
from home.serializers import BlogSerializer, BlogCommentSerializer
from home.models import BlogPost, BlogComment
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status


class BlogListView(APIView):
    serializer_class = BlogSerializer

    def get(self, request):
        blog = BlogPost.objects.all()
        blog_data = self.serializer_class(blog, many=True).data
        return Response({"data": blog_data}, status=status.HTTP_200_OK)
   
class BlogView(APIView):
    serializer_class = BlogSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        id = request.query_params.get('id')
        try:
            blog = BlogPost.objects.get(id=id)
        except BlogPost.DoesNotExist:
            return Response({"error": "Blog post not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.serializer_class(blog)  # Pass the instance of the blog post to the serializer
        data = serializer.data

        return Response({'result': data}, status=status.HTTP_200_OK)
    
    
    
    def post(self, request):
        data = request.data
        user = request.user
        data['user'] = user.id

        serializer = self.serializer_class(data=data)
        
        if serializer.is_valid(): 
            serializer.save()
        
            return Response({"data": serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)       


    def patch(self, request):
        # Update an existing blog post based on the id query parameter in the URL
        blog_id = request.query_params.get('id')  # Retrieve the blog post ID from query parameters
        user = request.user

        try:
            blog_post = BlogPost.objects.get(id=blog_id, user=user)
        except BlogPost.DoesNotExist:
            return Response({'error':'blog not found for this id'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.serializer_class(blog_post, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({'error':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        try:
            blog_id = request.query_params.get('id')
            user = request.user
            blog_object = BlogPost.objects.filter(id=blog_id, user=user)

            if blog_object:
                blog_object.delete()
                return Response('blog has been deleted') 
            
            else:
                return Response({'blog doesnot exist'})

        except Exception as e:
            return Response(
                {"data": {}, "message": "something wrong"}, status=status.HTTP_400_BAD_REQUEST
            )
        

class BlogCommentView(APIView):
    serializer_class = BlogCommentSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        
        comment = BlogComment.objects.all()
        serializer = self.serializer_class(comment, many=True)  # Pass the instance of the blog post to the serializer
        data = serializer.data

        if data:
            return Response({'reult':data}, status=status.HTTP_200_OK)
        else:
            return Response({'no comment found'})       

    def post(self, request):

        data = request.data
        user = request.user

        data['user'] = user.id

        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            serialized_data = serializer.data
            return Response({'reult':serialized_data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)       


    def patch(self, request, id):
        try:
            cmt = BlogComment.objects.get(id=id)  # Retrieve the specific comment by ID
        except BlogComment.DoesNotExist:
            return Response({"error": "Comment not found"}, status=status.HTTP_404_NOT_FOUND)
        
        user = request.user

        if cmt.user == user:
            serializer = self.serializer_class(cmt, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                serialized_data = serializer.data
                return Response({'result': 'Comment updated', 'data': serialized_data}, status=status.HTTP_200_OK)
            else:
                return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)       
        else:
            return Response({"error": "You are not authorized to update this comment"}, status=status.HTTP_403_FORBIDDEN)