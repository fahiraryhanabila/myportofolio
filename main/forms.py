from django.core.exceptions import ValidationError
from django.forms import (
    CheckboxInput,
    DateTimeInput,
    ModelForm,
    NumberInput,
    Select,
    Textarea,
    TextInput,
    URLInput,
)
from django.utils.html import strip_tags

from main.models import Education, Experience


def clean_text(value, field_label, required=True):
    cleaned = strip_tags(value or "").strip()
    if required and not cleaned:
        raise ValidationError(f"{field_label} tidak boleh hanya berisi tag HTML.")
    return cleaned


def clean_thumbnail_url(value):
    thumbnail = (value or "").strip()
    if not thumbnail:
        return thumbnail
    lowered = thumbnail.lower()
    if thumbnail.startswith("//"):
        raise ValidationError("URL thumbnail tidak valid.")
    if not (thumbnail.startswith("/") or lowered.startswith(("http://", "https://"))):
        raise ValidationError("URL thumbnail harus diawali http://, https://, atau /.")
    return thumbnail


class EducationForm(ModelForm):
    class Meta:
        model = Education
        fields = [
            "title",
            "category_edu",
            "description",
            "is_ongoing",
            "start_year",
            "end_year",
            "skills",
            "thumbnail",
        ]

        labels = {
            "title": "Nama Institusi/Jenjang",
            "category_edu": "Jenjang Pendidikan",
            "description": "Deskripsi",
            "is_ongoing": "Masih Berlangsung?",
            "start_year": "Tahun Mulai",
            "end_year": "Tahun Selesai",
            "skills": "Skill (pisahkan dengan koma)",
            "thumbnail": "URL Gambar",
        }

        widgets = {
            "title": TextInput(
                attrs={
                    "placeholder": "Masukkan jenjang pendidikanmu",
                    "maxlength": 255,
                }
            ),
            "category_edu": Select(),
            "description": Textarea(
                attrs={
                    "placeholder": "Ceritakan pengalaman pendidikanmu",
                    "rows": 3,
                }
            ),
            "is_ongoing": CheckboxInput(),
            "start_year": NumberInput(
                attrs={"placeholder": "Masukkan tahun mulai pendidikan"}
            ),
            "end_year": NumberInput(
                attrs={"placeholder": "Masukkan tahun selesai pendidikan"}
            ),
            "skills": TextInput(
                attrs={"placeholder": "Masukkan skills yang kamu dapatkan"}
            ),
            "thumbnail": URLInput(
                attrs={
                    "placeholder": "https://drive.google.com/thumbnail?id=...&sz=w1000",
                }
            ),
        }

    def clean_title(self):
        return clean_text(self.cleaned_data["title"], "Nama institusi/jenjang")

    def clean_description(self):
        return clean_text(self.cleaned_data["description"], "Deskripsi")

    def clean_skills(self):
        return clean_text(self.cleaned_data.get("skills", ""), "Skills", required=False)

    def clean_thumbnail(self):
        return clean_thumbnail_url(self.cleaned_data.get("thumbnail"))


class ExperienceForm(ModelForm):
    class Meta:
        model = Experience
        fields = [
            "title",
            "description",
            "category",
            "thumbnail",
            "ended_at",
        ]

        labels = {
            "title": "Judul Pengalaman",
            "description": "Deskripsi",
            "category": "Jenis Kegiatan",
            "thumbnail": "URL Gambar",
            "ended_at": "Tanggal Selesai",
        }

        widgets = {
            "title": TextInput(
                attrs={"placeholder": "Masukkan nama experience atau pengalaman"}
            ),
            "description": Textarea(
                attrs={"placeholder": "Ceritakan pengalamanmu", "rows": 3}
            ),
            "category": Select(),
            "thumbnail": TextInput(
                attrs={"placeholder": "https://... atau /static/img/foto.jpeg"}
            ),
            "ended_at": DateTimeInput(
                attrs={
                    "type": "datetime-local",
                    "placeholder": "Pilih tanggal selesai",
                },
                format="%Y-%m-%dT%H:%M",
            ),
        }

    def clean_title(self):
        return clean_text(self.cleaned_data["title"], "Judul experience")

    def clean_description(self):
        return clean_text(self.cleaned_data["description"], "Deskripsi")

    def clean_thumbnail(self):
        return clean_thumbnail_url(self.cleaned_data.get("thumbnail"))