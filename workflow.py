import aiohttp
import sendgrid
from sendgrid.helpers.mail import Mail
from temporalio import workflow, activity
from datetime import timedelta

@activity.defn
async def fetch_data_from_api(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            response.raise_for_status()
            return await response.json()

@activity.defn
async def store_data_in_db(data):
    from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData
    engine = create_engine('sqlite:///temporal_poc.db')
    metadata = MetaData()
    data_table = Table('data', metadata,
                       Column('id', Integer, primary_key=True),
                       Column('content', String))
    metadata.create_all(engine)
    conn = engine.connect()
    ins = data_table.insert().values(content=str(data))
    conn.execute(ins)
    conn.close()

@activity.defn
async def send_email(data, to_email):
    sg = sendgrid.SendGridAPIClient(api_key='YOUR_SENDGRID_API_KEY')
    email = Mail(
        from_email='your_email@example.com',
        to_emails=to_email,
        subject='Fetched Data',
        html_content=f"<p>{data}</p>")
    response = sg.send(email)
    return response.status_code

@workflow.defn
class FetchStoreSendWorkflow:
    @workflow.run
    async def run(self, url, to_email):
        data = await workflow.execute_activity(fetch_data_from_api, url, start_to_close_timeout=timedelta(seconds=10))
        await workflow.execute_activity(store_data_in_db, data, start_to_close_timeout=timedelta(seconds=10))
        await workflow.execute_activity(send_email, data, to_email, start_to_close_timeout=timedelta(seconds=10))
        return data