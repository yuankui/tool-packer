import json
import sys
import base64

file_dict_json = """{JSON_CONTENT}"""

file_dict = json.loads(file_dict_json)

args = sys.argv
if len(args) <= 1:
    print """sub commands"""
    commands = map(lambda x: " " * 4 + x, file_dict.keys())
    print "\n".join(commands)

sub_cmd_base64 = file_dict.get(args[1])
sub_cmd = base64.decodestring(sub_cmd_base64)

sys.argv = sys.argv[1:]
exec(sub_cmd, {}, {})