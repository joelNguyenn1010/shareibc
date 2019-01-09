from .models import Project, ProjectImage
from rest_framework import serializers
class ImageSeriallizer(serializers.ModelSerializer):
    class Meta:
        model = ProjectImage
        fields = ['name', 'images']

class ProjectSerializer(serializers.ModelSerializer):
    images_project = ImageSeriallizer(many=True)
    class Meta:
        model = Project
        fields = ('id','name', 'fund', 'image','target_fund','area','about_this_project','location','images_project')

