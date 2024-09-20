from . import vendorize_directory, vendorize_requirement

import argparse


def main():
    parser = argparse.ArgumentParser(prog="python-vendorize")
    parser.add_argument("path", default=".", nargs="?")
    parser.add_argument("--requirement")
    parser.add_argument("--target_directory")
    parser.add_argument("--upgrade", "-U", action="store_true")
    args = parser.parse_args()

    if args.requirement is None and args.target_directory is None:
        vendorize_directory(args.path, args.upgrade)
    else:
        vendorize_requirement(
            cwd=".",
            requirement=args.requirement,
            target_directory=args.target_directory,
            upgrade=args.upgrade
        )


if __name__ == "__main__":
    main()
