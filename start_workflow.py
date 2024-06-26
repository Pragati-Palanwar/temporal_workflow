import asyncio
from datetime import timedelta
from temporalio.client import Client
from workflow import FetchStoreSendWorkflow

async def main():
    client = await Client.connect("localhost:7233")
    api_key = "4d8d9ea88cd2c8e20afe5868e90252c4"
    city = "London"
    api_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    result = await client.start_workflow(
        FetchStoreSendWorkflow.run,
        api_url,  # Replace with your API URL
        "pragatipalanwar238@gmail.com",         # Replace with recipient email
        id="fetch-store-send-workflow",
        task_queue="my-task-queue",
        execution_timeout=timedelta(minutes=5)
    )
    print(f"Started workflow {result.workflow_id} with run ID {result.run_id}")

if __name__ == "__main__":
    asyncio.run(main())
