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

# chat_id='-1001747077372'
channel_id = '-1001742418776'

def conn():    

    gp_conn = psycopg2.connect(host='gpdb-pgbouncer.taxi.yandex.net',
                           port=5432,
                           database='ritchie',
                           user='xshoker',
                           password=open(os.path.expanduser('~/bot/Программы/password.txt')).read())
    return gp_conn

def report():
    
    config = {'number_of_weeks':6}
    city_metrics_per_week = pd.read_sql(
        """
        -- Убить свои сессии, кроме текущей
        select
            pg_terminate_backend(pid)
        from
            pg_stat_activity
        where
            usename = current_user
            and pid != pg_backend_pid();

        select
            shift_distribution.region_name,
            date_trunc('week', shift_distribution.local_hour) as week,
            sum(shift_distribution.number_of_orders) as number_of_orders,
            (sum(shift_distribution.number_of_orders) - sum(shift_distribution.number_of_orders) filter(where is_market=0)) as market_orders,
            round(100*(sum(shift_distribution.number_of_orders) / nullif(sum(shift_distribution.number_of_orders_plan), 0) - 1), 1) as plan_fact_orders_mistake,
            round(sum(shift_distribution.fact_sh_total)::int, 0) as fact_sh,
            cast(100*(sum(shift_distribution.fact_sh_total) / nullif(sum(number_of_sh_forecast), 0) - 1) as INTEGER) as plan_fact_sh,
            round(cast((sum(number_of_orders) - sum(number_of_taxi_orders)
            - sum(number_of_cancelled_orders)) / nullif(sum(fact_sh_total), 0) as double precision)::numeric, 1) as oph,
            cast(sum(shift_distribution.cte_sum) / nullif(sum(shift_distribution.number_of_asap_delivered_orders), 0) as INTEGER) as cte,
            round(100*sum(shift_distribution.number_of_cancelled_orders) / nullif(sum(shift_distribution.number_of_orders), 0), 1) as cancelled,
            round(100*sum(shift_distribution.number_of_taxi_orders) / nullif(sum(shift_distribution.number_of_orders), 0), 1) as taxi_orders,
            round(100*sum(shift_distribution.number_of_surged_orders) / nullif(sum(shift_distribution.number_of_orders), 0), 1) as surged_orders,
            round(100*sum(number_of_orders_cte40) / nullif(sum(shift_distribution.number_of_asap_delivered_orders), 0), 1) as cte40_orders,
            sh_info.active_couriers,
            round(sh_info.sh_per_week::int, 0) as sh_per_week
        from
            snb_lavka.shift_final_agg shift_distribution
        left join
            (select
                s.city_name as region_name,
                date_trunc('week', shd.rep_hour_start) as week,
                sum(case
                        when ssc='wms' and shift_status_code in ('complete','leave') then (work_sec - coalesce(pause_sec,0))/3600 
                        when ssc='ctt' and shift_status_code != 'not_started'        then (work_sec - coalesce(pause_sec,0))/3600
                    else 0 end ) / count(distinct courier_id)::int as sh_per_week,
                count(distinct courier_id) as active_couriers
            from
                snb_eda.shift_sh_detail shd 
            left join eda_ods_wms.store s 
                on shd.store_id = s.store_id 
            where
                shd.rep_hour_start >= date_trunc('week', now())::DATE - interval '{number_of_weeks} week'
                and shd.rep_hour_start < date_trunc('week', now())::DATE
                and work_sec > 0 
                and city_name not in ('Тель-Авив', 'Париж', 'Лондон')
            group by
                s.city_name,
                date_trunc('week', shd.rep_hour_start)
            order by
                s.city_name,
                date_trunc('week', shd.rep_hour_start)) sh_info
                    on sh_info.region_name = shift_distribution.region_name
                        and sh_info.week = date_trunc('week', shift_distribution.local_hour)
        where
            shift_distribution.local_hour::date between date_trunc('week', current_date) - interval '{number_of_weeks} weeks' and date_trunc('day', current_date) - interval '1 day'
            and shift_distribution.region_name not in ('Тель-Авив', 'Париж', 'Лондон', 'Иркутск')
            and shift_distribution.active_zone = 'foot'
        group by
            shift_distribution.region_name,
            date_trunc('week', shift_distribution.local_hour),
            sh_info.active_couriers,
            sh_info.sh_per_week
        order by
            shift_distribution.region_name,
            date_trunc('week', shift_distribution.local_hour)
        """.format(**config), conn()
            )
    conn().close()

    city_metrics_per_day = pd.read_sql(
        """
        -- Убить свои сессии, кроме текущей
        select
            pg_terminate_backend(pid)
        from
            pg_stat_activity
        where
            usename = current_user
            and pid != pg_backend_pid();

        select
            shift_distribution.region_name,
            shift_distribution.local_hour::date as date,
            sum(shift_distribution.number_of_orders) as number_of_orders,
            (sum(shift_distribution.number_of_orders) - sum(shift_distribution.number_of_orders) filter(where is_market=0)) as market_orders,
            round(100*(sum(shift_distribution.number_of_orders) / nullif(sum(shift_distribution.number_of_orders_plan), 0) - 1), 1) as plan_fact_orders_mistake,
            round(sum(shift_distribution.fact_sh_total)::int, 0) as fact_sh,
            cast(100*(sum(shift_distribution.fact_sh_total) / nullif(sum(shift_distribution.number_of_sh_forecast), 0) - 1) as INTEGER) as plan_fact_sh,
            round(cast((sum(number_of_orders) - sum(number_of_taxi_orders)
            - sum(number_of_cancelled_orders)) / nullif(sum(fact_sh_total), 0) as double precision)::numeric, 1) as oph,
            cast(sum(shift_distribution.cte_sum) / nullif(sum(shift_distribution.number_of_asap_delivered_orders), 0) as INTEGER) as cte,
            round(100*sum(shift_distribution.number_of_cancelled_orders) / nullif(sum(shift_distribution.number_of_orders), 0), 1) as cancelled,
            round(100*sum(shift_distribution.number_of_taxi_orders) / nullif(sum(shift_distribution.number_of_orders), 0), 1) as taxi_orders,
            round(100*sum(shift_distribution.number_of_surged_orders) / nullif(sum(shift_distribution.number_of_orders), 0), 1) as surged_orders,
            round(100*sum(number_of_orders_cte40) / nullif(sum(shift_distribution.number_of_asap_delivered_orders), 0), 1) as cte40_orders,
            sh_info.active_couriers
        from
            snb_lavka.shift_final_agg shift_distribution
        left outer join
            (select
                s.city_name as region_name,
                shd.rep_hour_start::date as date,
                sum(case
                        when ssc='wms' and shift_status_code in ('complete','leave') then (work_sec - coalesce(pause_sec,0))/3600 
                        when ssc='ctt' and shift_status_code != 'not_started'        then (work_sec - coalesce(pause_sec,0))/3600
                    else 0 end ) / count(distinct courier_id)::int as sh_per_week,
                count(distinct courier_id) as active_couriers
            from
                snb_eda.shift_sh_detail shd 
            left join eda_ods_wms.store s 
                on shd.store_id = s.store_id 
            where
                shd.rep_hour_start between date_trunc('week', current_date)
                                       and date_trunc('week', current_date + interval '1 week') - interval '1 day'
                and work_sec > 0 
                and city_name not in ('Тель-Авив', 'Париж', 'Лондон')
            group by
                s.city_name,
                shd.rep_hour_start::date
            ) sh_info
                    on sh_info.region_name = shift_distribution.region_name
                        and sh_info.date = shift_distribution.local_hour::date
        where
            shift_distribution.local_hour::date between date_trunc('week', current_date)
                                              and date_trunc('week', current_date + interval '1 week') - interval '1 day'
            and shift_distribution.region_name not in ('Тель-Авив', 'Париж', 'Лондон', 'Иркутск')
            and shift_distribution.active_zone = 'foot'
            --and shift_distribution.region_name != 'Москва'
        group by
            shift_distribution.region_name,
            shift_distribution.local_hour::date,
            sh_info.active_couriers,
            sh_info.sh_per_week
        order by
            shift_distribution.region_name,
            shift_distribution.local_hour::date
        """, conn()
            )
    conn().close()
    # выгружаем за предыдущую неделю и переименовываем даты для concat'а
    city_metrics_per_day_previous_week = pd.read_sql(
        """
        -- Убить свои сессии, кроме текущей
        select
            pg_terminate_backend(pid)
        from
            pg_stat_activity
        where
            usename = current_user
            and pid != pg_backend_pid();

        select
            shift_distribution.region_name,
            shift_distribution.local_hour::date + interval '1 week' as date,
            sum(shift_distribution.number_of_orders) as number_of_orders,
            (sum(shift_distribution.number_of_orders) - sum(shift_distribution.number_of_orders) filter(where is_market=0)) as market_orders,
            round(100*(sum(shift_distribution.number_of_orders) / nullif(sum(shift_distribution.number_of_orders_plan), 0) - 1), 1) as plan_fact_orders_mistake,
            round(sum(shift_distribution.fact_sh_total)::int, 0) as fact_sh,
            cast(100*(sum(shift_distribution.fact_sh_total) / nullif(sum(shift_distribution.number_of_sh_forecast), 0) - 1) as INTEGER) as plan_fact_sh,
            round(cast((sum(number_of_orders) - sum(number_of_taxi_orders)
            - sum(number_of_cancelled_orders)) / nullif(sum(fact_sh_total), 0) as double precision)::numeric, 1) as oph,
            cast(sum(shift_distribution.cte_sum) / nullif(sum(shift_distribution.number_of_asap_delivered_orders), 0) as INTEGER) as cte,
            round(100*sum(shift_distribution.number_of_cancelled_orders) / nullif(sum(shift_distribution.number_of_orders), 0), 1) as cancelled,
            round(100*sum(shift_distribution.number_of_taxi_orders) / nullif(sum(shift_distribution.number_of_orders), 0), 1) as taxi_orders,
            round(100*sum(number_of_orders_cte40) / nullif(sum(shift_distribution.number_of_asap_delivered_orders), 0), 1) as cte40_orders,
            round(100*sum(shift_distribution.number_of_surged_orders) / nullif(sum(shift_distribution.number_of_orders), 0), 1) as surged_orders,
            sh_info.active_couriers
        from
            snb_lavka.shift_final_agg shift_distribution
        left outer join
            (select
                s.city_name as region_name,
                shd.rep_hour_start::date as date,
                sum(case
                        when ssc='wms' and shift_status_code in ('complete','leave') then (work_sec - coalesce(pause_sec,0))/3600 
                        when ssc='ctt' and shift_status_code != 'not_started'        then (work_sec - coalesce(pause_sec,0))/3600
                    else 0 end ) / count(distinct courier_id)::int as sh_per_week,
                count(distinct courier_id) as active_couriers
            from
                snb_eda.shift_sh_detail shd 
            left join eda_ods_wms.store s 
                on shd.store_id = s.store_id 
            where
                shd.rep_hour_start between date_trunc('week', current_date) - interval '1 week'
                                       and date_trunc('week', current_date) - interval '1 day'
                and work_sec > 0 
                and city_name not in ('Тель-Авив', 'Париж', 'Лондон')
            group by
                s.city_name,
                shd.rep_hour_start::date
            ) sh_info
                    on sh_info.region_name = shift_distribution.region_name
                        and sh_info.date = shift_distribution.local_hour::date
        where
            shift_distribution.local_hour::date between date_trunc('week', current_date) - interval '1 week'
                                              and date_trunc('week', current_date) - interval '1 day'
            and shift_distribution.region_name not in ('Тель-Авив', 'Париж', 'Лондон', 'Иркутск')
            and shift_distribution.active_zone = 'foot'
            --and shift_distribution.region_name = 'Москва'
        group by
            shift_distribution.region_name,
            shift_distribution.local_hour::date,
            sh_info.active_couriers,
            sh_info.sh_per_week
        order by
            shift_distribution.region_name,
            shift_distribution.local_hour::date
        """, conn()
            )
    conn().close()

    # границы выгрузки
    today = datetime.date.today()
    today_np64 = np.datetime64(today.strftime("%F"))
    days_to_week_end = 6 - datetime.date.today().weekday()
    sunday = today + datetime.timedelta(days=days_to_week_end)
    monday = today - datetime.timedelta(days=6 - days_to_week_end)

    # создание столбца со средними значениями (week)
    city_metrics_week = city_metrics_per_day[city_metrics_per_day['date'] != today_np64].copy()
    city_metrics_week = city_metrics_week.dropna()
    city_metrics_week = city_metrics_week.groupby(by='region_name').agg(
        {
            'number_of_orders': 'sum',
            'market_orders': 'sum',
            'plan_fact_orders_mistake': 'mean',
            'fact_sh': 'sum',
            'plan_fact_sh': 'mean',
            'oph': 'mean',
            'cte': 'mean',
            'cancelled': 'mean',
            'taxi_orders': 'mean',
            'surged_orders': 'mean',
            'active_couriers': 'mean',
            'cte40_orders': 'mean'
        }).reset_index()
    city_metrics_week['date'] = 'week'
    
    city_metrics_previous_week = city_metrics_per_day_previous_week.copy()
    city_metrics_previous_week = city_metrics_previous_week[city_metrics_previous_week['date'] < today_np64]
    city_metrics_previous_week = city_metrics_previous_week.dropna()
    city_metrics_previous_week = city_metrics_previous_week.groupby(by='region_name').agg(
    {
        'number_of_orders': 'sum',
        'market_orders': 'sum',
        'plan_fact_orders_mistake': 'mean',
        'fact_sh': 'sum',
        'plan_fact_sh': 'mean',
        'oph': 'mean',
        'cte': 'mean',
        'cancelled': 'mean',
        'taxi_orders': 'mean',
        'surged_orders': 'mean',
        'active_couriers': 'sum',
        'cte40_orders': 'mean'
    }).reset_index()
    city_metrics_previous_week['date'] = 'previous_week'

    # добавление сравнения метрик с предыдущей неделей (для понедельника - добавление строк в таблицу для
    # совпадения индексов с метриками предыдущей недели (без понедельника))
    city_metrics_wow = city_metrics_per_day.copy()
    if days_to_week_end == 6:
        i = 1
        while i < len(city_metrics_wow):
            line = pd.DataFrame({
                    'region_name': 'city',
                    'date': np.nan,
                    'number_of_orders': np.nan,
                    'market_orders': np.nan,
                    'plan_fact_orders_mistake': np.nan,
                    'fact_sh': np.nan,
                    'plan_fact_sh': np.nan,
                    'oph': np.nan,
                    'cte': np.nan,
                    'cancelled': np.nan,
                    'taxi_orders': np.nan,
                    'surged_orders': np.nan,
                    'cte40_orders': np.nan,
                    'active_couriers': np.nan,
                    }, index=[i + 0.5])
            city_metrics_wow = city_metrics_wow.append(line, ignore_index=False)
            city_metrics_wow = city_metrics_wow.sort_index().reset_index(drop=True)
            i += 7
    city_metrics_per_day['date'] = pd.to_datetime(
                city_metrics_per_day["date"], errors="coerce"
            ).dt.strftime("%d.%m.%y")
    columns = [
        'number_of_orders',
        'market_orders',
        'plan_fact_orders_mistake',
        'fact_sh',
        'plan_fact_sh',
        'oph',
        'cte',
        'cancelled',
        'taxi_orders',
        'surged_orders',
        'cte40_orders',
        'active_couriers',
    ]
    city_metrics_week_wow = pd.merge(city_metrics_week, city_metrics_previous_week, on='region_name')
    for item in columns:
        city_metrics_wow[item] = 100 * (city_metrics_wow[item] / city_metrics_per_day_previous_week[item] - 1)
        try:
            city_metrics_week_wow[item] = 100 * (city_metrics_week_wow[item + '_x'] / city_metrics_week_wow[item + '_y'] - 1)
        except:
            pass
    city_metrics_wow['plan_fact_orders_mistake'] = np.nan
    city_metrics_wow['plan_fact_sh'] = np.nan
    for item in columns:
        city_metrics_wow[item] = city_metrics_wow[item].map('{:,.0f}%'.format)
        city_metrics_week_wow[item] = city_metrics_week_wow[item].map('{:,.0f}%'.format)
    city_metrics_wow['date'] = pd.to_datetime(city_metrics_wow["date"], errors="coerce").dt.strftime("%d.%m.%y")
    city_metrics_wow['date'] = city_metrics_wow['date'] + ' wow'
    columns.append('region_name')
    city_metrics_week_wow = city_metrics_week_wow[columns]
    city_metrics_week_wow['date'] = 'week_wow'
    city_metrics_week_wow['plan_fact_orders_mistake'] = np.nan
    city_metrics_week_wow['plan_fact_sh'] = np.nan

    # итоговая сборка
    city_metrics_week_output = pd.concat([city_metrics_per_day, city_metrics_week])
    city_metrics_week_output = pd.concat([city_metrics_week_output, city_metrics_week_wow])
    city_metrics_week_output = pd.concat([city_metrics_week_output, city_metrics_wow])
    Msc_day = city_metrics_week_output[city_metrics_week_output['region_name'] == 'Москва'].set_index('date').T.fillna('')
    Spb_day = city_metrics_week_output[city_metrics_week_output['region_name'] == 'Санкт-Петербург'].set_index('date').T.fillna('')
    Nnv_day = city_metrics_week_output[city_metrics_week_output['region_name'] == 'Нижний Новгород'].set_index('date').T.fillna('')
    Kzn_day = city_metrics_week_output[city_metrics_week_output['region_name'] == 'Казань'].set_index('date').T.fillna('')
    Ekb_day = city_metrics_week_output[city_metrics_week_output['region_name'] == 'Екатеринбург'].set_index('date').T.fillna('')
#     Irk_day = city_metrics_week_output[city_metrics_week_output['region_name'] == 'Иркутск'].set_index('date').T.fillna('')
    Rnd_day = city_metrics_week_output[city_metrics_week_output['region_name'] == 'Ростов-на-Дону'].set_index('date').T.fillna('')
    Krd_day = city_metrics_week_output[city_metrics_week_output['region_name'] == 'Краснодар'].set_index('date').T.fillna('')
    Nsk_day = city_metrics_week_output[city_metrics_week_output['region_name'] == 'Новосибирск'].set_index('date').T.fillna('')

    # выстраивание столбцов для чтения
    columns = []
    current_date = monday
    while current_date <= sunday:
        columns.append(current_date.strftime("%d.%m.%y"))
        columns.append(current_date.strftime("%d.%m.%y") + " wow")
        current_date = current_date + datetime.timedelta(days=1)
    columns.append('week')
    columns.append('week_wow')
    if days_to_week_end == 6:
        Msc_day[sunday.strftime("%d.%m.%y")] = Msc_day[(sunday - datetime.timedelta(days=1)).strftime("%d.%m.%y")]
        Msc_day[sunday.strftime("%d.%m.%y") + ' wow'] = Msc_day[(sunday - datetime.timedelta(days=1)).strftime("%d.%m.%y")]
        Spb_day[sunday.strftime("%d.%m.%y")] = Spb_day[(sunday - datetime.timedelta(days=1)).strftime("%d.%m.%y")]
        Spb_day[sunday.strftime("%d.%m.%y") + ' wow'] = Spb_day[(sunday - datetime.timedelta(days=1)).strftime("%d.%m.%y")]
        Nnv_day[sunday.strftime("%d.%m.%y")] = Nnv_day[(sunday - datetime.timedelta(days=1)).strftime("%d.%m.%y")]
        Nnv_day[sunday.strftime("%d.%m.%y") + ' wow'] = Nnv_day[(sunday - datetime.timedelta(days=1)).strftime("%d.%m.%y")]
        Kzn_day[sunday.strftime("%d.%m.%y")] = Kzn_day[(sunday - datetime.timedelta(days=1)).strftime("%d.%m.%y")]
        Kzn_day[sunday.strftime("%d.%m.%y") + ' wow'] = Kzn_day[(sunday - datetime.timedelta(days=1)).strftime("%d.%m.%y")]
        Ekb_day[sunday.strftime("%d.%m.%y")] = Ekb_day[(sunday - datetime.timedelta(days=1)).strftime("%d.%m.%y")]
        Ekb_day[sunday.strftime("%d.%m.%y") + ' wow'] = Ekb_day[(sunday - datetime.timedelta(days=1)).strftime("%d.%m.%y")]
#         Irk_day[sunday.strftime("%d.%m.%y")] = Irk_day[(sunday - datetime.timedelta(days=1)).strftime("%d.%m.%y")]
#         Irk_day[sunday.strftime("%d.%m.%y") + ' wow'] = Irk_day[(sunday - datetime.timedelta(days=1)).strftime("%d.%m.%y")]
        Rnd_day[sunday.strftime("%d.%m.%y")] = Rnd_day[(sunday - datetime.timedelta(days=1)).strftime("%d.%m.%y")]
        Rnd_day[sunday.strftime("%d.%m.%y") + ' wow'] = Rnd_day[(sunday - datetime.timedelta(days=1)).strftime("%d.%m.%y")]
        Krd_day[sunday.strftime("%d.%m.%y")] = Krd_day[(sunday - datetime.timedelta(days=1)).strftime("%d.%m.%y")]
        Krd_day[sunday.strftime("%d.%m.%y") + ' wow'] = Krd_day[(sunday - datetime.timedelta(days=1)).strftime("%d.%m.%y")]
        Nsk_day[sunday.strftime("%d.%m.%y")] = Nsk_day[(sunday - datetime.timedelta(days=1)).strftime("%d.%m.%y")]
        Nsk_day[sunday.strftime("%d.%m.%y") + ' wow'] = Nsk_day[(sunday - datetime.timedelta(days=1)).strftime("%d.%m.%y")]
        
    Msc_day = Msc_day[columns]
    Msc_day[today.strftime("%d.%m.%y") + ' wow'] = 'nan%'
    Msc_day[today.strftime("%d.%m.%y")] = 'nan%'
    Msc_day.at['region_name', today.strftime("%d.%m.%y") + ' wow'] = 'завтра'
    Msc_day.at['region_name', today.strftime("%d.%m.%y")] = 'Метрики'
    Spb_day = Spb_day[columns]
    Spb_day[today.strftime("%d.%m.%y") + ' wow'] = 'nan%'
    Spb_day[today.strftime("%d.%m.%y")] = 'nan%'
    Spb_day.at['region_name', today.strftime("%d.%m.%y") + ' wow'] = 'завтра'
    Spb_day.at['region_name', today.strftime("%d.%m.%y")] = 'Метрики'
    Nnv_day = Nnv_day[columns]
    Nnv_day[today.strftime("%d.%m.%y") + ' wow'] = 'nan%'
    Nnv_day[today.strftime("%d.%m.%y")] = 'nan%'
    Nnv_day.at['region_name', today.strftime("%d.%m.%y") + ' wow'] = 'завтра'
    Nnv_day.at['region_name', today.strftime("%d.%m.%y")] = 'Метрики'
    Kzn_day = Kzn_day[columns]
    Kzn_day[today.strftime("%d.%m.%y") + ' wow'] = 'nan%'
    Kzn_day[today.strftime("%d.%m.%y")] = 'nan%'
    Kzn_day.at['region_name', today.strftime("%d.%m.%y") + ' wow'] = 'завтра'
    Kzn_day.at['region_name', today.strftime("%d.%m.%y")] = 'Метрики'
    Ekb_day = Ekb_day[columns]
    Ekb_day[today.strftime("%d.%m.%y") + ' wow'] = 'nan%'
    Ekb_day[today.strftime("%d.%m.%y")] = 'nan%'
    Ekb_day.at['region_name', today.strftime("%d.%m.%y") + ' wow'] = 'завтра'
    Ekb_day.at['region_name', today.strftime("%d.%m.%y")] = 'Метрики'
#     Irk_day = Irk_day[columns]
#     Irk_day[today.strftime("%d.%m.%y") + ' wow'] = 'nan%'
#     Irk_day[today.strftime("%d.%m.%y")] = 'nan%'
#     Irk_day.at['region_name', today.strftime("%d.%m.%y") + ' wow'] = 'завтра'
#     Irk_day.at['region_name', today.strftime("%d.%m.%y")] = 'Метрики'
    Rnd_day = Rnd_day[columns]
    Rnd_day[today.strftime("%d.%m.%y") + ' wow'] = 'nan%'
    Rnd_day[today.strftime("%d.%m.%y")] = 'nan%'
    Rnd_day.at['region_name', today.strftime("%d.%m.%y") + ' wow'] = 'завтра'
    Rnd_day.at['region_name', today.strftime("%d.%m.%y")] = 'Метрики'
    Krd_day = Krd_day[columns]
    Krd_day[today.strftime("%d.%m.%y") + ' wow'] = 'nan%'
    Krd_day[today.strftime("%d.%m.%y")] = 'nan%'
    Krd_day.at['region_name', today.strftime("%d.%m.%y") + ' wow'] = 'завтра'
    Krd_day.at['region_name', today.strftime("%d.%m.%y")] = 'Метрики'
    Nsk_day = Nsk_day[columns]
    Nsk_day[today.strftime("%d.%m.%y") + ' wow'] = 'nan%'
    Nsk_day[today.strftime("%d.%m.%y")] = 'nan%'
    Nsk_day.at['region_name', today.strftime("%d.%m.%y") + ' wow'] = 'завтра'
    Nsk_day.at['region_name', today.strftime("%d.%m.%y")] = 'Метрики'
    
    for i in range(0, 6):
        column_name = (monday + datetime.timedelta(days=i)).strftime("%d.%m.%y") + " wow" 
        Msc_day = Msc_day.rename(
            columns={column_name : "wow"}).replace({'nan%':''}).replace('Москва', 'Msk')
        Spb_day = Spb_day.rename(
            columns={column_name : "wow"}).replace({'nan%':''}).replace('Санкт-Петербург', 'Spb')
        Nnv_day = Nnv_day.rename(
            columns={column_name : "wow"}).replace({'nan%':''}).replace('Нижний Новгород', 'Nnv')
        Kzn_day = Kzn_day.rename(
            columns={column_name : "wow"}).replace({'nan%':''}).replace('Казань', 'Kzn')
        Ekb_day = Ekb_day.rename(
            columns={column_name : "wow"}).replace({'nan%':''}).replace('Екатеринбург', 'Ekb')
#         Irk_day = Irk_day.rename(
#             columns={column_name : "wow"}).replace({'nan%':''})
        Rnd_day = Rnd_day.rename(
            columns={column_name : "wow"}).replace({'nan%':''}).replace('Ростов-на-Дону', 'Rnd')
        Krd_day = Krd_day.rename(
            columns={column_name : "wow"}).replace({'nan%':''}).replace('Краснодар', 'Krd')
        Nsk_day = Nsk_day.rename(
            columns={column_name : "wow"}).replace({'nan%':''}).replace('Новосибирск', 'Nsk')
    
#     Msc_day = Msc_day[columns].fillna(' ')
#     Spb_day = Spb_day[columns].fillna(' ')
#     Nnv_day = Nnv_day[columns].fillna(' ')
#     Kzn_day = Kzn_day[columns].fillna(' ')
#     Ekb_day = Ekb_day[columns].fillna(' ')
#     Irk_day = Irk_day[columns].fillna(' ')
#     Rnd_day = Rnd_day[columns].fillna(' ')
#     Krd_day = Krd_day[columns].fillna(' ')
#     Nsk_day = Nsk_day[columns].fillna(' ')

    def unit():
        unit = pd.read_csv('config.csv', sep = ';')
        return unit
    
    Msc_week = city_metrics_per_week[city_metrics_per_week['region_name'] == 'Москва'].set_index('week').T
    Spb_week = city_metrics_per_week[city_metrics_per_week['region_name'] == 'Санкт-Петербург'].set_index('week').T
    Nnv_week = city_metrics_per_week[city_metrics_per_week['region_name'] == 'Нижний Новгород'].set_index('week').T
    Kzn_week = city_metrics_per_week[city_metrics_per_week['region_name'] == 'Казань'].set_index('week').T
    Ekb_week = city_metrics_per_week[city_metrics_per_week['region_name'] == 'Екатеринбург'].set_index('week').T
#     Irk_week = city_metrics_per_week[city_metrics_per_week['region_name'] == 'Иркутск'].set_index('week').T
    Rnd_week = city_metrics_per_week[city_metrics_per_week['region_name'] == 'Ростов-на-Дону'].set_index('week').T
    Krd_week = city_metrics_per_week[city_metrics_per_week['region_name'] == 'Краснодар'].set_index('week').T
    Nsk_week = city_metrics_per_week[city_metrics_per_week['region_name'] == 'Новосибирск'].set_index('week').T
    
    Msc_week.to_csv('Msc.csv')
    Spb_week.to_csv('Spb.csv')
    Nnv_week.to_csv('Nnv.csv')
    Kzn_week.to_csv('Kzn.csv')
    Ekb_week.to_csv('Ekb.csv')
#     Irk_week.to_csv('Irk.csv')
    Rnd_week.to_csv('Rnd.csv')
    Krd_week.to_csv('Krd.csv')
    Nsk_week.to_csv('Nsk.csv')
    
    Msc_week = pd.merge(pd.read_csv('Msc.csv').rename(columns={'Unnamed: 0':'week'}), unit(), on = 'week', how='left').fillna('').set_index('week').replace('Москва', 'Msk')
    Spb_week = pd.merge(pd.read_csv('Spb.csv').rename(columns={'Unnamed: 0':'week'}), unit(), on = 'week', how='left').fillna('').set_index('week').replace('Санкт-Петербург', 'Spb')
    Nnv_week = pd.merge(pd.read_csv('Nnv.csv').rename(columns={'Unnamed: 0':'week'}), unit(), on = 'week', how='left').fillna('').set_index('week').replace('Нижний Новгород', 'Nnv')
    Kzn_week = pd.merge(pd.read_csv('Kzn.csv').rename(columns={'Unnamed: 0':'week'}), unit(), on = 'week', how='left').fillna('').set_index('week').replace('Казань', 'Kzn')
    Ekb_week = pd.merge(pd.read_csv('Ekb.csv').rename(columns={'Unnamed: 0':'week'}), unit(), on = 'week', how='left').fillna('').set_index('week').replace('Екатеринбург', 'Ekb')
#     Irk_week = pd.merge(pd.read_csv('Irk.csv').rename(columns={'Unnamed: 0':'week'}), unit(), on = 'week', how='left').fillna('').set_index('week').replace('Иркутск', 'Irk')
    Rnd_week = pd.merge(pd.read_csv('Rnd.csv').rename(columns={'Unnamed: 0':'week'}), unit(), on = 'week', how='left').fillna('').set_index('week').replace('Ростов-на-Дону', 'Rnd')
    Krd_week = pd.merge(pd.read_csv('Krd.csv').rename(columns={'Unnamed: 0':'week'}), unit(), on = 'week', how='left').fillna('').set_index('week').replace('Краснодар', 'Krd')
    Nsk_week = pd.merge(pd.read_csv('Nsk.csv').rename(columns={'Unnamed: 0':'week'}), unit(), on = 'week', how='left').fillna('').set_index('week').replace('Новосибирск', 'Nsk')
    
    cols = Msc_week.columns.tolist()
    cols = cols[-1:] + cols[:-1]
    
    Msc_week = Msc_week[cols]
    Spb_week = Spb_week[cols]
    Nnv_week = Nnv_week[cols]
    Kzn_week = Kzn_week[cols]
    Ekb_week = Ekb_week[cols]
#     Irk_week = Irk_week[cols]
    Rnd_week = Rnd_week[cols]
    Krd_week = Krd_week[cols]
    #Nsk_week = Nsk_week[cols]
    Msc_week.columns = pd.MultiIndex.from_tuples(zip(['-', 'w', 'e', 'e', 'k', 'l', 'y', '-', 'm', 'e', 't', 'r', 'i', 'c', 's', '-'], Msc_week.columns))
    Spb_week.columns = pd.MultiIndex.from_tuples(zip(['-', 'w', 'e', 'e', 'k', 'l', 'y', '-', 'm', 'e', 't', 'r', 'i', 'c', 's', '-'], Spb_week.columns))
    Nnv_week.columns = pd.MultiIndex.from_tuples(zip(['-', 'w', 'e', 'e', 'k', 'l', 'y', '-', 'm', 'e', 't', 'r', 'i', 'c', 's', '-'], Nnv_week.columns))
    Kzn_week.columns = pd.MultiIndex.from_tuples(zip(['-', 'w', 'e', 'e', 'k', 'l', 'y', '-', 'm', 'e', 't', 'r', 'i', 'c', 's', '-'], Kzn_week.columns))
    Ekb_week.columns = pd.MultiIndex.from_tuples(zip(['-', 'w', 'e', 'e', 'k', 'l', 'y', '-', 'm', 'e', 't', 'r', 'i', 'c', 's', '-'], Ekb_week.columns))
#     Irk_week.columns = pd.MultiIndex.from_tuples(zip(['-', 'w', 'e', 'e', 'k', 'l', 'y', '-', 'm', 'e', 't', 'r', 'i', 'c', 's', '-'], Irk_week.columns))
    Rnd_week.columns = pd.MultiIndex.from_tuples(zip(['-', 'w', 'e', 'e', 'k', 'l', 'y', '-', 'm', 'e', 't', 'r', 'i', 'c', 's', '-'], Rnd_week.columns))
    Krd_week.columns = pd.MultiIndex.from_tuples(zip(['-', 'w', 'e', 'e', 'k', 'l', 'y', '-', 'm', 'e', 't', 'r', 'i', 'c', 's', '-'], Krd_week.columns))
    #Nsk_week.columns = pd.MultiIndex.from_tuples(zip(['-', 'w', 'e', 'e', 'k', 'l', 'y', '-', 'm', 'e', 't', 'r', 'i', 'c', 's', '-'], Nsk_week.columns))
    Msc_day.columns = pd.MultiIndex.from_tuples(zip(['-', 'd', 'a', 'i', 'l', 'y', '-', '-', 'm', 'e', 't', 'r', 'i', 'c', 's', '-'], Msc_day.columns))
    Spb_day.columns = pd.MultiIndex.from_tuples(zip(['-', 'd', 'a', 'i', 'l', 'y', '-', '-','m', 'e', 't', 'r', 'i', 'c', 's', '-'], Spb_day.columns))
    Nnv_day.columns = pd.MultiIndex.from_tuples(zip(['-', 'd', 'a', 'i', 'l', 'y', '-', '-','m', 'e', 't', 'r', 'i', 'c', 's', '-'], Nnv_day.columns))
    Kzn_day.columns = pd.MultiIndex.from_tuples(zip(['-', 'd', 'a', 'i', 'l', 'y', '-', '-','m', 'e', 't', 'r', 'i', 'c', 's', '-'], Kzn_day.columns))
    Ekb_day.columns = pd.MultiIndex.from_tuples(zip(['-', 'd', 'a', 'i', 'l', 'y', '-', '-','m', 'e', 't', 'r', 'i', 'c', 's', '-'], Ekb_day.columns))
#     Irk_day.columns = pd.MultiIndex.from_tuples(zip(['-', 'd', 'a', 'i', 'l', 'y', '-', '-','m', 'e', 't', 'r', 'i', 'c', 's', '-'], Irk_day.columns))
    Rnd_day.columns = pd.MultiIndex.from_tuples(zip(['-', 'd', 'a', 'i', 'l', 'y', '-', '-','m', 'e', 't', 'r', 'i', 'c', 's', '-'], Rnd_day.columns))
    Krd_day.columns = pd.MultiIndex.from_tuples(zip(['-', 'd', 'a', 'i', 'l', 'y', '-', '-','m', 'e', 't', 'r', 'i', 'c', 's', '-'], Krd_day.columns))
    Nsk_day.columns = pd.MultiIndex.from_tuples(zip(['-', 'd', 'a', 'i', 'l', 'y', '-', '-','m', 'e', 't', 'r', 'i', 'c', 's', '-'], Nsk_day.columns))
    
    import dataframe_image as dfi
    dfi.export(Msc_day, 'Msc.png', table_conversion = 'matplotlib')
    dfi.export(Spb_day, 'Spb.png', table_conversion = 'matplotlib')
    dfi.export(Nnv_day, 'Nnv.png', table_conversion = 'matplotlib')
    dfi.export(Kzn_day, 'Kzn.png', table_conversion = 'matplotlib')
    dfi.export(Ekb_day, 'Ekb.png', table_conversion = 'matplotlib')
#     dfi.export(Irk_day, 'Irk.png', table_conversion = 'matplotlib')
    dfi.export(Rnd_day, 'Rnd.png', table_conversion = 'matplotlib')
    dfi.export(Krd_day, 'Krd.png', table_conversion = 'matplotlib')
    dfi.export(Nsk_day, 'Nsk.png', table_conversion = 'matplotlib')
    dfi.export(Msc_week, 'Msc_week.png', table_conversion = 'matplotlib')
    dfi.export(Spb_week, 'Spb_week.png', table_conversion = 'matplotlib')
    dfi.export(Nnv_week, 'Nnv_week.png', table_conversion = 'matplotlib')
    dfi.export(Kzn_week, 'Kzn_week.png', table_conversion = 'matplotlib')
    dfi.export(Ekb_week, 'Ekb_week.png', table_conversion = 'matplotlib')
#     dfi.export(Irk_week, 'Irk_week.png', table_conversion = 'matplotlib')
    dfi.export(Rnd_week, 'Rnd_week.png', table_conversion = 'matplotlib')
    dfi.export(Krd_week, 'Krd_week.png', table_conversion = 'matplotlib')
    dfi.export(Nsk_week, 'Nsk_week.png', table_conversion = 'matplotlib')

    return

report()