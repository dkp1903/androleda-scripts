from rest_framework import viewsets, filters, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from django.core.cache import cache
from .models import Blog
from .serializers import BlogSerializer

class BlogViewSet(viewsets.ModelViewSet):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['title', 'summary', 'category__name', 'tags__name']

    @action(detail=False, methods=['get'])
    def search(self, request):
        title = request.query_params.get('title', None)
        tags = request.query_params.getlist('tags', None)
        category = request.query_params.get('category', None)
        from_date = request.query_params.get('from_date', None)
        to_date = request.query_params.get('to_date', None)

        # Generate cache key
        cache_key = f'search_{title}_{tags}_{category}_{from_date}_{to_date}'
        cached_result = cache.get(cache_key)
        
        if cached_result:
            return Response(cached_result, status=status.HTTP_200_OK)

        query = Q()

        if title:
            query &= Q(title__icontains=title)
        if category:
            query &= Q(category__name__icontains=category)
        if tags:
            query &= Q(tags__name__in=tags)
        if from_date and to_date:
            query &= Q(published_date__range=[from_date, to_date])

        blogs = Blog.objects.filter(query).distinct()
        serializer = self.get_serializer(blogs, many=True)

        # Cache the result
        cache.set(cache_key, serializer.data, timeout=60 * 5)  # Cache for 5 minutes
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def ingest(self, request):
        """ 
        Endpoint for Kafka consumer to send data to 
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
