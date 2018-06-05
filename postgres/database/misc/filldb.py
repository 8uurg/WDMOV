"""
This script was used to generate the initial schemas automatically.
"""

import pandas as pd
import sqlalchemy as sa
import os

server = "postgres://postgres:@db:5432"
filedir = "../../data"
files = ['routes.txt', 'stop_times.txt', 'stops.txt', 'trips.txt'] # ['agency', 'calendar_dates', 'feed_info', 'shapes']

engine = sa.create_engine(server) # Changes may have to be made
conn = engine.connect()

for file in files:
    path = os.path.join(filedir, file)
    filedf = pd.read_csv(path)
    filedf.to_sql(file.split(".")[0], conn)

conn.close()