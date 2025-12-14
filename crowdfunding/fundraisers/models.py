from django.db import models
from django.contrib.auth import get_user_model


class Fundraiser(models.Model):
    category_choices = [('Finance', 'Finance'),
                        ('Tech_Digital', 'Tech & Digital'),
                        ('Health_Lifestyle', 'Health & Lifestyle'),
                        ('Career', 'Career'),('Creative_Skills','Creative Skills'),
                        ('Personal_Development','Personal Development'),('Language','Language & Cultural Exchange')]

    category = models.CharField(max_length=20, choices=category_choices)
    title= models.CharField(max_length=200)
    background = models.TextField()
    years_experience = models.IntegerField()
    profile_url = models.URLField()
    is_active=models.BooleanField(default=True)
    session_length = models.IntegerField(default=30)
    date_created=models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(
    get_user_model(),
    on_delete=models.CASCADE,
    related_name='fundraiser'
    )

class Pledge(models.Model):
    slot = models.OneToOneField('BookingTime',
        on_delete= models.CASCADE,
        related_name = 'pledges')
    fundraiser = models.ForeignKey('Fundraiser',
        on_delete=models.CASCADE,
        related_name='pledges')
    mentee = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name = 'pledges'
        
    ) 
    notes = models.TextField(blank= True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)

class BookingTime(models.Model):

    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)
    fundraiser = models.ForeignKey(
        'Fundraiser',
        on_delete=models.CASCADE,
        related_name='booking_time'
    )
    
