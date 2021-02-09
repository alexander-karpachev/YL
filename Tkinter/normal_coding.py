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

# Lets try calc it for one middle block for one req
# 0 1 2 3 4
# F T T F F
# 0: 1++ till T
block_id = 3
req = reqs[0]


def dist(blocks, index, req):
    if blocks[index].get(req):
        return 0
    acc_lr = 1000
    for i in range(index+1, len(blocks)):
        if blocks[i].get(req):
            acc_lr = i - index
            break

    acc_ll = 1000
    for i in range(index, -1, -1):
        if blocks[i].get(req):
            acc_ll = index - i
            break

    return min(acc_ll, acc_lr)


d = []
for r in reqs:
    print([int(not b.get(r)) for b in blocks])


min_acc = 1000
min_id = 0
for i in range(len(blocks)):
    acc = []
    print(f'BLOCK {i} ----------')
    for r in reqs:
        d.append(dist(blocks, i, r))
        #acc += d
    print('  ', reqs, d, max(d), acc)
    d.clear()

# print(min_id)