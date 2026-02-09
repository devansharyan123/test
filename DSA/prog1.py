class Node:
    def __init__(self, val):
        self.val = val
        self.next = None

def delete_middle(head):
    if not head or not head.next:
        return None

    count = 0
    temp = head
    while temp:
        count += 1
        temp = temp.next

    mid = count // 2


    temp = head
    for _ in range(mid - 1):
        temp = temp.next

    temp.next = temp.next.next

    return head



n = int(input())
values = list(map(int, input().split()))

head = Node(values[0])
curr = head

for val in values[1:]:
    curr.next = Node(val)
    curr = curr.next

head = delete_middle(head)


curr = head
while curr:
    print(curr.val, end=" ")
    curr = curr.next
