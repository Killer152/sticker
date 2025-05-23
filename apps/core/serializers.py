from rest_framework import serializers

from .models import Image, OrderForms


class ImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Image
        fields = ['id', 'upload_date', 'approved', 'image_url', 'image']
        read_only_fields = ['ip_address', 'upload_date', 'approved']

    def get_image_url(self, obj):
        request = self.context.get('request')
        if request and obj.image:
            return request.build_absolute_uri(obj.image.url)
        return None


class OrderFormsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderForms
        fields = ['id', 'name', 'phone', 'contact_method', 'created_at']
        read_only_fields = ['id', 'created_at']

    def validate_phone(self, value):
        """
        Remove all non-digit characters and validate phone number
        """

        digits_only = ''.join(filter(str.isdigit, value))

        if len(digits_only) < 13:
            raise serializers.ValidationError("Phone number must have at least 13 digits")

        return digits_only
