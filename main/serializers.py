from rest_framework import serializers
from main.models import Experience, Education
from main.forms import clean_text, clean_thumbnail_url

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
        return clean_text(value, "Judul experience")

    def validate_description(self, value):
        return clean_text(value, "Deskripsi")

    thumbnail = serializers.CharField(required=False, allow_blank=True, allow_null=True, max_length=200)
    def validate_thumbnail(self, value):
        return clean_thumbnail_url(value)
    
class EducationSerializer(serializers.ModelSerializer):
    category_edu_display = serializers.CharField(
        source="get_category_edu_display", read_only=True,
    )
    skill_list = serializers.ReadOnlyField()
    star_count = serializers.SerializerMethodField()
    is_starred = serializers.SerializerMethodField()
    starred_by_names = serializers.SerializerMethodField()

    class Meta:
        model = Education
        fields = [
            "id", "title", "description", "category_edu", "category_edu_display",
            "start_year", "end_year", "is_ongoing", "skills", "skill_list",
            "thumbnail", "star_count", "is_starred", "starred_by_names",
        ]
        read_only_fields = ["id"]

    def get_star_count(self, obj):
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
        return clean_text(value, "Nama institusi/jenjang")

    def validate_description(self, value):
        return clean_text(value, "Deskripsi")

    def validate_skills(self, value):
        return clean_text(value, "Skills", required=False)

    def validate(self, attrs):
        def current(name, default=None):
            return attrs.get(name, getattr(self.instance, name, default))

        start, end, ongoing = current("start_year"), current("end_year"), current("is_ongoing", False)
        if ongoing and end is not None:
            raise serializers.ValidationError(
                {"end_year": "Pendidikan yang masih berlangsung tidak boleh punya tahun selesai."}
            )
        if not ongoing and end is None:
            raise serializers.ValidationError(
                {"end_year": "Pendidikan yang sudah selesai harus punya tahun selesai."}
            )
        if start is not None and end is not None and end < start:
            raise serializers.ValidationError(
                {"end_year": "Tahun selesai tidak boleh lebih awal dari tahun mulai."}
            )
        return attrs