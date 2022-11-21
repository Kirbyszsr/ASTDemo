from project_analyzer.ast_decorator import DetectorTransformer
from project_analyzer.file_analyzer import FileAnalyzer
import ast
import astunparse
import settings.settings as s

__all__ = 'ProjectASTParser'


def reverse_command(function_type: str):
    return 'add' if function_type == 'delete' else 'delete'


def reverse_position(position_type: str):
    return 'after' if position_type == 'before' else 'before'


def read_lines(file_full_uri):
    file, lines = None, None
    encoding_types = ['utf-8', 'iso-8859-1']
    while True:
        for encoding_type in encoding_types:
            try:
                file = open(file_full_uri, encoding=encoding_type, mode='r')
                lines = file.readlines()
                break
            except UnicodeDecodeError:
                # for UnicodeDecodeError for utf-8
                continue
            finally:
                if file:
                    file.close()
                return lines if lines else []


def write_file(file_full_uri, new_lines):
    file = None
    try:
        file = open(file_full_uri, encoding='utf-8', mode='w')
        file.write(new_lines)
        file.close()
        return True
    finally:
        if file:
            file.close()
        return False


class ProjectASTParser:
    def __init__(self, _basic_url=None, file_command=None):
        if file_command is None:
            file_command = []
        assert(isinstance(_basic_url, str))
        assert(isinstance(file_command, list))
        for command in file_command:
            assert(isinstance(command, dict))
            assert('file' in command.keys())
            assert(isinstance(command['file'], str))
            assert('commands' in command.keys())
            assert(isinstance(command['commands'], list))
        self.basic_url = _basic_url
        self.file_command = file_command
        self.project_tree = self.analyze()
        self.result_ast = None

    def analyze(self):
        file_system = FileAnalyzer.file_analyze(root_dir=self.basic_url)
        # file_system.print_tree()
        if file_system:
            is_succeed, file_system_suffix_python = FileAnalyzer.file_suffix_analyze('py', file_system)
            if not is_succeed:
                raise AssertionError('[ProjectASTParser]file system analyze failed')
            return file_system_suffix_python
        else:
            return None

    def parse(self):
        if self.project_tree is None:
            raise AssertionError("Project Tree is None")
        for command in self.file_command:
            find_results = self.project_tree.find(command['file'])
            if find_results:
                file_full_uri = find_results.get_concrete_url(base_url='')
                lines_array = read_lines(file_full_uri)

                complete_line = ""
                for line in lines_array:
                    complete_line += line
                expr_ast = ast.parse(complete_line)

                command = command['commands']
                transformer = DetectorTransformer(command)

                modified_ast = transformer.visit(expr_ast)
                modified_code = astunparse.unparse(modified_ast)
                try:
                    write_file(file_full_uri, modified_code)
                except Exception as e:
                    print(e.__str__())
                    continue
        return

    def reverse(self):
        for command in self.file_command:
            for structure_command in command['commands']:
                structure_command['command_type'] = reverse_command(structure_command['command_type'])
        self.file_command.reverse()
        self.parse()
        for command in self.file_command:
            for structure_command in command['commands']:
                structure_command['command_type'] = reverse_command(structure_command['command_type'])
        self.file_command.reverse()


if __name__ == "__main__":
    basic_url = s.basic_url
    commands = s.commands

    file_basic_url = 'C:\\Users\\Lenovo\\Desktop\\sample_project\\sample_python_file.py'
    print(read_lines(file_basic_url))
    ProjectASTParser(basic_url, commands).parse()
    print(read_lines(file_basic_url))
    ProjectASTParser(basic_url, commands).reverse()
    print(read_lines(file_basic_url))
