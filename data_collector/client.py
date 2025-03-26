import asyncio
import logging
import backoff
import websockets.exceptions

from typing import Dict, Any, Callable, Coroutine

logger = logging.getLogger(__name__)

class Client:
    def __init__(self, response_handler: Callable[[dict], Coroutine]) -> None:
        self.response_handler = response_handler

    @backoff.on_exception(
        backoff.expo,
        (websockets.exceptions.WebSocketException, asyncio.TimeoutError),
        max_tries=3
    )
    async def request(self, data: Dict[str, Any]) -> None:
        try:
            async with websockets.connect(data['url']) as websocket:
                for message in data['init_messages']:
                    await websocket.send(message)
                
                while True:
                    try:
                        response = await websocket.recv()
                        await self.response_handler(response)
                    except websockets.exceptions.ConnectionClosed as e:
                        logger.warning(f"WebSocket closed: {e}")
                        break
                    except asyncio.TimeoutError:
                        logger.warning("Timeout error while waiting for message.")
                        break
                    except Exception as e:
                        logger.exception(f"Error while receiving message: {e}")
        except Exception as e:
            logger.exception(f"Unexpected error: {e}")