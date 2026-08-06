from app.commands import parse_command
from app.parser import setup_parser


def main():
    parser = setup_parser()
    args = parser.parse_args()

    parse_command(args)


if __name__ == "__main__":
    main()
