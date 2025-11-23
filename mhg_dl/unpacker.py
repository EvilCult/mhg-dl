import re
import json
import lzstring

def unpack(js_str: str) -> dict[str, any] | None:
    match = re.search(r'return p;}\(\'(.*?)\',(\d+),(\d+),\'(.*?)\'\[', js_str)
    if match:
        p = match.group(1)
        a = int(match.group(2))
        c = int(match.group(3))
        k = match.group(4)
        unpacked_js = unpack_packed(p, a, c, k)
        return parse_json(unpacked_js)
    else:
        return None

def unpack_packed(p, a, c, k) -> str:
    decoder = lzstring.LZString()
    k = decoder.decompressFromBase64(k)
    k = k.split('|') if isinstance(k, str) else k
    def e(c_val):
        if c_val < a:
            s = ''
        else:
            s = e(c_val // a)
        rem = c_val % a
        if rem > 35:
            s += chr(rem + 29)
        else:
            s += "0123456789abcdefghijklmnopqrstuvwxyz"[rem]
        return s

    d = {}
    for i in range(c):
        d[e(i)] = k[i] if i < len(k) else e(i)

    pattern = re.compile(r'\b(\w+)\b')
    def replace(match):
        word = match.group(1)
        return d.get(word, word)

    result = pattern.sub(replace, p)
    return result

def parse_json(unpacked_js) -> dict[str, any] | None:
    match = re.search(r'\{.*\}', unpacked_js, re.DOTALL)

    if match:
        json_str = match.group(0)
        json_str = fix_illegal_json_str(json_str)
    else:
        return None

    return json.loads(json_str)

def fix_illegal_json_str(js_str: str) -> str:
    js_str = re.sub(r'(:\s*),', r': null,', js_str)

    empty_keys = re.findall(r'""\s*:', js_str)
    for i in range(len(empty_keys)):
        js_str = js_str.replace('"":', f'"e{i}":', 1)

    js_str = re.sub(r',\s*(?=[}\]])', '', js_str)

    js_str = re.sub(r'/+', '/', js_str)

    return js_str
