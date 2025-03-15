from dotenv import load_dotenv
from core.constructor import Constructor


def main():
    """
    Main entry point of the program.

    This script initializes and constructs various components required for execution.
    It loads environment variables and sequentially builds necessary modules.

    Steps:
        1. Load environment variables from a `.env` file.
        2. Instantiate the `Constructor` class.
        3. Build the environment configuration.
        4. Build system components, including Part, Allocator, Transceiver, and Tester.
    """
    load_dotenv(override=True)
    builder = Constructor()
    builder.build_environment()
    builder.build_part()
    builder.build_allocator()
    builder.build_transceiver()
    builder.build_tester()


if __name__ == "__main__":
    main()
