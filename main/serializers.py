from rest_framework import serializers
from main.models import Experience


class ExperienceSerializer(serializers.ModelSerializer):
    is_ongoing = serializers.ReadOnlyField()
    star_count = serializers.SerializerMethodField()
    is_starred = serializers.SerializerMethodField()
    category_display = serializers.CharField(source="get_category_display", read_only=True)
    starred_by_names = serializers.SerializerMethodField()

    class Meta:
        model = Experience
        fields = [
            "id", "title", "description", "category", "category_display", "thumbnail",
            "started_at", "ended_at", "is_ongoing",
            "star_count", "is_starred", "starred_by_names",
        ]
        read_only_fields = ["id", "started_at"]

    def get_star_count(self, obj):
        # len(.all()) memakai hasil prefetch, .count() akan query ulang
        return len(obj.starred_by.all())

    def get_is_starred(self, obj):
        request = self.context.get("request")
        user = getattr(request, "user", None)
        if not user or not user.is_authenticated:
            return False
        return any(u.pk == user.pk for u in obj.starred_by.all())
    
    def get_starred_by_names(self, obj):
        return ", ".join(u.username for u in obj.starred_by.all())
    
    def validate_title(self, value):
        if "<" in value or ">" in value:
            raise serializers.ValidationError("Judul tidak boleh mengandung karakter < atau >.")
        return value

    def validate_thumbnail(self, value):
        if value and not value.startswith(("http://", "https://")):
            raise serializers.ValidationError("Thumbnail harus berupa URL http atau https.")
        return value