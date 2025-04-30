import imghdr

from django.core.exceptions import ValidationError
from django.core.validators import validate_image_file_extension
from rest_framework import viewsets, status
from rest_framework.response import Response

from .models import Image, OrderForms
from .pagination import CustomPagination
from .serializers import OrderFormsSerializer


def get_client_ip(request):
    """Get client IP address from request"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def validate_image_format(image_file):
    """
    Validate that the file is actually a valid image
    Returns (is_valid, error_message)
    """
    if not image_file:
        return False, "No image file provided."

    if not image_file.content_type.startswith('image/'):
        return False, "File must be an image."

    try:

        validate_image_file_extension(image_file)

        image_type = imghdr.what(image_file)
        if not image_type:
            return False, "File does not contain valid image data."

        allowed_formats = ['jpeg', 'jpg', 'png', 'gif', 'bmp', 'webp']
        if image_type not in allowed_formats:
            return False, f"Image format '{image_type}' is not supported. Allowed formats: {', '.join(allowed_formats)}"

        if hasattr(image_file, 'seek'):
            image_file.seek(0)

        return True, None

    except ValidationError as e:
        return False, f"Invalid image file: {str(e)}"
    except Exception as e:
        return False, f"Error validating image: {str(e)}"


class ImageViewSet(viewsets.ModelViewSet):
    """
    API endpoint for handling images
    """
    queryset = Image.objects.all()
    pagination_class = CustomPagination

    def list(self, request, *args, **kwargs):
        """
        List only approved images for regular users.
        Admins can see all images or filter by approval status.
        """
        queryset = self.queryset.filter(approved=True)

        serializer = self.get_serializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """
        Create a new image with IP check (one image per IP)
        """

        ip_address = get_client_ip(request)

        if Image.objects.filter(ip_address=ip_address).exists():
            return Response(
                {'detail': 'You have already uploaded an image. Only one image per IP address is allowed.'},
                status=status.HTTP_403_FORBIDDEN
            )

        if 'image' not in request.FILES:
            return Response(
                {'detail': 'No image file provided.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        image_file = request.FILES['image']

        if image_file.size > 5 * 1024 * 1024:
            return Response(
                {'detail': 'Image file size must be under 5MB.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        is_valid, error_message = validate_image_format(image_file)
        if not is_valid:
            return Response(
                {'detail': error_message},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(
                ip_address=ip_address,
                original_filename=image_file.name
            )
            return Response(
                {
                    'detail': 'Image uploaded successfully! It will be visible after approval.',
                    'data': serializer.data
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderFormsViewSet(viewsets.ModelViewSet):
    """
    API endpoint for order forms
    """
    queryset = OrderForms.objects.all().order_by('-created_at')
    serializer_class = OrderFormsSerializer

    def create(self, request, *args, **kwargs):
        """
        Create a new order form from POST data
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Order form submitted successfully',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
