import random, sys, os, string, argparse


class shuf:
    def __init__(self, filename, args):
        self.args = args
        if filename is None or filename == '-':
            print("Defaulting to standard input")
            self.lines = sys.stdin.readlines()
        elif type(filename) == list:
            self.lines = filename
        else:
            with open(filename, 'r') as f:
                self.lines = f.readlines()

    def print_shuffle(self):
        random.shuffle(self.lines)
        num_lines = len(self.lines)

        if self.args.repeat and self.args.head_count is None:
            while True:
                sys.stdout.write(random.choice(self.lines))

        if self.args.head_count is not None:
            if self.args.head_count < len(self.lines):
                num_lines = self.args.head_count              
            if self.args.repeat:
                for i in range(self.args.head_count):
                    sys.stdout.write(random.choice(self.lines))
                return    

        for line in self.lines[:num_lines]:
            print(line, end='')
    



def main():
    # Parser for file name
    parser = argparse.ArgumentParser(description='Randomly permute lines of a file')
    parser.add_argument('filename', nargs='*',help='input lines or a filename')

    # Parser for flags
    parser.add_argument('-n', '--head-count', type=int, help='output at most COUNT lines')
    parser.add_argument('-r', '--repeat', action='store_true', help='allow output lines to be repeated')
    parser.add_argument('-e', '--echo', action='store_true', help='treat each ARG as an input line')
    parser.add_argument('-i', '--input-range', help='treat each number LO-HI as an input line')
    args = parser.parse_args() 

    new_input = []

    if args.echo:
        if args.input_range:
            parser.error("cannot combine -e and -i options")
        new_input = [arg + '\n' for arg in args.filename]
        s = shuf(new_input, args)
        s.print_shuffle()

    elif args.input_range:
        try:
            range_ = args.input_range.split('-')
            if len(range_) != 2:
                raise ValueError
            
            low = int(range_[0])
            high = int(range_[1])

            if low > high:
                parser.error("invalid range given: '{args.input_range}'")

            new_input=[str(i) + '\n' for i in range(low, high + 1)]
            s = shuf(new_input, args)
            s.print_shuffle()


        except ValueError:
            parser.error("invalid range given: '{args.input_range}'")

    else:
        s = shuf(args.filename[0], args)
        s.print_shuffle()


if __name__ == "__main__":
    main()