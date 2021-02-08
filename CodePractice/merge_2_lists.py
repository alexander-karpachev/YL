
# Definition for a linked-list node.
class Node(object):
    def __init__(self, val, next=None):
        self.val = val
        self.next = next

class Solution:
    @staticmethod
    def mergeTwoLists(a, b):

        a_head = a
        b_head = b
        r = Node(0)
        r_head = r
        tail = None
        while True:
            while b_head and a_head.val <= b_head.val:
                r.next, a_head = a_head, a_head.next
                r = r.next
                if not a_head:
                    tail = b_head
                    break
            while a_head and a_head.val >= b_head.val:
                r.next, b_head = b_head, b_head.next
                r = r.next
                if not b_head:
                    tail = a_head
                    break
            if tail:
                break
        while tail:
            r.next, tail = b_head, tail.next

        return r_head.next


# Test program
# 1 -> 3 ->5
a = Node(1)
a.next = Node(3)
a.next.next = Node(5)

# 2 -> 4 -> 6
b = Node(2)
b.next = Node(4)
b.next.next = Node(6)

c = Solution().mergeTwoLists(a, b)
while c:
  print(c.val)
  c = c.next
# 1 2 3 4 5 6