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
        return [0, 0]
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

    return min([acc_ll, acc_lr])


for i in range(len(blocks)):
    for r in reqs:
        print(r, dist(blocks, 1, r))

