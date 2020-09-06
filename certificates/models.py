from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


# Create your models here.

class font(models.Model):

    font_id = models.AutoField(primary_key=True)
    font_name = models.CharField(max_length = 50)
    font_file = models.FileField(upload_to='fonts',blank = True, null = True)

    def __str__(self):
        return '%s %s' % (self.font_id, self.font_name)


class certificate(models.Model):

    cert_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length = 50)
    dimensions = models.TextField()
    tags = models.TextField()
    desc = models.TextField()
    image1 = models.ImageField( upload_to='certificate_templates',blank = True, null = True)
    image2 = models.ImageField( upload_to='certificate_templates',blank = True, null = True)
    image3 = models.ImageField( upload_to='certificate_templates',blank = True, null = True)

    #font details
    font_used = models.ForeignKey(font ,default = None, on_delete=models.SET_DEFAULT)
    font_size1 = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(72)],default=0)
    font_size2 = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(72)], default=0)

    def __str__(self):
        return '%s %s' % (self.cert_id,self.name)