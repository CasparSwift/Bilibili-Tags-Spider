
file = open('output500-600.txt','a')
with open('output59050yihou.txt','r') as f:
    lines = f.readlines()
    print(len(lines))
    for line in lines:
        line = line.replace('\n','')
        if line == 'No Tag' or line == 'UnicodeEncodeError!':
            pass
        else:
            data = eval(line)
            d = {
                'tag_id': data['tag_id'],
                'tag_name': data['tag_name'],
                'atten': data['atten'],
                'use': data['use']
            }
            try:
                file.write(str(d))
            except UnicodeEncodeError:
                file.write('UnicodeEncodeError!')
            file.write('\n')
file.close()