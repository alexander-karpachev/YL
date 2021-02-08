def reversed_linked_list(head):
    if not head or not head.next:
        return
    curr, head.next = head.next, None
    while curr:
        head, head.next, curr = curr, head, curr.next
    return head


class LinkedList:
    def __init__(self, value):
        self.value = value
        self.next = None

    def add(self, value):
        curr = self
        while curr.next:
            curr = curr.next
        curr.next = LinkedList(value)

    def getlist(self):
        curr = self
        s = []
        s1 = []
        while curr:
            s.append(curr.value)
            s.append(id(curr))
            curr = curr.next
        s.append(None)
        return s


a = LinkedList(1)
a.add(2)
a.add(3)
a.add(4)
a.add(5)

print(id(a))
a = reversed_linked_list(a)

print('---------------------------------')
print(id(a))
print(a.getlist())

