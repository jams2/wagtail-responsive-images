import os

from functools import cache
from functools import reduce
from typing import Optional

from django import template
from django.conf import settings
from django.template.base import token_kwargs
from wagtail.images.models import Image
from wagtail.images.models import Rendition
from wagtail.images.models import SourceImageIOError

from ..apps import RESPONSIVE_IMAGES_PSET_TEMPLATE
from ..image_spec import ImageSpec
from ..parser import parser as spec_parser

register = template.Library()


@cache
def get_pset_template_str():
    return getattr(
        settings, "RESPONSIVE_IMAGES_PSET_TEMPLATE", RESPONSIVE_IMAGES_PSET_TEMPLATE
    )


@register.tag(name="pset")
def compile_picture_set(parser, token):
    output_var_name = None

    try:
        tag_name, image_expr, specs, *bits = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError(
            "pset expected `{% pset IMAGE SPECS (attr=value)* [as VARNAME] %}`",
        )

    image_expr = parser.compile_filter(image_expr)

    if len(bits) > 1 and bits[-2] == "as":
        output_var_name = bits[-1]
        bits = bits[:-2]

    attrs = token_kwargs(bits, parser)
    webp = attrs.pop("webp", False)
    image_specs = spec_parser.parse(specs)
    return PictureSetNode(
        image_expr, image_specs, output_var_name=output_var_name, attrs=attrs, webp=webp
    )


def add_webp_rendition(left: list[ImageSpec], right: ImageSpec):
    return [
        *left,
        ImageSpec(right.breakpoint, f"{right.filter_spec}|format-webp"),
        right,  # Put the webp first so the browser will prefer it
    ]


def get_renditions(
    image: Image, specs: list[ImageSpec], webp: bool = True
) -> tuple[list[tuple[ImageSpec, Rendition]], Optional[Rendition]]:
    """Returns two values:

    - a list of pairs of (ImageSpec, Rendition): the set of renditions with which to
    populate the srcset of an <img> tag, or generate the <source> tags in a <picture>
    set; and

    - a fallback Rendition: for the `src` attribute of an <img> tag, or for the <img>
    tag in a <picture> set. This *might* be None if the source image has been deleted.
    (This shouldn't happen, but may arise when e.g. running a copy of a production
    database without the associated assets)
    """

    src_specs = filter(lambda x: not x.is_fallback, specs)
    if webp:
        src_specs = reduce(add_webp_rendition, src_specs, [])
    src_specs = list(src_specs)
    renditions: list[tuple[ImageSpec, Rendition]] = []
    for spec in src_specs:
        try:
            rendition = image.get_rendition(spec.filter_spec)
            renditions.append((spec, rendition))
        except SourceImageIOError:
            continue
    try:
        fallback_rendition = image.get_rendition(
            next(filter(lambda x: x.is_fallback, specs)).filter_spec,
        )
    except (StopIteration, SourceImageIOError):
        # If a fallback wasn't specified with `fallback(...)`, just use the last spec.
        fallback_rendition = renditions[-1][1] if renditions else None

    return renditions, fallback_rendition


def get_file_extension(rendition: Rendition) -> str:
    _, ext = os.path.splitext(rendition.file.name)
    return ext[1:]


def get_mime_type(rendition: Rendition) -> str:
    extension = get_file_extension(rendition)
    if extension == "jpg" or extension == "jpeg":
        return "image/jpeg"
    return f"image/{extension}"


def pack_rendition(rendition: Rendition, spec: Optional[ImageSpec] = None) -> dict:
    packed = {"type": get_mime_type(rendition), "srcset": rendition.url}
    if spec is not None and spec.media_query is not None:
        packed.update({"media": spec.media_query})
    return packed


class PictureSetNode(template.Node):
    def __init__(
        self, image_expr, image_specs, output_var_name=None, attrs=None, webp=False
    ):
        self.image_expr = image_expr
        self.image_specs = image_specs
        self.output_var_name = output_var_name
        self.attrs = attrs or {}
        self.webp = webp

    def render(self, context):
        try:
            image: Image = self.image_expr.resolve(context)
        except template.VariableDoesNotExist:
            return ""

        renditions, fallback_rendition = get_renditions(
            image, self.image_specs, webp=self.webp
        )
        sources = [pack_rendition(rendition, spec) for spec, rendition in renditions]

        pset_context = {
            "sources": sources,
            "src": fallback_rendition.url if fallback_rendition else "",
            "attrs": self.attrs,
        }

        if self.output_var_name is not None:
            context[self.output_var_name] = pset_context
            return ""
        else:
            context.update(pset_context)
            return context.template.engine.get_template(get_pset_template_str()).render(
                context
            )
