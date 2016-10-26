import os
import sys
import json
import base64

template = '''
import json
import sys
import base64

file_dict_json = """{JSON_CONTENT}"""

file_dict = json.loads(file_dict_json)

args = sys.argv
if len(args) <= 1:
    print """sub commands"""
    commands = map(lambda x: " " * 4 + x, file_dict.keys())
    print \"\\n\".join(commands)
    sys.exit(1)

sub_cmd_base64 = file_dict.get(args[1])
sub_cmd = base64.decodestring(sub_cmd_base64)

sys.argv = sys.argv[1:]
exec(sub_cmd, {}, {})
'''


def is_python_file(path):
    if not path.endswith('.py'):
        return False
    if not os.path.isfile(path):
        return False
    return True


def encode(content):
    return base64.encodestring(content)


def decode(content):
    return base64.decodestring(content)


def read_files(py_files):
    file_dict = {}

    for py in py_files:
        content = open(py).read()
        base64_str = encode(content)
        file_dict[py[:-3]] = base64_str

    return file_dict


def usage():
    print """usage:
    packer [src_file...] target_file"""


def run(args):
    if len(args) <= 1:
        usage()
        sys.exit(1)
    files = os.listdir('.')
    target_file = open(args[-1], 'w')

    if len(args) > 2:
        files = args[1:-1]

    py_files = filter(is_python_file, files)
    file_dict = read_files(py_files)

    json_content = json.dumps(file_dict)

    target_content = template.replace('{JSON_CONTENT}', json_content.encode('string_escape'))
    target_file.write(target_content)


if __name__ == '__main__':
    run(sys.argv)
