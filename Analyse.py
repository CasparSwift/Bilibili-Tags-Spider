from operator import itemgetter
with open('output_all.txt','r') as file:
    lines = file.readlines()
    rows = []
    for line in lines:
        try:
            d = eval(line)
            d['total'] = int(d['atten'])+int(d['use'])
            rows.append(d)
        except SyntaxError:
            #print(line)
            pass
    rows_by_total = sorted(rows, key=itemgetter('total'),reverse=True)
    for i,dic in enumerate(rows_by_total):
        print(dic['tag_name'],end=' ')