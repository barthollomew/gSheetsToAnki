import logging

def validate_args(args):
    """
    Validate command-line arguments.

    Args:
        args (argparse.Namespace): Parsed command-line arguments.

    Returns:
        bool: True if arguments are valid, False otherwise.
    """
    if not args.credentials or not args.sheet_name or not args.deck_name:
        logging.error("All arguments --credentials, --sheet-name, and --deck-name are required.")
        return False
    return True
