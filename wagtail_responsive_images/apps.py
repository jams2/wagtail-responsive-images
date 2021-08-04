from django.apps import AppConfig


class WagtailResponsiveImagesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "wagtail_responsive_images"


RESPONSIVE_IMAGES_BREAKPOINTS = {
    "xs": 639,  # < 640
    "sm": 767,  # < 768
    "md": 1023,  # < 1024
    "lg": 1279,  # < 1280
    "xl": 1535,  # < 1536
}

RESPONSIVE_IMAGES_PSET_TEMPLATE = "wagtail_responsive_images/picture_set.html"
