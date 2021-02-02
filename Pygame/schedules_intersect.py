c1 = [['9:00', '10:30'], ['12:00', '13:00'], ['16:00', '18:00']]
b1 = ['9:00', '20:00']
c2 = [['10:00', '11:30'], ['12:30', '14:30'], ['14:30', '15:00'], ['16:00', '17:00']]
b2 = ['10:00', '18:30']
time = 30


# convert list of intervals in format HH:FF to minutes
def c2m(c):
    return [d2m(i) for i in c]


# convert interval [HH:MM, HH:MM] to [minutes, minutes]
def d2m(d):
    return [t2m(d[0]), t2m(d[1])]


# convert time from HH:MM to minutes
def t2m(hhmm):
    t = list(map(int, hhmm.split(':')))
    return t[0]*60 + t[1]


# convert time from minutes to HH:MM
def m2t(minutes):
    hh = minutes // 60
    mm = minutes - hh * 60
    return f'{hh}:{mm:02}'


def m2ti(interval):
    return [m2t(interval[0]), m2t(interval[1])]


def intersect_intervals(interval1, interval2):
    if interval1[0] < interval2[0]:
        i1, i2 = interval1, interval2
    else:
        i1, i2 = interval2, interval1
    if i1[1] < i2[0]:
        return []
    return [i2[0], min(i1[1], i2[1])]


def busy2free(c, b):
    # converts 2d array to 1d and removes first and last members
    t = list()
    t.append(b[0])
    t += sum(c, [])
    t.append(b[1])
    r = list()
    for i in range(0, len(t), 2):
        if t[i] != t[i+1]:
            r.append([t[i], t[i+1]])
    return r


def free_intervals(c1, b1, c2, b2, time):
    l_c1 = c2m(c1)
    l_c2 = c2m(c2)
    l_b1 = d2m(b1)
    l_b2 = d2m(b2)

    l_c1 = busy2free(l_c1, l_b1)
    l_c2 = busy2free(l_c2, l_b2)
    r = list()
    for d1 in l_c1:
        for d2 in l_c2:
            p = intersect_intervals(d1, d2)
            if p:
                if p[1] - p[0] >= time:
                    r.append([m2t(p[0]), m2t(p[1])])
                break
    return r


r = free_intervals(c1, b1, c2, b2, time)
print(r)

