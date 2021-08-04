import re

from dataclasses import dataclass
from typing import ClassVar


@dataclass(frozen=True)
class ImageSpec:
    breakpoint: str
    filter_spec: str
    default_specs: ClassVar[str] = (
        "sm(width-640),md(width-768),lg(width-1024),xl(width-1280),default(width-1536),"
        "fallback(width-1280)"
    )

    pattern: ClassVar[re.Pattern] = re.compile(
        r"(?P<breakpoint>(?:sm)|(?:md)|(?:lg)|(?:xl)|(?:2xl)|(?:default)|(?:fallback))"
        r"\((?P<filter_spec>[^)]+)\)",
        re.VERBOSE,
    )

    @property
    def is_default(self):
        return self.breakpoint == "default"

    @property
    def is_fallback(self):
        return self.breakpoint == "fallback"

    @property
    def breakpoint_value(self):
        return self.breakpoints.get(self.breakpoint)

    @property
    def media_query(self):
        if self.breakpoint_value is None:
            return None
        return f"(max-width: {self.breakpoint_value}px)"

    def get_size(self, rendition):
        if self.is_default:
            return f"{rendition.width}px"
        return f"{self.media_query} {rendition.width}px"

    @classmethod
    def from_string(cls, spec: str) -> "ImageSpec":
        return ImageSpec(*cls.pattern.match(spec).groups())
