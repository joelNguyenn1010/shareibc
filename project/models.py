from django.db import models
from django.core.exceptions import ValidationError


from PIL import Image
def filepath_images(instance, filename):
    title = instance.project.name
    return 'projects/%s-%s' % (title, filename)

def filepath_front_images(instance, filename):
    title = instance.name
    return 'projects/%s-%s' % (title, filename)


def validate_image(value):
    if value.width != 1920 and value.height != 1080:
        raise ValidationError("The image should be in HD format (1920x1080)")
    else:
        return value


class Project(models.Model):
    name = models.CharField(max_length=165)
    location = models.TextField()
    target_fund = models.DecimalField(max_digits=15, decimal_places=2)
    fund = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    area = models.CharField(max_length=65)
    about_this_project = models.TextField()
    image = models.ImageField(upload_to=filepath_front_images, validators=[validate_image])
    # date = models.DateField(auto_now_add=True, blank=True, default=None, null=True)

    # def save(self, *args, **kwargs):
    #     if not self.image:
    #         return
    #     if
    #     super().save()
    #     img = Image.open(storage.open(self.image.name))
    #     print(img.size)
    #     output_size = (1920, 1080)
    #     img.resize(output_size)
    #     img.save(self.image)
        #
        # user = super(Project, self).save()
        # try:
        #     image = Image.open(user.primaryphoto)
        #     resized_image = image.resize((1920, 1080), Image.ANTIALIAS)
        #     resized_image.save(user.primaryphoto.path)
        # except:
        #     pass
        # return user



class ProjectImage(models.Model):
    name = models.CharField(max_length=165)
    images = models.ImageField(upload_to=filepath_images)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='images_project', validators=[validate_image])

