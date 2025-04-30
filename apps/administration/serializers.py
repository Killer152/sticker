from rest_framework import serializers

from ..core.models import Image, OrderForms


class AdminImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Image
        fields = ['id', 'image', 'ip_address',
                  'upload_date', 'approved', 'image_url']
        read_only_fields = ['id', 'image', 'ip_address', 'upload_date']

    def get_image_url(self, obj):
        request = self.context.get('request')
        if request and obj.image:
            return request.build_absolute_uri(obj.image.url)
        return None


class AdminOrderFormsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderForms
        fields = ['id', 'name', 'phone', 'contact_method', 'created_at']
        read_only_fields = ['id', 'created_at']
