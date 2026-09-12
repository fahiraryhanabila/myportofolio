from django.db import models

# Create your models here.
import uuid
from django.db import models

class Experience(models.Model):
    EXPERIENCE_CHOICES = [
        ('internship', 'Internship'),
        ('research', 'Research'),
        ('volunteer', 'Volunteer'),
        ('part-time', 'Part-Time'),
        ('full-time', 'Full-Time'),
        ('freelance', 'Freelance'),
    ]
        
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=EXPERIENCE_CHOICES, default='full-time')
    thumbnail = models.URLField(blank=True, null=True)
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(blank=True, null=True)
    def __str__(self):
        return self.title
    
    @property
    def is_ongoing(self):
        return self.ended_at is None
    
class Education(models.Model):
    EDUCATIONAL_LEVEL = [
        ("Elementary School", "elementary school"),
        ("Junior High School", "junior high school"),
        ("Senior High School", "senior high school"),
        ("Bachelor's Degree", "bachelor's degree"),
    ]
    title = models.CharField(max_length=255, default="")
    is_ongoing = models.BooleanField(default=False)
    start_year = models.IntegerField()
    description = models.TextField()
    end_year = models.IntegerField(null=True, blank=True) 
    category_edu = models.CharField(max_length=20, choices=EDUCATIONAL_LEVEL)
    skills = models.CharField(max_length=255, blank=True, default="")
    thumbnail = models.URLField(blank=True, null=True)
    
    def __str__(self):
        return self.title
    
    @property
    def skill_list(self):
        return [s.strip() for s in self.skills.split(",") if s.strip()]
