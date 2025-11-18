from django.db import models

# Creating a python class definition
class Fundraiser(models.Model):
#the following are attributes telling Django what type of fields we want in our database table.
    title= models.CharField(max_length=200) #we are saying title field can have a max of 200 characters.
    description = models.TextField()
    goal= models.IntegerField() #this field should contain an integer
    image= models.URLField()
    is_open=models.BooleanField()
    data_created=models.DateTimeField(auto_now_add=True) #we are saying here that the date will automatically be set to the current date when a new record is created.

class Pledge(models.Model):
    amount= models.IntegerField()
    comment= models.CharField(max_length=200)
    anonymous = models.BooleanField()
    #This tells Django that each Pledge needs to have the ID of a Fundraiser saved in this field. The on_delete functions says, that if a Fundraiser is deleted or doesn't exist, we will also delete the pledge linked to that Fundraiser.
    fundraiser= models.ForeignKey('Fundraiser',
        on_delete=models.CASCADE,
        related_name='pledges'         
    )