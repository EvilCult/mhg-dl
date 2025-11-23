import sys
import types
import json
from mhg_dl.unpacker import fix_illegal_json_str, parse_json, unpack

fake_lz = types.ModuleType("lzstring")
class _FakeLZObj:
    def decompressFromBase64(self, s):
        return s


fake_lz.LZString = lambda: _FakeLZObj()
sys.modules['lzstring'] = fake_lz

def test_fix_illegal_json_str_trailing_commas_and_empty_keys():
    js = '{"a":, "": 3, "b":2,}'
    fixed = fix_illegal_json_str(js)
    assert '"a": null' in fixed
    assert '"e0":' in fixed
    parsed = json.loads(fixed)
    assert parsed['a'] is None
    assert parsed['e0'] == 3
    assert parsed['b'] == 2


def test_parse_json_extracts_object_and_rewrites_empty_keys():
    js = 'var foo = {"x":1, "":2,}; var y = 1;'
    parsed = parse_json(js)
    assert isinstance(parsed, dict)
    assert parsed.get('x') == 1
    assert parsed.get('e0') == 2


def test_unpack_returns_none_for_non_packer_input():
    assert unpack("console.log('hi');") is None


def test_parse_json_returns_none_when_no_object():
    assert parse_json('no object here') is None
