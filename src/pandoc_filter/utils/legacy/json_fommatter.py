import sys 
import json

with open('hexo_footnote_test_pandoce.json', 'r', encoding='utf-8') as json_file:
    data = json.load(json_file)

with open('formatted_output.json', 'w', encoding='utf-8') as formatted_file:
    json.dump(data, formatted_file, indent=4, ensure_ascii=False)