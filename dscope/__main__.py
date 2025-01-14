import argparse

from . import __version__
from .simulator import (
    logical_clock_simulator,
    vector_clock_simulator,
)

simulator_lists = ["logical-clock", "vector-clock"]

def main():
    parser = argparse.ArgumentParser(description="DScope CLI")
    parser.add_argument(
        "--version",
        action="version",
        version=f"DScope v{__version__}",
        help="Show the version and exit.",
    )
    parser.add_argument(
        "--simulator",
        type=str,
        choices=simulator_lists,
        help="Run the simulator.",
    )

    args = parser.parse_args()
    assert args.simulator in simulator_lists, f"\033[91m[E] Simulator {args.simulator} not found.\033[0m"

    if args.simulator == "logical-clock":
        simulator_log = logical_clock_simulator()
    elif args.simulator == "vector-clock":
        simulator_log = vector_clock_simulator()

    print(f"\033[92m[+] {simulator_log}\033[0m")
    return

if __name__ == "__main__":
    main()