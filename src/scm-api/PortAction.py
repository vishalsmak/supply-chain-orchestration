import argparse

class PortAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        if not 0 < values < 2**16:
            raise argparse.ArgumentError(self, "port numbers must be between 0 and 2**16")
        setattr(namespace, self.dest, values)
    
    def Add_Port_Param(parser : argparse.ArgumentParser, param_name : str, help_text : str):
        parser.add_argument(f'-{param_name}',
                        help=help_text,
                        dest=param_name,
                        type=int,
                        default=5000,
                        action=PortAction,
                        metavar="{0..65535}")
        return parser