import logging
import asyncio
import signal
import sys

from data_collector import setup_logger

setup_logger()
logger = logging.getLogger(__name__)

async def main():
    logger.info("Starting app...")

    try:
        while True:
            print("Hello, world!", flush=True)
            await asyncio.sleep(3)
    except Exception as e:
        logger.error(f"Error occurred: {e}", exc_info=True)
    finally:
        logger.info("App complete!")

def handle_sigterm(sig, frame):
    logger.info("Received SIGTERM, shutting down...")
    sys.exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGTERM, handle_sigterm)

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Script interrupted by user.")
    except Exception as e:
        logger.critical(f"Critical error: {e}", exc_info=True)