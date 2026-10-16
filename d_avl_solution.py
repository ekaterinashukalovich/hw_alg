import sys
from dataclasses import dataclass


@dataclass
class Node:
    key: int
    left: 'Node | None' = None
    right: 'Node | None' = None
    height: int = 1


def height(node: 'Node | None') -> int:
    return 0 if node is None else node.height


def update(node: Node) -> None:
    node.height = 1 + max(height(node.left), height(node.right))


def balance_factor(node: Node) -> int:
    return height(node.right) - height(node.left)


def rotate_left(a: Node) -> Node:
    b = a.right
    assert b is not None
    a.right = b.left
    b.left = a
    update(a)
    update(b)
    return b


def rotate_right(a: Node) -> Node:
    b = a.left
    assert b is not None
    a.left = b.right
    b.right = a
    update(a)
    update(b)
    return b


def rebalance(node: Node) -> Node:
    update(node)
    bal = balance_factor(node)
    if bal == 2:
        u = node.right
        assert u is not None
        if balance_factor(u) >= 0:
            return rotate_left(node)
        node.right = rotate_right(u)
        return rotate_left(node)
    if bal == -2:
        u = node.left
        assert u is not None
        if balance_factor(u) <= 0:
            return rotate_right(node)
        node.left = rotate_left(u)
        return rotate_right(node)
    return node


def avl_insert(root: 'Node | None', key: int) -> 'Node | None':
    if root is None:
        return Node(key)
    if key == root.key:
        return root
    if key < root.key:
        root.left = avl_insert(root.left, key)
    else:
        root.right = avl_insert(root.right, key)
    return rebalance(root)


def find_min(node: Node) -> Node:
    while node.left is not None:
        node = node.left
    return node


def avl_delete(root: 'Node | None', key: int) -> 'Node | None':
    if root is None:
        return None
    if key < root.key:
        root.left = avl_delete(root.left, key)
    elif key > root.key:
        root.right = avl_delete(root.right, key)
    else:
        if root.left is None:
            return root.right
        if root.right is None:
            return root.left
        succ = find_min(root.right)
        root.key = succ.key
        root.right = avl_delete(root.right, succ.key)
    return rebalance(root)


def exists(root: 'Node | None', key: int) -> bool:
    while root is not None:
        if key == root.key:
            return True
        root = root.left if key < root.key else root.right
    return False


def next_key(root: 'Node | None', x: int) -> 'int | None':
    ans = None
    while root is not None:
        if root.key >= x:
            ans = root.key
            root = root.left
        else:
            root = root.right
    return ans


def prev_key(root: 'Node | None', x: int) -> 'int | None':
    ans = None
    while root is not None:
        if root.key <= x:
            ans = root.key
            root = root.right
        else:
            root = root.left
    return ans


def preorder(root: 'Node | None') -> list[int]:
    if root is None:
        return []
    result = []
    stack = [root]
    while stack:
        node = stack.pop()
        result.append(node.key)
        if node.right is not None:
            stack.append(node.right)
        if node.left is not None:
            stack.append(node.left)
    return result


def main() -> None:
    data = sys.stdin.buffer.read().split()
    q = int(data[0])
    pos = 1
    root: 'Node | None' = None
    out: list[str] = []

    for _ in range(q):
        cmd = data[pos].decode()
        pos += 1
        if cmd == 'add':
            root = avl_insert(root, int(data[pos]))
            pos += 1
        elif cmd == 'del':
            root = avl_delete(root, int(data[pos]))
            pos += 1
        elif cmd == 'exists':
            out.append('YES' if exists(root, int(data[pos])) else 'NO')
            pos += 1
        elif cmd == 'next':
            res = next_key(root, int(data[pos]))
            out.append('None' if res is None else str(res))
            pos += 1
        elif cmd == 'prev':
            res = prev_key(root, int(data[pos]))
            out.append('None' if res is None else str(res))
            pos += 1
        elif cmd == 'root':
            out.append('Empty' if root is None else str(root.key))
        elif cmd == 'height':
            out.append(str(height(root)))
        elif cmd == 'print':
            keys = preorder(root)
            out.append(' '.join(map(str, keys)) if keys else 'Empty')

    if out:
        sys.stdout.write('\n'.join(out) + '\n')


if __name__ == '__main__':
    main()