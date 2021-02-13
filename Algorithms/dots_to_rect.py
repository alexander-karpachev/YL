# Dynamic programming
a = [2, 4, 6, 10]
s = 6


class Const:
    ACCURACY = 6

def get_subsets(a, s):
    pass


##### all lines
# ex:
# {
#   (m, b): lambda x: m*x + b
# }

##### all parallel lines
all_lines = {}

#
parallel_lines = {}


def add_line(p1, p2, d):
    x0, y0 = p1
    x1, y1 = p2
    # using formula  y=mx+b
    m = round((y1 - y0) / (x1 - x0), Const.ACCURACY)
    b = round(y0 - m * x0, Const.ACCURACY)
    d[(m, b)] = lambda x: m * x + b
    print(f'y={m}x+{b}')


def is_parallel(line1, line2):
    return line1[0] == line2[0] and line1[1] != line2[1]


add_line((4, 7), (-3, 3), all_lines)

# divide lines into groups by parallelism
for line1 in all_lines:
    pass




