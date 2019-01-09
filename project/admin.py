from django.contrib import admin
from .models import Project, ProjectImage
from image_cropping import ImageCroppingMixin

# Register your models here.
class ImageInLine(admin.TabularInline):
    model = ProjectImage

class MyModelAdmin(ImageCroppingMixin, admin.ModelAdmin):
    pass


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'fund', 'target_fund')
    list_filter = ('name', 'target_fund')
    inlines = [ImageInLine,]


admin.site.register(Project, ProjectAdmin)
admin.site.register(ProjectImage)

