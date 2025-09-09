import logging

# Create a new logger with the name of the current module.
logger = logging.getLogger(__name__)

def main():
    # Define the log format, see below.
    log_format = "%(asctime)s - %(levelname)s - %(name)s - %(message)s"

    # Create a new logger configuration.
    logging.basicConfig(filename="program.log", 
        level=logging.DEBUG, format=log_format)

    # Change some settings for the logger of other modules.
    logging.getLogger("json").setLevel(logging.WARNING)
    logging.getLogger("numpy").setLevel(logging.ERROR)

    # Log a simple message.
    logger.info("Starting the application")

    # Log a message with some data.
    position: tuple = (34.56, 79.11)
    logger.debug(f"The point it located at: {position=}")

if __name__ == "__main__":
    main()

