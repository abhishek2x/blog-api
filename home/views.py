from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from home.serializers import BlogSerializer
from home.models import Blog
from django.db.models import Q
from django.core.paginator import Paginator


class PublicBlogView(APIView):
    
    def get(self, request):
        try:
            blogs = Blog.objects.all().order_by('?')
            
            if request.GET.get('search'):
                search = request.GET.get('search')
                blogs = blogs.filter(Q(blog_title__icontains = search) | Q(blog_text__icontains = search))
            
            
            page_number = request.GET.get('page', 1)
            paginator = Paginator(blogs, 5)
            serializer = BlogSerializer(paginator.page(page_number), many = True)
                    
            return Response({
                    'data': serializer.data,
                    'message': 'Blog fetched Successfully'
                }, status = status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                "data" : {},
                "message": "Something went wrong or invalid page"
            })
    


class BlogView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    # Lists all blogs created by the logged in User
    def get(self, request):
        try:
            blogs = Blog.objects.filter(blog_author = request.user)
            
            if request.GET.get('search'):
                search = request.GET.get('search')
                blogs = blogs.filter(Q(blog_title__icontains = search) | Q(blog_text__icontains = search))
            
            serializer = BlogSerializer(blogs, many = True)
            
            return Response({
                    'data': serializer.data,
                    'message': 'Blog fetched Successfully'
                }, status = status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                "data" : e,
                "message": "Something went wrong"
            })
    
    
    # Creates a new blog for the User
    def post(self, request):
        try:
            data = request.data
            data['blog_author'] = request.user.id 
            serializer = BlogSerializer(data = data)

            if not serializer.is_valid():
                return Response({
                    'data': serializer.errors,
                    'message': 'something went wrong (ps: check serializer)'
                }, status = status.HTTP_400_BAD_REQUEST)
        
            serializer.save()
            
            return Response({
                    'data': serializer.data,
                    'message': 'Blog Created Successfully'
                }, status = status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response({
                'data': {},
                'message': 'something went wrong'
            }, status = status.HTTP_400_BAD_REQUEST)
        
    
    def patch(self, request):
        try:
            data = request.data
            blog = Blog.objects.filter(uid = data.get('uid'))
            
            if not blog.exists():
                return Response({
                    'data': {},
                    'message': 'Invalid blog ID'
                }, status = status.HTTP_400_BAD_REQUEST)
            
            if blog[0].blog_author != request.user: 
                return Response({
                    'data': {},
                    'message': 'you are not authorized to this blog'
                }, status = status.HTTP_406_NOT_ACCEPTABLE)
        
            serializer = BlogSerializer(blog[0], data = data, partial=True)
                
            if not serializer.is_valid():
                return Response({
                    'data': serializer.errors,
                    'message': 'Serializer error'
                }, status = status.HTTP_400_BAD_REQUEST)

            serializer.save()
            
            return Response({
                    'data': serializer.data,
                    'message': 'Blog Updated Successfully'
                }, status = status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response({
                'data': {},
                'message': 'something went wrong'
            }, status = status.HTTP_400_BAD_REQUEST)
        
    
    def delete(self, request):
        try:
            data = request.data
            blog = Blog.objects.filter(uid = data.get('uid'))
            
            if not blog.exists():
                return Response({
                    'data': {},
                    'message': 'Invalid blog ID'
                }, status = status.HTTP_400_BAD_REQUEST)
            
            if blog[0].blog_author != request.user: 
                return Response({
                    'data': {},
                    'message': 'you are not authorized to this blog'
                }, status = status.HTTP_406_NOT_ACCEPTABLE)

            blog[0].delete()
            
            return Response({
                    'data': {},
                    'message': 'Blog deleted Successfully'
                }, status = status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response({
                'data': {},
                'message': 'something went wrong'
            }, status = status.HTTP_400_BAD_REQUEST)
        