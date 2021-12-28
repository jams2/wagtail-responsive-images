from functools import lru_cache
from typing import Union

from django.conf import settings

from .apps import RESPONSIVE_IMAGES_BREAKPOINTS


@lru_cache
def get_breakpoint_value(breakpoint_name: str) -> Union[int, None]:
    breakpoints = getattr(
        settings, "RESPONSIVE_IMAGES_BREAKPOINTS", RESPONSIVE_IMAGES_BREAKPOINTS
    )
    return breakpoints.get(breakpoint_name)


class ImageSpec:
    __slots__ = (
        "breakpoint_name",
        "filter_spec",
        "breakpoint_value",
        "media_query",
        "is_default",
        "is_fallback",
    )

    def __init__(self, breakpoint_name: str, filter_spec: str):
        self.filter_spec: str = filter_spec
        self.breakpoint_name: str = breakpoint_name
        self.breakpoint_value: Union[int, None] = get_breakpoint_value(
            self.breakpoint_name
        )
        self.media_query: Union[str, None] = self._get_media_query()
        self.is_default: bool = self.breakpoint_name == "default"
        self.is_fallback: bool = self.breakpoint_name == "fallback"

    def _get_media_query(self):
        if self.breakpoint_value is None:
            return None
        return f"(max-width: {self.breakpoint_value}px)"

    def get_size(self, rendition):
        if self.is_default:
            return f"{rendition.width}px"
        return f"{self.media_query} {rendition.width}px"
