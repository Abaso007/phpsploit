import argparse
import ui.output

def help_format_proclist(prog):
    kwargs = {'width': ui.output.columns(), 'max_help_position': 34}
    return argparse.HelpFormatter(prog, **kwargs)

def parse(args):
    parser = argparse.ArgumentParser(prog="scan", add_help=False, usage=argparse.SUPPRESS)
    return vars(parser.parse_args(args))

