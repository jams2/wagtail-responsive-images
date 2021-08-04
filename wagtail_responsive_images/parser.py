from .image_spec import ImageSpec
from lark import Lark, Transformer
from lark.visitors import Visitor_Recursive

grammar = """
specs: spec | wrapped_spec+
wrapped_spec: "@" breakpoint "(" spec ")"
breakpoint: /(default|fallback|[2-9]?[a-z]{2})/

spec: op filters?
op: op_name | op_name "-" parameter ("-" crop_intensity)?
op_name: WORD
parameter: SIZE | INT | DECIMAL
crop_intensity: CROP_INTENSITY

filters: ("|" FILTER)+

SIZE: /[1-9][0-9]*x[1-9][0-9]*/
FILTER: /[a-z]+(-([a-z]+|[1-9][0-9]*))*/
WORD: /[a-z]+/
CROP_INTENSITY: /c(100|[1-9][0-9]|[1-9])/
INT: /[1-9][0-9]*/
DECIMAL: _DIGIT+ "." _DIGIT+
_DIGIT: /[0-9]/
FIELD_SEPARATOR: ","
%ignore FIELD_SEPARATOR

"""


class TreeToImageSpecs(Transformer):
    def filters(self, tree):
        return f"|{'|'.join(x.value for x in tree)}"

    def breakpoint(self, tokens):
        return tokens[0].value

    def parameter(self, tokens):
        return tokens[0].value

    def op_name(self, tokens):
        return tokens[0].value

    def op(self, tree):
        # breakpoint()
        return "-".join(tree)

    def crop_intensity(self, tokens):
        return tokens[0].value

    def wrapped_spec(self, tree):
        return (tree[0], "".join(tree[1]))

    def spec(self, tree):
        return "".join(tree)

    def specs(self, arg_lists):
        if len(arg_lists) == 1 and isinstance(arg_lists[0], str):
            # One spec without a breakpoint, mark it as default.
            return [ImageSpec("default", arg_lists[0])]
        return [ImageSpec(*arg_list) for arg_list in arg_lists]


class ImageSpecGenerator(TreeToImageSpecs):
    def specs(self, arg_lists):
        return (ImageSpec(*arg_list) for arg_list in arg_lists)


class CustomVisitor(Visitor_Recursive):
    def crop_intensity(self, tokens):
        return tokens[0].value

    def parameter(self, tokens):
        return tokens[0].value

    def op_name(self, tokens):
        return tokens[0].value

    def filters(self, tokens):
        return f"|{'|'.join(token for token in tokens)}"

    def op(self, tokens):
        return "-".join(tokens)


parser = Lark(grammar, start="specs", parser="lalr", transformer=TreeToImageSpecs())
# parser = Lark(grammar, start="specs", parser="lalr", transformer=CustomVisitor())
