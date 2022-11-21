import ast
import astunparse
import ast2json


class DecoratorTransformer(ast.NodeTransformer):
    def visit_BinOp(self, node):
        # print(node.__dict__)
        node.op = ast.BoolOp
        # print(node.__dict__)
        return node

    def visit_FunctionDef(self, node):
        for element in node.decorator_list:
            if isinstance(element, ast.Name):
                print(element.id)
                element.id = 'changed_static_method'
                print('[ast.Name]')
                print(element.id)
            elif isinstance(element, ast.Call):
                print('[ast.Call]]')
                element.func.id = "changed_call_method"
                keyword_count = 0
                for keyword in element.keywords:
                    keyword_count += 1
                    keyword.arg = 'keyword_' + str(keyword_count)
                    # keyword[i].value
        return node


if __name__ == '__main__':
    expr = """
\"\"\"
sample test
\"\"\"
@staticmethod
@ceshi(test_arg='ceshi',test_arg2='ceshi2')
def add(arg1,arg2):
    if arg1 == 1:
        return arg1 + arg2
    else:
        return arg1
"""
    expr_ast = ast.parse(expr)
    print(ast.dump(expr_ast))

    transformer = DecoratorTransformer()
    modified = transformer.visit(expr_ast)

    print("modified ast:")
    print(ast.dump(modified))

    print("modified code:")
    print(astunparse.unparse(modified))

    print("json:")
    data = ast2json.ast2json(modified)
    print(data)

    print("json2ast:")
    tree = None
    print(tree)
