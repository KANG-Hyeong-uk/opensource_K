from django.contrib import admin
from .models import NewsDocument, DocumentEmbedding, SimilarityCache


@admin.register(NewsDocument)
class NewsDocumentAdmin(admin.ModelAdmin):
    list_display = ['news_id', 'title_short', 'category', 'is_clickbait', 'process_type', 'created_at']
    list_filter = ['is_clickbait', 'category', 'process_type', 'created_at']
    search_fields = ['news_id', 'title', 'content']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('기본 정보', {
            'fields': ('news_id', 'category', 'subcategory')
        }),
        ('콘텐츠', {
            'fields': ('title', 'subtitle', 'content')
        }),
        ('분류', {
            'fields': ('is_clickbait', 'process_type', 'process_pattern', 'process_level')
        }),
        ('문장 정보', {
            'fields': ('sentence_count', 'sentences')
        }),
        ('메타데이터', {
            'fields': ('part_num', 'created_at', 'updated_at')
        }),
    )

    def title_short(self, obj):
        return obj.title[:50] + '...' if len(obj.title) > 50 else obj.title
    title_short.short_description = '제목'


@admin.register(DocumentEmbedding)
class DocumentEmbeddingAdmin(admin.ModelAdmin):
    list_display = ['document_news_id', 'model_name', 'dimension', 'created_at']
    list_filter = ['model_name', 'created_at']
    search_fields = ['document__news_id', 'document__title']
    readonly_fields = ['created_at', 'updated_at']

    def document_news_id(self, obj):
        return obj.document.news_id
    document_news_id.short_description = '문서 ID'


@admin.register(SimilarityCache)
class SimilarityCacheAdmin(admin.ModelAdmin):
    list_display = ['query_text_short', 'hit_count', 'created_at']
    list_filter = ['created_at']
    search_fields = ['query_text', 'query_hash']
    readonly_fields = ['created_at', 'hit_count']

    def query_text_short(self, obj):
        return obj.query_text[:50] + '...' if len(obj.query_text) > 50 else obj.query_text
    query_text_short.short_description = '쿼리'
