import ast
import astunparse
import ast2json

__all__ = "DetectorTransformer"


def parse_value_to_ast(value):
    """
    parse value to AST element according to value's type
    :param value: value to be parsed
    :return: AST element
    """
    if isinstance(value, bool):
        value = ast.NameConstant(value=value)
    elif isinstance(value, str):
        value = ast.Str(s=value)
    elif isinstance(value, list):
        value = ast.List(elts=[parse_value_to_ast(element)
                         for element in value], ctx=ast.Load())
    elif isinstance(value, tuple):
        value = ast.Tuple(elts=[parse_value_to_ast(element)
                          for element in value], ctx=ast.Load())
    elif isinstance(value, dict):
        keys = [parse_value_to_ast(key) for key in value.keys()]
        values = [parse_value_to_ast(value_element)
                  for value_element in value.values()]
        value = ast.Dict(keys=keys, values=values)
    elif isinstance(value, (int, float, complex)):
        value = ast.Num(n=value)
    else:
        value = ast.NameConstant(value=value)
    return value


class DetectorTransformer(ast.NodeTransformer):
    """
    traverse an AST and add or delete decorators(s)
    """

    def __init__(self, commands: list):
        """
        :param commands:
        an dict for the decorator.
        SAMPLE:
        [
            {
                'command_type' : 'delete',
                'name' : 'staticmethod',
                'paras' : {}
            },
            // which means delete @staticmethod
            {
                'command_type' : 'add',
                'name' : 'test_method',
                'paras' : {'test_arg1' : 'test1',
                           'test_arg2' : 'test2',
                           ......
                           }
            }
            // which means add @test_method(test_arg1='test1',
                                            test_arg2='test2')
        ]
        'command' above:
        a command showing the command for the detector to do.
        command = "add" => add decorator(s) for the AST
        command = "delete" => delete decorator(s) for the AST
        """
        if not isinstance(commands, list):
            raise AssertionError('commands must me type list')

        for input_command in commands:
            assert(isinstance(input_command, dict))
            if 'func' not in input_command.keys():
                raise AssertionError('command must have a func')
            if 'name' not in input_command.keys():
                raise AssertionError('command must have a name')
            if 'command_type' not in input_command.keys():
                raise AssertionError('command must have a command_type')
            elif input_command['command_type'] not in ('add', 'delete'):
                raise AssertionError('command ' + input_command['name']
                                     + ' must have a command_type'
                                     + 'within (add,delete), '
                                     + input_command['command_type']
                                     + ' found')

            if 'position' in input_command.keys():
                if not isinstance(input_command['position'], dict):
                    raise AssertionError(
                        'command %s\'s position must be a dict,' % input_command['name']
                        + ' %s found' % str(type(input_command['position'])))
                else:
                    if 'direction' not in input_command['position'].keys():
                        raise AssertionError(
                            'command %s\'s position must have a position' %
                            input_command['name'])
                    if 'location' not in input_command['position'].keys():
                        raise AssertionError(
                            'command %s\'s position must have a location' %
                            input_command['name'])
                    else:
                        if input_command['position']['direction'] not in (
                                'before', 'after'):
                            raise AssertionError(
                                'command ' +
                                input_command['name'] +
                                '\'s position must have a position' +
                                'within (before,after), ' +
                                input_command['position']['direction'] +
                                ' found')

            if 'paras' in input_command.keys():
                if not isinstance(input_command['paras'], dict):
                    raise AssertionError('command ' +
                                         input_command['name'] +
                                         '\'s paras must be a dict, ' +
                                         str(type(input_command['command_type'])) +
                                         ' found')
            else:
                input_command['paras'] = {}
                # is a blank paras
        self.commands = commands

    def visit_FunctionDef(self, node):
        for current_command in self.commands:
            if node.name != current_command['func']:
                continue
            if current_command['command_type'] == 'add':
                if not current_command['paras']:
                    decorator = ast.Name(id=current_command['name'],
                                         ctx=ast.Load())
                    # node.decorator_list.append(decorator)
                else:
                    keywords = []
                    for key, value in current_command['paras'].items():
                        value = parse_value_to_ast(value)
                        keyword = ast.keyword(arg=key, value=value)
                        keywords.append(keyword)
                    decorator = ast.Call(
                        func=ast.Name(
                            id=current_command['name'],
                            ctx=ast.Load()),
                        args=[],
                        keywords=keywords)

                if 'position' in current_command.keys():
                    print(
                        'found position in command %s' %
                        current_command['position'])
                    index = 0
                    for deco in node.decorator_list:
                        decorator_id = ""
                        if isinstance(deco, ast.Name):
                            decorator_id = deco.id
                        elif isinstance(deco, ast.Call):
                            decorator_id = deco.func.id
                        if decorator_id == current_command['position']['location']:
                            if current_command['position']['direction'] == 'after':
                                index += 1
                            break
                        else:
                            index += 1
                    node.decorator_list.insert(index, decorator)
                else:
                    # automatically insert after
                    node.decorator_list.append(decorator)
                    # print('succeed')
            else:
                # command['command_type'] == 'delete':
                for decorator in node.decorator_list:
                    if isinstance(decorator, ast.Name):
                        if decorator.id == current_command['name']:
                            node.decorator_list.remove(decorator)
                    else:
                        if decorator.func.id == current_command['name']:
                            node.decorator_list.remove(decorator)
        return node


if __name__ == '__main__':
    expr = """
\"\"\"
sample test
\"\"\"
@testing
@ceshi(ceshi1='ceshi',ceshi2=1,ceshi3=True,ceshi4={'ceshi':'ceshi','ceshi2':1,1:"ceshi3"},
ceshi5=[1,2,'ceshi'],ceshi6=(1,2),ceshi7=5.6,ceshi8=9j)
def add(arg1,arg2):
    if arg1 == 1:
        return arg1 + arg2
    else:
        return arg1
"""
    expr_ast = ast.parse(expr)
    print(ast.dump(expr_ast))

    command = [  # {'name' : 'ceshi',
        #  'command_type': 'add',
        #  'paras': {}
        #  },
        {'func': 'add',
         'name': 'ceshi1',
         'command_type': 'add',
         'paras': {'ceshi1': 'ceshi',
                   'ceshi2': 1,
                   'ceshi3': True,
                   'ceshi4': {'ceshi': "ceshi", "ceshi2": 1, 1: "ceshi3"},
                   'ceshi5': [1, 2, 'ceshi'],
                   'ceshi6':(1, 2),
                   'ceshi7':5.6,
                   'ceshi8':9j
                   }
         },
        {'func': 'add',
         'name': 'ceshi2',
         'command_type': 'delete'
         }
    ]

    transformer = DetectorTransformer(command)

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
