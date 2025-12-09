from rest_framework import serializers
from django.apps import apps
from datetime import timedelta
from .models import BookingTime

class BookingTimeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = apps.get_model('fundraisers.BookingTime')
        fields = '__all__'
        read_only_fields = ['end_time']
#Auto-set end time
    def validate(self, data):
        fundraiser = data.get('fundraiser', getattr(self.instance, 'fundraiser', None))
        start = data.get('start_time', getattr(self.instance, 'start_time', None))
    
        if start and fundraiser:
            session_length = fundraiser.session_length
            auto_end = start + timedelta(minutes= session_length)
            data['end_time'] = auto_end
            end = auto_end
        else:
            end = getattr(self.instance, 'end_time', None)

#Prevent overlaps
        if start and end:
            qs = BookingTime.objects.filter(fundraiser=fundraiser)
            if self.instance:
                qs = qs.exclude(id=self.instance.id)
            overlap_exist = qs.filter(
                start_time__lt=end,
                end_time__gt=start
            ).exists()
            if overlap_exist:
                raise serializers.ValidationError("This slot overlaps with an existing booking")
        return data

#can't modify booked slot

    def update(self, instance, validated_data):
        if instance.pledges.exists():
            raise serializers.ValidationError("This slot already has a booking and cannot be changed")
        return super().update(instance, validated_data)

class PledgeSerializer(serializers.ModelSerializer):
    mentee = serializers.ReadOnlyField(source='mentee.id')
    class Meta:
        model = apps.get_model('fundraisers.Pledge')
        fields ='__all__'

    def update(self, instance, validated_data):
        instance.slot = validated_data.get('slot', instance.slot)
        instance.notes = validated_data.get('notes', instance.notes)
        instance.fundraiser = validated_data.get('fundraiser',instance.fundraiser)
        instance.save()
        return instance

class FundraiserSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.id')
    class Meta:
        model = apps.get_model('fundraisers.Fundraiser')
        fields = '__all__'

class FundraiserDetailSerializer(FundraiserSerializer):
    pledges = PledgeSerializer(many=True, read_only=True)
    booking_time = BookingTimeSerializer(many=True, read_only=True)

    def update(self, instance, validated_data):
        instance.category = validated_data.get('category', instance.category)
        instance.title = validated_data.get('title', instance.title)
        instance.background = validated_data.get('background', instance.background)
        instance.years_experience = validated_data.get('years_experience', instance.years_experience)
        instance.profile_url = validated_data.get('profile_url', instance.profile_url)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.session_length = validated_data.get('session_length', instance.session_length)
        instance.date_created = validated_data.get('date_created', instance.date_created)
        instance.save()
        return instance


