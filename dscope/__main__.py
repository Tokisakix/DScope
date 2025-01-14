import argparse

from . import __version__

def main():
    parser = argparse.ArgumentParser(description="DScope CLI")
    parser.add_argument(
        "--version",
        action="version",
        version=f"DScope v{__version__}",
        help="Show the version and exit.",
    )
    args = parser.parse_args()
    return

if __name__ == "__main__":
    main()