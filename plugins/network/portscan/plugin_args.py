import argparse
import sys
from api import plugin
import ui.output


def help_format_network_scan(prog):
    kwargs = {'width': ui.output.columns(), 'max_help_position': 34}
    return argparse.HelpFormatter(prog, **kwargs)


def parse(args):
    parser = argparse.ArgumentParser(prog="scan", add_help=False, usage=argparse.SUPPRESS)
    parser.formatter_class = help_format_network_scan
    parser.add_argument('-p', '--port',
                        metavar="<PORT>", default='20-10000')
    parser.add_argument('-t', '--timeout', type=float,
                        metavar="<TIMEOUT>", default=0.2)
    parser.add_argument('address')
    options = vars(parser.parse_args(args))
    options['port'] = parse_port(options['port'])

    return options

def parse_port(input):
    data = input.split('-') if input.count('-') == 1 else [input, input]
    try:
        data = [int(x) for x in data]
    except:
        sys.exit("Illegal port specifications")

    if min(data) < 0 or max(data) > 65535:
        sys.exit("Ports specified must be between 0 and 65535 inclusive")
    if data[0] > data[1]:
        sys.exit("Your port range %d-%d is backwards. Did you mean %d-%d?"
                 % (data[0], data[1], data[1], data[0]))

    return data
