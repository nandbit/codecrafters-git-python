from app.executor import execute_command
from app.parser import setup_parser


def main():
    parser = setup_parser()
    args = parser.parse_args()
    print(args)

    execute_command(args)


if __name__ == "__main__":
    main()
