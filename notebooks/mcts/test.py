import time
from .node import Node, mcts
from .common import Result
from . import tictactoe

# from .tictactoe import State, Command, get_command
from .connect4 import State, Command, get_command


def apply_command(root: Node, command: Command) -> Node:
    """
    Either get the child node that has this command or
    create a new root
    """

    if command in root.children:
        return root.children[command]

    else:
        # This was never explored, create a new node
        # from scratch
        return Node(root.state.apply(command))


def pick_move(root: Node, seconds: float) -> Command:
    print("Computer thinking...")
    start = time.time()

    N = 1000

    for i in range(N):
        mcts(root)

    duration = time.time() - start

    print(f"Ran {N} playouts in {duration} seconds")
    print("Best line:", root.best_line())
    return root.best()


def main() -> None:

    s = State()
    root: Node[State] = Node(s)

    print(root.state)
    print("")
    while root.state.result == Result.INPROGRESS:

        human = get_command(root.state)
        root = apply_command(root, human)
        print(root.state)
        print("")
        if root.state.result == Result.INPROGRESS:
            computer = pick_move(root, 1.5)
            root = apply_command(root, computer)
        print(root.state)
        print("")
    print(f"GAME OVER, result is {root.state.result}")
