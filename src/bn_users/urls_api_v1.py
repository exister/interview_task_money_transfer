from django.conf.urls import url

from ov_videos.api.v1.highlights import HighlightViewSet, TaggedHighlightsViewSet

from .api.v1.tags import MyTagViewSet, PublicTagViewSet, TagViewSet

urlpatterns = [
    url(
        '^tags/$', TagViewSet.as_view({'get': 'list'}),
        name='tag-list'
    ),
    url(
        '^tags/(?P<pk>\d+)/$', TagViewSet.as_view({'get': 'retrieve'}),
        name='tag-details'
    ),

    url(
        '^tags/public/$', PublicTagViewSet.as_view({'get': 'list'}),
        name='tag-list'
    ),
    url(
        '^tags/public/(?P<pk>\d+)/$', PublicTagViewSet.as_view({'get': 'retrieve'}),
        name='tag-details'
    ),

    url(
        '^tags/my/$', MyTagViewSet.as_view({'get': 'list', 'post': 'create'}),
        name='tag-my-list'
    ),
    url(
        '^tags/my/(?P<pk>\d+)/$', MyTagViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}),
        name='tag-my-details'
    ),

    url(
        '^tags/(?P<parent_lookup_tags>\d+)/highlights/$', HighlightViewSet.as_view({'get': 'list'}),
        name='tag-highlight-list'
    ),
    url(
        '^tags/(?P<parent_lookup_tags>\d+)/highlights/(?P<pk>\d+)/$', HighlightViewSet.as_view({'get': 'retrieve'}),
        name='tag-highlight-details'
    ),

    url(
        '^tags/helpers/tagged-highlights/$', TaggedHighlightsViewSet.as_view({'get': 'list'}),
        name='tagged-highlights-list'
    ),
]
