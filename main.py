import logging
import asyncio
import signal
import sys

from data_collector import setup_logger, Database, DATABASE_URL, DATA, Client, Handler

setup_logger()
logger = logging.getLogger(__name__)

async def main():
    logger.info("Starting app...")

    try:
        db = Database(DATABASE_URL)
        await db.create_table()

        h = Handler(db)
        client = Client(h.response_handler)
        await client.request(DATA)
    except Exception as e:
        logger.error(f"Error occurred: {e}", exc_info=True)
    finally:
        await db.close()
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