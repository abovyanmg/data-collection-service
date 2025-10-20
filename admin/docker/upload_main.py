import json
import os
from datetime import datetime, timedelta
from morin import WBbyDate
from morin import MSKLDbyDate
from morin import GCbyDate
from morin import OZONbyDate
from morin import OZONANbyDate
from morin import YDbyDate
from morin import YMbyDate
from morin import MRKTbyDate
from morin import BTRXbyDate
from morin import VKbyDate
from morin import ALFAbyDate
from morin import DISKbyPage
import time
import asyncio
import threading
import pandas as pd


def parse_source(file_path):
    excel_data = pd.ExcelFile(file_path)
    final_json = []
    for sheet_name in excel_data.sheet_names:
        if sheet_name!='db' and sheet_name!='all_reports':
            sheet_df = excel_data.parse(sheet_name)
            table_df = get_top_left_table(sheet_df)
            table_df = table_df[table_df['conn_num'] != 'пример']
            table_df= table_df.drop(columns=['conn_num'])
            df_filtered = table_df.dropna(subset=['db_num'])
            df_filtered = df_filtered[df_filtered['db_num'] != '']
            df_filtered['db_num'] = df_filtered['db_num'].astype(int)
            df_filtered['platform'] = sheet_name
            try:
                df_filtered['backfill_days'] = df_filtered['backfill_days'].fillna(0)
                df_filtered['backfill_days'] = df_filtered['backfill_days'].astype(int)
            except: pass
            df_filtered = df_filtered.fillna("")
            data_as_dict = df_filtered.to_dict(orient="records")
            final_json = final_json + data_as_dict
    return final_json

def parse_db(file_path):
    excel_data = pd.ExcelFile(file_path)
    final_json = []
    for sheet_name in excel_data.sheet_names:
        if sheet_name =='db':
            sheet_df = excel_data.parse(sheet_name)
            table_df = get_top_left_table(sheet_df)
            table_df = table_df[table_df['db_num'] != 'пример']
            df_filtered = table_df.dropna(subset=['database'])
            df_filtered = df_filtered[df_filtered['database'] != '']
            try: df_filtered['db_num'] = df_filtered['db_num'].astype(int)
            except: pass
            try: df_filtered['port'] = df_filtered['port'].astype(int)
            except: pass
            df_filtered = df_filtered.fillna("")
            data_as_dict = df_filtered.to_dict(orient="records")
            final_json = final_json + data_as_dict
    return final_json

def get_top_left_table(df):
    start_row = 0
    start_col = 0
    for i, row in df.iterrows():
        if not row.isnull().all():
            start_row = i
            break
    for j, col in df.items():
        if not col.isnull().all():
            start_col = df.columns.get_loc(j)
            break
    table_df = df.iloc[start_row:, start_col:].dropna(how="all").reset_index(drop=True)
    table_df.columns = table_df.iloc[0]  # Устанавливаем первую строку как заголовок
    table_df = table_df[1:].reset_index(drop=True)  # Убираем первую строку, которая стала заголовком
    return table_df

def get_db(num):
    for db in db_data:
        if db["db_num"] == num:
            return {
                "host": db["host"],
                "port": db["port"],
                "username": db["username"],
                "password": db["password"].strip(),
                "database": db["database"],
                "bot_token": db['bot_token'],
                "chats": db['chats'],
                "message_type": db['message_type']
            }
    return None

def run_task_yd(client, db):
    print(f"Запуск задачи по Директу в {datetime.now().strftime('%H:%M')}")
    connection = YDbyDate(
        db.get('bot_token'),
        db.get('chats'),
        db.get('message_type'),
        db.get('subd'),
        db.get('host'),
        int(db.get('port')),
        db.get('username'),
        db.get('password'),
        db.get('database'),
        client.get('add_name'),
        client.get('login'),
        client.get('token'),
        client.get('start'),
        client.get('backfill_days'),
        client.get('columns'),
        client.get('report').replace(' ',''),
        client.get('goals'),
        client.get('attributions')
    )
    connection.collecting_manager()

def run_task_ym(client, db):
    print(f"Запуск задачи по Метрике в {datetime.now().strftime('%H:%M')}")
    connection = YMbyDate(
        db.get('bot_token'),
        db.get('chats'),
        db.get('message_type'),
        db.get('subd'),
        db.get('host'),
        int(db.get('port')),
        db.get('username'),
        db.get('password'),
        db.get('database'),
        client.get('add_name'),
        client.get('login'),
        client.get('token'),
        client.get('start'),
        client.get('backfill_days'),
        client.get('report').replace(' ',''),
        client.get('dimensions').replace(' ',''),
        client.get('metrics').replace(' ',''),
        client.get('filters')
    )
    connection.collecting_manager()

def run_task_mskld(client, db):
    print(f"Запуск задачи по Мойсклад в {datetime.now().strftime('%H:%M')}")
    connection = MSKLDbyDate(
        db.get('bot_token'),
        db.get('chats'),
        db.get('message_type'),
        db.get('subd'),
        db.get('host'),
        int(db.get('port')),
        db.get('username'),
        db.get('password'),
        db.get('database'),
        client.get('add_name'),
        client.get('token'),
        client.get('start'),
        client.get('backfill_days'),
        client.get('reports').replace(' ','')
    )
    connection.collecting_manager()



def run_task_gc(client, db):
    print(f"Запуск задачи по Getcourse в {datetime.now().strftime('%H:%M')}")
    connection = GCbyDate(
        db.get('bot_token'),
        db.get('chats'),
        db.get('message_type'),
        db.get('subd'),
        db.get('host'),
        int(db.get('port')),
        db.get('username'),
        db.get('password'),
        db.get('database'),
        client.get('add_name'),
        client.get('clientid'),
        client.get('token'),
        client.get('start'),
        client.get('group_id'),
        client.get('reports').replace(' ','')
    )
    connection.collecting_manager()

def run_task_disk(client, db):
    print(f"Запуск задачи по Яндекс Диск в {datetime.now().strftime('%H:%M')}")
    connection = DISKbyPage(
        db.get('bot_token'),
        db.get('chats'),
        db.get('message_type'),
        db.get('subd'),
        db.get('host'),
        int(db.get('port')),
        db.get('username'),
        db.get('password'),
        db.get('database'),
        client.get('add_name'),
        client.get('link'),
        client.get('token'),
        client.get('start'),
        client.get('reports').replace(' ','')
    )
    connection.collecting_manager()

def run_task_wb(client, db):
    print(f"Запуск задачи по WB в {datetime.now().strftime('%H:%M')}")
    connection = WBbyDate(
        db.get('bot_token'),
        db.get('chats'),
        db.get('message_type'),
        db.get('subd'),
        db.get('host'),
        int(db.get('port')),
        db.get('username'),
        db.get('password'),
        db.get('database'),
        client.get('add_name'),
        client.get('token'),
        client.get('start'),
        client.get('backfill_days'),
        client.get('reports').replace(' ','')
    )
    connection.collecting_manager()

def run_task_vk(client, db):
    print(f"Запуск задачи по VK в {datetime.now().strftime('%H:%M')}")
    connection = VKbyDate(
        db.get('bot_token'),
        db.get('chats'),
        db.get('message_type'),
        db.get('subd'),
        db.get('host'),
        int(db.get('port')),
        db.get('username'),
        db.get('password'),
        db.get('database'),
        client.get('add_name'),
        client.get('token'),
        client.get('start'),
        client.get('backfill_days'),
        client.get('reports').replace(' ','')
    )
    connection.collecting_manager()

def run_task_btrx(client, db):
    print(f"Запуск задачи по BTRX в {datetime.now().strftime('%H:%M')}")
    connection = BTRXbyDate(
        db.get('bot_token'),
        db.get('chats'),
        db.get('message_type'),
        db.get('subd'),
        db.get('host'),
        int(db.get('port')),
        db.get('username'),
        db.get('password'),
        db.get('database'),
        client.get('add_name'),
        client.get('webhook_link'),
        client.get('start'),
        client.get('backfill_days'),
        client.get('reports').replace(' ','')
    )
    connection.collecting_manager()

def run_task_ozon(client, db):
    print(f"Запуск задачи по OZON в {datetime.now().strftime('%H:%M')}")
    connection = OZONbyDate(
        db.get('bot_token'),
        db.get('chats'),
        db.get('message_type'),
        db.get('subd'),
        db.get('host'),
        int(db.get('port')),
        db.get('username'),
        db.get('password'),
        db.get('database'),
        client.get('add_name'),
        str(client.get('clientid')),
        client.get('token'),
        client.get('start'),
        client.get('backfill_days'),
        client.get('reports').replace(' ','')
    )
    connection.collecting_manager()


def run_task_ozonan(client, db):
    print(f"Запуск задачи по OZON Analytics в {datetime.now().strftime('%H:%M')}")
    connection = OZONANbyDate(
        db.get('bot_token'),
        db.get('chats'),
        db.get('message_type'),
        db.get('subd'),
        db.get('host'),
        int(db.get('port')),
        db.get('username'),
        db.get('password'),
        db.get('database'),
        client.get('add_name'),
        str(client.get('clientid')),
        client.get('token'),
        client.get('start'),
        client.get('backfill_days'),
        client.get('dimensions'),
        client.get('metrics'),
        client.get('reports').replace(' ','')
    )
    connection.collecting_manager()

def run_task_alfa(client, db):
    print(f"Запуск задачи по ALFACRM в {datetime.now().strftime('%H:%M')}")
    connection = ALFAbyDate(
        db.get('bot_token'),
        db.get('chats'),
        db.get('message_type'),
        db.get('subd'),
        db.get('host'),
        int(db.get('port')),
        db.get('username'),
        db.get('password'),
        db.get('database'),
        client.get('add_name'),
        str(client.get('main_url')),
        str(client.get('token')),
        str(client.get('xappkey')),
        str(client.get('email')),
        client.get('start'),
        client.get('backfill_days'),
        client.get('reports').replace(' ',''),
        client.get('branches')
    )
    connection.collecting_manager()

def run_task_mrkt(client, db):
    print(f"Запуск задачи по Яндекс Маркету в {datetime.now().strftime('%H:%M')}")
    connection = MRKTbyDate(
        db.get('bot_token'),
        db.get('chats'),
        db.get('message_type'),
        db.get('subd'),
        db.get('host'),
        int(db.get('port')),
        db.get('username'),
        db.get('password'),
        db.get('database'),
        client.get('add_name'),
        str(client.get('clientid')),
        client.get('token'),
        client.get('start'),
        client.get('backfill_days'),
        client.get('reports').replace(' ','')
    )
    connection.collecting_manager()

def should_run_task(schedule_times):
    now = (datetime.now() + timedelta(hours=3)).strftime("%H:%M")
    for sh_time in schedule_times:
        sh_time_strip = sh_time.strip()
        if len(sh_time_strip) == 4:
            schedule_times.append(f'0{sh_time_strip}')
        if len(sh_time) > 5:
            schedule_times.append(f'{sh_time_strip}')
    return now in schedule_times


def run_task(client):
    db = get_db(client.get('db_num'))
    if client.get('platform') == 'wb':
        run_task_wb(client, db)
    if client.get('platform') == 'ozon':
        run_task_ozon(client, db)
    if client.get('platform') == 'ozonan':
        run_task_ozonan(client, db)
    if client.get('platform') == 'alfa':
        run_task_alfa(client, db)
    if client.get('platform') == 'mrkt':
        run_task_mrkt(client, db)
    if client.get('platform') == 'yd':
        run_task_yd(client, db)
    if client.get('platform') == 'ym':
        run_task_ym(client, db)
    if client.get('platform') == 'gc':
        run_task_gc(client, db)
    if client.get('platform') == 'btrx':
        run_task_btrx(client, db)
    if client.get('platform') == 'vk':
        run_task_vk(client, db)
    if client.get('platform') == 'disk':
        run_task_disk(client, db)
    if client.get('platform') == 'mskld':
        run_task_mskld(client, db)


async def schedule_tasks():
    while True:
        for client in clients_data:
            schedule_times = client.get("schedule_time", "").split(",")
            if should_run_task(schedule_times) and client != current_client and client not in tasks:
                tasks.append(client)
        await asyncio.sleep(20)

current_dir = os.path.dirname(__file__)
settings_file_path = os.path.join(current_dir, 'settings.xlsx')

tasks = []
current_client = {}

clients_data = parse_source(settings_file_path)
db_data = parse_db(settings_file_path)

for client in clients_data:
    run_task(client)

def start_schedule():
    asyncio.run(schedule_tasks())

# Запускаем планировщик в отдельном потоке
threading.Thread(target=start_schedule, daemon=True).start()

while True:
    if tasks:
        current_client = tasks.pop(0)  # Берем первую задачу из очереди
        run_task(current_client)
        current_client = {}
    else:
        time.sleep(60)


