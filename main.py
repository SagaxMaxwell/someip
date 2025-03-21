from dotenv import load_dotenv


from core.constructor import Constructor


def main():
    """
    Main entry point of the program.

    This function initializes and constructs various system components required for execution.
    It follows a sequential build process to ensure all dependencies are properly set up.

    Steps:
        1. Load environment variables from a `.env` file.
        2. Instantiate the `Constructor` class.
        3. Build the environment configuration.
        4. Construct system components, including:
           - Part: Configures system parts.
           - Allocator: Manages client-session allocation.
           - Transceiver: Handles network communication.
           - Logger: Sets up logging for the system.
           - Tester: Initializes the appropriate tester based on vehicle type.

    Raises:
        Exception: If any critical setup step fails, an exception may be raised.
    """
    load_dotenv(override=True)
    builder = Constructor()
    builder.build_environment()
    builder.build_part()
    builder.build_allocator()
    builder.build_transceiver()
    builder.build_logger()
    builder.build_tester()


if __name__ == "__main__":
    main()
