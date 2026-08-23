import django_filters

from .models import Post


class PostFilter(django_filters.FilterSet):

    # Filter posts by title
    title = django_filters.CharFilter(
        field_name="title",
        lookup_expr="icontains"
    )

    # Filter published posts
    published = django_filters.BooleanFilter(
        field_name="published"
    )

    # Simple date filter
    created_at = django_filters.DateFilter(
        field_name="created_at",
        lookup_expr="date"
    )

    class Meta:
        model = Post

        fields = [
            "title",
            "published",
            "created_at"
        ]