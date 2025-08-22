import argparse

parser = argparse.ArgumentParser(
    description="Read a TDMS file and print its contents.",
)
parser.add_argument("file", type=str, nargs="+", help="Path to the TDMS file to read.")
