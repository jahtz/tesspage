def parse_arguments(arguments: list[str]) -> None:
    """
    Command line arguments handling

    Args:
        arguments (list[str]): list of arguments provided my sys.argv
    """
    if (len(arguments) > 1):
        match(arguments[1].lower()):
            case 'prepare':
                pass
            case 'train':
                pass
            case 'run':
                pass
            case _:
                # default case: help
                print_help()
    else:
        # missing arguments: help
        print_help()
    

def print_help() -> None:
    """Prints HELP page"""
    print('''
          TessPage
          Help:
          ''')
    
            
    