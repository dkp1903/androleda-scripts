from rest_framework import serializers
from .models import Blog, Tag, BlogCategory

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['name']

class BlogSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, required=False)

    class Meta:
        model = Blog
        fields = ['title', 'link', 'published_date', 'summary', 'category', 'tags']

    def create(self, validated_data):
        tags_data = validated_data.pop('tags', [])
        blog = Blog.objects.create(**validated_data)
        for tag_data in tags_data:
            tag, created = Tag.objects.get_or_create(name=tag_data['name'])
            blog.tags.add(tag)
        return blog
