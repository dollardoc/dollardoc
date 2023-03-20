import sys

from dollar.builder.dollarbuilder import DollarBuilder


def cli():
    args = sys.argv[1:]
    if len(args) == 0:
        print("You need to provide atleast one option")
        print()
        args = ["help"]
    main_option = args[0]
    if main_option == "help":
        print("dollardoc help")
        print("dollardoc build")
        print()
    elif main_option == "build":
        DollarBuilder.build()
