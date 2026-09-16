from django.forms import ModelForm, TextInput, Textarea, NumberInput, URLInput, CheckboxInput, Select

from main.models import Education

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
                attrs={
                    "placeholder": "Masukkan tahun mulai pendidikan",
                }
            ),
            "end_year": NumberInput(
                attrs={
                    "placeholder": "Masukkan tahun selesai pendidikan",
                }
            ),
            "skills": TextInput(
                attrs={
                    "placeholder": "Masukkan skills yang kamu dapatkan",
                }
            ),
            "thumbnail": URLInput(
                attrs={
                    "placeholder": "https://drive.google.com/thumbnail?id=...&sz=w1000",
                }
            ),
        }