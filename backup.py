import pandas as pd
from datetime import datetime
import config
from sqlalchemy import create_engine
engine = create_engine(config.SQLALCHEMY_DATABASE_URI)
# start = datetime.now()
sql = """SELECT * FROM public.nhs_ndata_entry n
where n.date > now() - interval '501 day'
order by n.date"""
df = pd.read_sql(sql, engine)
# print(datetime.now - start)
folder = r'\\bghdataserver\prismdata\Hospital & Enterprise PI\NHSN'
try:
    df.to_excel(folder+'\Daily Data Dump\DataDump500_test.xlsx', index=False)
except:
    df.to_excel(folder+'\Daily Data Dump\DataDump500_test_.xlsx', index=False)
