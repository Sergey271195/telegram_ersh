from django.db import models

class Section(models.Model):

    section_title = models.CharField(max_length = 300, unique = True, blank = True, null = True)
    additional_info = models.CharField(max_length = 500, blank = True, null = True)
    img_url = models.CharField(max_length = 500, blank = True, null = True)

    def __str__(self):
        return(f'{self.section_title} + {self.additional_info}')

class Dish(models.Model):

    section = models.ForeignKey(Section, on_delete = models.CASCADE)
    dish_title = models.CharField(max_length = 300, blank = True, null = True)
    type_1 = models.CharField(max_length = 500, blank = True, null = True)
    price_1 =  models.IntegerField(blank = True, null = True)
    type_2 = models.CharField(max_length = 500, blank = True, null = True)
    price_2 =  models.IntegerField(blank = True, null = True)
    type_3 = models.CharField(max_length = 500, blank = True, null = True)
    price_3 =  models.IntegerField(blank = True, null = True)
    type_4 = models.CharField(max_length = 500, blank = True, null = True)
    price_4 =  models.IntegerField(blank = True, null = True)

    def __str__(self):
        return(f'{self.section} + {self.dish_title} + {self.type_1} + {self.price_1}')
