import django_filters

from .models import Post


class PostFilter(django_filters.FilterSet):

    # Search by title
    title = django_filters.CharFilter(
        field_name="title",
        lookup_expr="icontains"
    )

    # Filter published or unpublished posts
    published = django_filters.BooleanFilter(
        field_name="published"
    )

    # Find posts created after a date/time
    created_after = django_filters.DateTimeFilter(
        field_name="created_at",
        lookup_expr="gte"
    )

    # Find posts created before a date/time
    created_before = django_filters.DateTimeFilter(
        field_name="created_at",
        lookup_expr="lte"
    )

    class Meta:
        model = Post

        fields = [
            "title",
            "published",
            "created_after",
            "created_before"
        ]