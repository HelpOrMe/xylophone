from xylophone import *


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Random sentence generator.", add_help=False)
    parser.add_argument("--run", "-r", default='words-dict | structure | translate --to "chinese (traditional)" | '
                                               'translate --to en', help="Run custom xylophone!")
    parser.add_argument("--stage", "-s", action="store_true", help="Execute specific stage.")
    parser.add_argument("--help", "-h", action="store_true", help="Print this message or xylophone stage help such as "
                                                                  "'xylophone -h words-dict'.")
    parser.add_argument("--list", "-l", action="store_true", help="List all available xylophone stages.")

    args, unknown_args = parser.parse_known_args()

    if args.stage:
        stage = create_stage(unknown_args[0], unknown_args[1:])
        output = "\n".join(stage.process())
        print(output)

    elif args.help:
        if len(unknown_args) > 0 and stage_exists(unknown_args[0]):
            print(get_stage_help(unknown_args[0]))
        else:
            parser.print_help()

    elif args.list:
        print(', '.join(STAGES.keys()))

    else:
        print(run_xylophone(args.run, unknown_args)[0])


if __name__ == "__main__":
    main()
