import re
import json
with open('output0.txt','r') as f:
    text = f.read()
    lists = text.split('\n')
    #print(lists)
    new_lists = []
    for tag in lists:
        #tag = "{'tag_name': '再给我两分钟', 'tag_id': 100101, 'use': 2, 'atten': 0}"
        tag=tag.replace('\n','')
        if tag != 'UnicodeEncodeError!':
            #print(tag)
            try:
                results = re.search("{'tag_name':\s'(.*?)',", tag,re.S)
                tag_name = results.group(1)
                results = re.search("'tag_id':\s(.*?),",tag,re.S)
                tag_id = results.group(1)
                results = re.search("'atten':\s(.*?)}",tag,re.S)
                atten = results.group(1)
                results =re.search("'use':\s(.*?),",tag,re.S)
                use = results.group(1)
                new_d = {
                    'tag_id': int(tag_id),
                    'tag_name': tag_name,
                    'atten': int(atten),
                    'use': int(use)
                }
                new_lists.append(str(new_d))
            except AttributeError:
                print(tag)
                new_lists.append(tag)
        else: new_lists.append(tag)
    with open('output2.txt', 'a') as file:
        for tag in new_lists:
            try:
                file.write(tag)
                file.write('\n')
            except UnicodeEncodeError:
                print('UnicodeEncodeError!')
                file.write('UnicodeEncodeError!\n')

