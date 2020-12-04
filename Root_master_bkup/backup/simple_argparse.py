import argparse
import pdb

def main():
    # pdb.set_trace()
    try:
        breakpoint()
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "-a1",
            "--arg-n1",
            help="Argument-1. Format YYYY-MM-DD. Defaults to the current date.",
            type=str,
            default='CSV'
        )
        parser.add_argument(
            "-a2",
            "--arg-n2",
            help="Argument-2. Number of days to emit.",
            type=str,
            default='TXT'
        )
        parser.add_argument(
            "-a3",
            "--arg-n3",
            help="Argument-3. Log bucket name",
            type=str
        )
        parser.add_argument(
            "-a4",
            "--arg-n4",
            type=int,
            default=1)

        breakpoint()
        args = parser.parse_args()
    #print (args)
        if args.arg_n1:
            print ("Received: Arg 1")
        if args.arg_n2:
            print ("Received: Arg 2")
        if args.arg_n3:
            print ("Received: Arg 3")
        if args.arg_n4:
            print ("Received: Arg 4")
    except Exception:
        print ("Invalid arguments in the command prompt.")


main()
