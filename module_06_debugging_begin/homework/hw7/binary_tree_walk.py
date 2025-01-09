"""
Помимо того чтобы логи писать, нужно их ещё и уметь читать,
иначе мы будем как в известном анекдоте, писателями, а не читателями.

Для вас мы написали простую функцию обхода binary tree по уровням.
Также в репозитории есть файл с логами, написанными этой программой.

Напишите функцию restore_tree, которая принимает на вход путь до файла с логами
    и восстанавливать исходное BinaryTree.

Функция должна возвращать корень восстановленного дерева

def restore_tree(path_to_log_file: str) -> BinaryTreeNode:
    pass

Примечание: гарантируется, что все значения, хранящиеся в бинарном дереве уникальны
"""
import itertools
import logging
import random
import re
from collections import deque
from dataclasses import dataclass
from typing import Optional

logger = logging.getLogger("tree_walk")


@dataclass
class BinaryTreeNode:
    val: int
    left: Optional["BinaryTreeNode"] = None
    right: Optional["BinaryTreeNode"] = None

    def __repr__(self):
        return f"<BinaryTreeNode[{self.val}]>"


def walk(root: BinaryTreeNode):
    queue = deque([root])

    while queue:
        node = queue.popleft()

        logger.info(f"Visiting {node!r}")

        if node.left:
            logger.debug(
                f"{node!r} left is not empty. Adding {node.left!r} to the queue"
            )
            queue.append(node.left)

        if node.right:
            logger.debug(
                f"{node!r} right is not empty. Adding {node.right!r} to the queue"
            )
            queue.append(node.right)


counter = itertools.count(random.randint(1, 10 ** 6))


def get_tree(max_depth: int, level: int = 1) -> Optional[BinaryTreeNode]:
    if max_depth == 0:
        return None

    node_left = get_tree(max_depth - 1, level=level + 1)
    node_right = get_tree(max_depth - 1, level=level + 1)
    node = BinaryTreeNode(val=next(counter), left=node_left, right=node_right)

    return node


def restore_tree(path_to_log_file: str) -> BinaryTreeNode:
    binary_tree_dict = {}
    root = None

    with open(path_to_log_file, 'r') as log_file:
        for line in log_file.readlines():
            if line.startswith('INFO'):
                node_value = int(re.search(r'[-+]?\d+', line).group())
                if not node_value in binary_tree_dict:
                    new_node = BinaryTreeNode(node_value)
                    binary_tree_dict[node_value] = new_node

                    if root is None:
                        root = new_node


            elif line.startswith('DEBUG'):

                node_value = int(re.search(r'[-+]?\d+', line).group())



                if 'left' in line:

                    left_child_value = int(re.search(r'Adding <BinaryTreeNode\[(.*?)\]>', line).group(1))

                    if left_child_value not in binary_tree_dict:
                        binary_tree_dict[left_child_value] = BinaryTreeNode(left_child_value)
                    binary_tree_dict[node_value].left = binary_tree_dict[left_child_value]


                elif 'right' in line:

                    right_child_value = int(re.search(r'Adding <BinaryTreeNode\[(.*?)\]>', line).group(1))

                    if right_child_value not in binary_tree_dict:
                        binary_tree_dict[right_child_value] = BinaryTreeNode(right_child_value)
                    binary_tree_dict[node_value].right = binary_tree_dict[right_child_value]

    return root


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(levelname)s:%(message)s",
        filename="walk_log_4.txt",
    )

    # root = get_tree(5)
    # walk(root)

    print(restore_tree('walk_log_4.txt'))

