import requests
import telebot
import time
import datetime
from multiprocessing import *
import schedule
import numpy as np
from random import randint
import pandas as pd
import psycopg2
from pandas.plotting import table 
import seaborn as sns
import matplotlib.pyplot as plt
from telebot.types import InputMediaPhoto
from datetime import timedelta
import xlsxwriter
import pandas.util.testing as tm
from pandas.testing import assert_frame_equal
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import re
from datetime import date
import sys
import os
sys.path.insert(0, os.path.expanduser('./scripts'))
from business_models.databases import gdocs

def report_CPO():

    def conn():    

        gp_conn = psycopg2.connect(host='gpdb-pgbouncer.taxi.yandex.net',
                               port=5432,
                               database='ritchie',
                               user='xshoker',
                               password=open(os.path.expanduser('~/bot/Программы/password.txt')).read())
        return gp_conn


    sheet_id = '1_sd_IKiLy6Cw55yn60q2uLqo61wIrWWXJUYtdgB5yF0'
    
    def CPO():

        report = pd.read_sql(
            """select
       cpo.currency_code
      ,region_name
      ,round((sum(cost)
             /case count(distinct order_id) when 0 then null else count(distinct order_id) 
              end)::numeric, 2
            )                             as cpo
      ,count(distinct order_id)::int           as orders
      ,sum(cost)::int                          as courier_cost_lcy
      ,min(date)::date                          as from_date    
      ,max(date)::date                          as till_date    
    from 
      snb_eda.cpo_deconstructed_v2 cpo
    --  left join eda_ods_wms.store str         on cpo.place_id = str.store_id::bigint
    where 1=1
      and date between date_trunc('month', now()) and now()
      and component not in ('additional_compensation_manual_amount', -- рефералка, реактиваци и т.д.
                            'tips', -- чаевые курьерам
                            'additional_compensation_manual_amount_weighted'-- тоже рефералка, но в предыдущей версии
                            )
    group by 1,2
    order by 1,2""", conn()
                )

        conn().close()

        report = report.to_csv('report.csv')

        return report
    
    CPO()

    report_CPO = pd.read_csv('report.csv')
    
    return gdocs.write(dataframe=report_CPO.iloc[:,:9], table_name='CPO', sheet_id=sheet_id,
            if_not_exists='fail')

def cur_id():
    
    def conn():    

        gp_conn = psycopg2.connect(host='gpdb-pgbouncer.taxi.yandex.net',
                               port=5432,
                               database='ritchie',
                               user='xshoker',
                               password=open(os.path.expanduser('~/bot/Программы/password.txt')).read())
        return gp_conn


    sheet_id = '1_sd_IKiLy6Cw55yn60q2uLqo61wIrWWXJUYtdgB5yF0'
    
    def curs():

        cur = pd.read_sql(
            """select
      id::int as courier_id
      from eda_ods_bigfood.courier
      where pool_name = 'lavka'
      and work_status not in ('deactivated',
      'candidate')""", conn()
                )

        conn().close()

        cur = cur.to_csv('cur.csv', index = None)
        
        return cur
    
    curs()

    cur = pd.read_csv('cur.csv')

    return gdocs.write(dataframe=cur, table_name='Curs', sheet_id=sheet_id,
            if_not_exists='fail')