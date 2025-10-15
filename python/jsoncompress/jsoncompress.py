import json

with open('jsoncompress.json', 'r', encoding='utf-8') as f:
    obj = json.load(f)

compressed = json.dumps(obj, ensure_ascii=False, separators=(',', ':'))
print(compressed)