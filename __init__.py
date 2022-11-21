import settings.settings as s
from project_analyzer.project_astparser import ProjectASTParser
import argparse


def read_commands(command_uri=None):
    encoding_types = ['utf-8', 'iso-8859-1']
    file, lines = None, None
    while True:
        for encoding_type in encoding_types:
            try:
                file = open(command_uri, encoding=encoding_type, mode='r')
                lines = file.readlines()
                break
            except UnicodeDecodeError:
                # for UnicodeDecodeError for utf-8
                continue
            finally:
                if file:
                    file.close()
                return lines if lines else []


def parse_commands(command_array=None):
    if not command_array:
        command_array = []
    complete_line = ""
    for line in command_array:
        complete_line += line
    return complete_line


def get_commands(basic_url=None):
    exec_env = {}
    command_file = parse_commands(read_commands(basic_url))
    exec(command_file, exec_env)
    # print(commands['commands'])
    if exec_env and exec_env['commands']:
        print("[get_commands]read config file %s SUCCEED" % basic_url)
        return exec_env['commands']
    else:
        print("[get_commands]read config file %s FAILED" % basic_url)
        return []


def parse(basic_url=None, commands=None):
    basic_url = basic_url if basic_url else s.basic_url
    commands = s.commands if not commands else get_commands(commands)
    ProjectASTParser(basic_url, commands).parse()
    print('[Parse]%s Parse Succeed' % basic_url)


def reverse(basic_url=None, commands=None):
    basic_url = basic_url if basic_url else s.basic_url
    commands = s.commands if not commands else get_commands(commands)
    ProjectASTParser(basic_url, commands).reverse()
    print('[Reverse]%s Reverse Succeed' % basic_url)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="insert tracing detecting support")
    sub_parsers = parser.add_subparsers()

    parse_parser = sub_parsers.add_parser('parse', help="add detectors for project")
    parse_parser.add_argument('-u', type=str, help="basic_url for the project", default="")
    parse_parser.add_argument('-c', type=str, help="command_url for the project", default="")
    parse_parser.set_defaults(func=parse)

    reverse_parser = sub_parsers.add_parser('reverse', help="delete detectors for project")
    reverse_parser.add_argument('-u', type=str, help="basic_url for the project", default="")
    reverse_parser.add_argument('-c', type=str, help="command_url for the project", default="")
    reverse_parser.set_defaults(func=reverse)

    args = parser.parse_args()
    try:
        args.func(basic_url=args.u, commands=args.c)
        print('[__init__.py]Succeed')
    except AttributeError:
        arg_u = args.u if args.u else ""
        arg_c = args.c if args.c else ""
        print('[__init__.py]Failed args.u=%s args.c=%s' % (arg_u, arg_c))
        parser.print_help()
