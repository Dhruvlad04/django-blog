import django_filters

from .models import Post


class PostFilter(django_filters.FilterSet):

    # Search posts by author
    author = django_filters.CharFilter(
        field_name="author",
        lookup_expr="icontains"
    )

    # Search posts by title
    title = django_filters.CharFilter(
        field_name="title",
        lookup_expr="icontains"
    )

    # Filter published/unpublished posts
    published = django_filters.BooleanFilter(
        field_name="published"
    )

    class Meta:
        model = Post

        fields = [
            "author",
            "title",
            "published"
        ]