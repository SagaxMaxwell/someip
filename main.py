from dotenv import load_dotenv


from core.constructor import Constructor


if __name__ == "__main__":
    load_dotenv(override=True)
    builder = Constructor()
    builder.build_environment()
    builder.build_part()
    builder.build_allocator()
    builder.build__transceiver()
    builder.build_tester()
