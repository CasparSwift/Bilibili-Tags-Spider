with open('output_all.txt','a') as f:
    cnt = 0
    useful_cnt = 0
    for i in range(0,10):
        with open('output{}.txt'.format(i),'r') as file:
            lines = file.readlines()
            for line in lines:
                if line[0] == 'N' or line[0] == 'U': continue
                cnt += 1
                try:
                    d = eval(line)
                    if int(d['atten']) >= 10 and int(d['use']) >= 3:
                        useful_cnt += 1
                        f.write(line)
                except SyntaxError:
                    print(line,end='')
        f.write('\n')
    print(cnt)
    print(useful_cnt)
