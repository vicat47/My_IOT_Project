import write_excel

f = open('ac_data', 'r')
fw = open('data.txt', 'a')

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


for index in range(len(res)):
    if index != 0 and index % 8 == 0:
        fw.write('\r')
    fw.write(str(res[index]))
    fw.write(' ')
fw.write('\r')
print(res)