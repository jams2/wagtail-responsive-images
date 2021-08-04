from dataclasses import dataclass
from functools import cache

from django.conf import settings

from .apps import RESPONSIVE_IMAGES_BREAKPOINTS


@cache
def get_breakpoints():
    return getattr(
        settings, "RESPONSIVE_IMAGES_BREAKPOINTS", RESPONSIVE_IMAGES_BREAKPOINTS
    )


@dataclass(frozen=True)
class ImageSpec:
    breakpoint: str
    filter_spec: str

    @property
    def is_default(self):
        return self.breakpoint == "default"

    @property
    def is_fallback(self):
        return self.breakpoint == "fallback"

    @property
    def breakpoint_value(self):
        return get_breakpoints().get(self.breakpoint)

    @property
    def media_query(self):
        if self.breakpoint_value is None:
            return None
        return f"(max-width: {self.breakpoint_value}px)"

    def get_size(self, rendition):
        if self.is_default:
            return f"{rendition.width}px"
        return f"{self.media_query} {rendition.width}px"
