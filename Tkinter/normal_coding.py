blocks = [
    {
        'gym': False,
        'school': True,
        'store': False
    },
    {
        'gym': True,
        'school': False,
        'store': False
    },
    {
        'gym': True,
        'school': True,
        'store': False
    },
    {
        'gym': False,
        'school': True,
        'store': False
    },
    {
        'gym': False,
        'school': True,
        'store': True
    }
]

reqs = ['gym', 'school', 'store']


def search(blocks, reqs, index, step, acc=0):
    # check if index is valid
    if index < 0 or index > len(blocks)-1 or len(reqs) == 0:
        print(f'Stopped index={index}')
        return 0
    print(f'Continue on index={index}, req={reqs}, acc={acc}')

    # check is some of reqs in block
    new_reqs = []
    for i in reqs:
        if not blocks[index].get(i):
            new_reqs.append(i)
        else:
            acc += 1

    if len(new_reqs) == 0:
        return acc
    r = search(blocks, new_reqs, index+step, 1, acc)
    return r


d = []
for i in range(len(blocks)):
    print(f'----------------> block == {i}')
    x = search(blocks, reqs, 0, 1) + search(blocks, reqs, -1, 1)
    print(f'----------------> block == {i}, acc={x}')
    d.append(x)

print(d)
