from weather import fetch_forecast
from database import engine # The variable

from apscheduler.schedulers.asyncio import AsyncIOScheduler

async def run_pipeline():
    weather_df = await fetch_forecast(latitude= 47.965378, longitude= -81.873536)
    weather_df.to_sql(
        name='forecasts',      # Name of the SQL table
        con=engine,            # SQLAlchemy engine or connection
        if_exists='append',    # What to do if table exists ('fail', 'replace', or 'append')
        index=False            # Do not write the DataFrame index as a column
    )

# Instantiates object of scheduling specifically for AsyncIO
# Needs to be at module level so it doesn't get garbage collected
scheduler = AsyncIOScheduler()

async def start_scheduler():
    # Run it every hour; required 'interval'
    scheduler.add_job(run_pipeline, 'interval', hours=1)
    # Start it 
    scheduler.start()