import asyncio
import os
import random
import logging
from redis.asyncio import Redis
from tenacity import retry, stop_after_attempt, wait_exponential

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Redis setup
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

# Concurrency configuration
CONCURRENCY_LIMIT = 5


async def process_item(item_id: int, redis: Redis, semaphore: asyncio.Semaphore):
    async with semaphore:
        key = f"processed:item:{item_id}"

        # Prevent duplicate processing.
        if await redis.exists(key):
            logger.info(f"Item {item_id} already processed. Skipping.")
            return

        try:
            await perform_work(item_id)
            # Update processing status.
            await redis.set(key, "done")
            logger.info(f"Item {item_id} processed successfully.")
        except Exception as e:
            logger.error(f"Failed to process item {item_id}: {e}")
            raise


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
async def perform_work(item_id: int):
    # Simulate processing time.
    delay = random.uniform(0.5, 2.0)
    await asyncio.sleep(delay)

    # Simulate failure scenario.
    if random.random() < 0.2:
        raise ValueError("Random failure simulation")

    logger.info(f"Work done for item {item_id}")


async def main():
    redis = Redis.from_url(REDIS_URL, decode_responses=True)
    semaphore = asyncio.Semaphore(CONCURRENCY_LIMIT)

    tasks = []
    # Simulate a batch of items
    for i in range(20):
        tasks.append(process_item(i, redis, semaphore))

    await asyncio.gather(*tasks)
    await redis.close()


if __name__ == "__main__":
    asyncio.run(main())
