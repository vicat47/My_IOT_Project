f = open('ac_data', 'r')

'''
space 8981
pulse 4505
'''

d = []
res = []
for line in f.readlines():
    r = line.split(' ')
    d.append(int(r[1]))
    if len(d) == 2:
        if(d[1] > 1000):
            res.append(1)
        else:
            res.append(0)
        d = []
    line.strip()

print(res)