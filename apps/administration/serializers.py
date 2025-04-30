from rest_framework import serializers
from ..core.models import Image, OrderForms


class AdminImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Image
        fields = ['id', 'title', 'image', 'original_filename', 'ip_address',
                  'upload_date', 'approved', 'image_url']
        read_only_fields = ['id', 'image', 'original_filename', 'ip_address', 'upload_date']

    def get_image_url(self, obj):
        request = self.context.get('request')
        if request and obj.image:
            return request.build_absolute_uri(obj.image.url)
        return None


class AdminOrderFormsSerializer(serializers.ModelSerializer):
    contact_method_display = serializers.CharField(source='get_contact_method_display', read_only=True)

    class Meta:
        model = OrderForms
        fields = ['id', 'name', 'phone', 'contact_method', 'contact_method_display', 'created_at']
        read_only_fields = ['id', 'created_at']

