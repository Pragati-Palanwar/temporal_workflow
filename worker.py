import asyncio
from temporalio import worker
from temporalio.client import Client
from workflow import FetchStoreSendWorkflow, fetch_data_from_api, store_data_in_db, send_email

async def main():
    client = await Client.connect("localhost:7233")
    async with worker.Worker(
        client,
        task_queue="my-task-queue",
        workflows=[FetchStoreSendWorkflow],
        activities=[fetch_data_from_api, store_data_in_db, send_email]
    ) as w:
        await w.run()

if __name__ == "__main__":
    asyncio.run(main())
