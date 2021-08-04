from .parser import parser


def test_successful_parse():
    specs = [
        (
            "@sm(width-640),@md(width-768),@lg(width-1024),@xl(width-1280),"
            "@default(width-1536),@fallback(width-1280)"
        ),
        "fill-800x800|format-webp",
        (
            "@sm(width-640|format-png),@md(width-768),@lg(width-1024),@xl(width-1280),"
            "@default(width-1536),@fallback(width-1280)"
        ),
        "fill-800x800|format-webp|background-ffffff",
        "fill-800x800-c75",
        "fill-800x800-c75|format-webp|format-png",
    ]
    for spec in specs:
        parsed = parser.parse(spec)
        assert isinstance(parsed, list) and len(parsed) > 0
