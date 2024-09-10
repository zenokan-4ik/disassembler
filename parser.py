res = []

def init():
    with open('data.txt', 'r') as file:
        data = file.readlines()
    res = []
    for n in data:
        temp = n[1:].split()
        temp = temp[2:-1]

        for el in temp:
            a, b = el[:2], el[2:]
            temp[temp.index(el)] = b+a

        for el in range(len(temp)):
            if temp[el][:3] == '940':
                temp[el] += temp[el+1]
                temp[el+1] = ''
        while temp.count('') != 0:
            del temp[temp.index('')]

        for elem in range(len(temp)):
            temp[elem] = bin(int(temp[elem], 16))[2:]
        res.append(temp)

        print(temp)

    with open('output.txt', 'r+') as file:
        for i in res:
            file.write(' '.join(i)+'\n')

init()