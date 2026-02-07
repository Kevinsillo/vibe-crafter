"""VibeCrafter - Interactive project wizard."""

import sys

from vibecrafter.infrastructure.config.dependencies import create_wizard_runner


def main() -> None:
    runner = create_wizard_runner()
    try:
        runner.execute()
    except KeyboardInterrupt:
        print("\nCancelado.")
        sys.exit(1)


if __name__ == "__main__":
    main()
