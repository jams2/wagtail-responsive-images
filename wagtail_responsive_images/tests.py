import django

from django.conf import settings

from .image_spec import ImageSpec
from .parser import parser

settings.configure()
django.setup()


def test_parse_many():
    spec = (
        "@sm(width-640),@md(width-768),@lg(width-1024),@xl(width-1280),"
        "@default(width-1536),@fallback(width-1280)"
    )
    results = parser.parse(spec)
    assert len(results) == 6
    for result in results:
        assert isinstance(result, ImageSpec)


def test_single_spec_tagged_as_default():
    """If we pass a single spec to the template tag and no explicit breakpoint is
    provided it should be tagged 'default'.
    """
    spec = "fill-800x800|format-webp"
    results = parser.parse(spec)
    assert len(results) == 1
    assert results[0].breakpoint_name == "default"


def test_parse_with_multiple_parameters():
    """We should be able to parse with multiple parameters. It may not be a meaningful
    combination of filters, but Wagtail can deal with that.
    """
    spec = "fill-800x800|format-webp|background-ffffff"
    results = parser.parse(spec)
    assert isinstance(results[0], ImageSpec)


def test_fill_spec_with_crop_intensity():
    specs = ("fill-800x800-c75", "fill-800x800-c75|format-webp|format-png")
    for spec in specs:
        assert isinstance(parser.parse(spec)[0], ImageSpec)
