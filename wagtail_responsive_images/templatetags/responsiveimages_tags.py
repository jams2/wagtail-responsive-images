from django import template


def compile_pset(parser, token):
    try:
        tag_name, image, specs, *rest = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError(
            "pset expected `{% pset IMAGE SPECS [attrs*] [as VARNAME] %}`",
        )
