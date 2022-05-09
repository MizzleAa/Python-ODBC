"""
odbc

mssql -> tibero
- EXAMPLE_INFO

tibero -> mssql
- EXAMPLE_INFO
"""

import config as cfg
import time
import datetime
import string
import random

from lib.odbc import ODBC
from datetime import timedelta


class DatabaseConnect:
    """DatabaseConnect : Tibero 및 MSSQL db 연결
    """

    def __init__(self):
        """DatabaseConnect, __init__

        database를 연결하기 위한 초기 설정

        Args : 
            None

        Return : 
            None

        """
        self.tibero = ODBC(
            driver=None,
            server=None,
            database=cfg.tiberoDatabase,
            dsn=cfg.tiberoDSN,
            uid=cfg.tiberoID,
            pwd=cfg.tiberoPWD
        )

        self.mssql = ODBC(
            driver=cfg.mssqlDriver,
            server=f'{cfg.mssqlIP},{cfg.mssqlPort}',
            database=cfg.mssqlDatabase,
            dsn=None,
            uid=cfg.mssqlUsername,
            pwd=cfg.mssqlPassword
        )


class Calcurate:

    def time_check(self, table_name, input_time):
        day = datetime.datetime.now()

        hour = str(day.hour).zfill(2)
        minute = str(day.minute).zfill(2)

        result = f"{hour}:{minute}"

        #print(input_time, result)
        cfg.log.info(
            f"[ {table_name} ] : Now time({result}) / Active time ({input_time})")
        if result == input_time:
            cfg.log.info(f"[ {table_name} ] : Active !!")
            return True
        else:
            return False

    def calcurate_days(self, days):
        """Calcurate, calcurate_days

        특정 날짜 계산

        Args : 
            day ( int ) : 전일 후일 계산용 변수

        Return : 
            None

        """
        day = datetime.datetime.now() + timedelta(days=days)
        result = datetime.datetime(day.year, day.month, day.day)
        return result

class Example(DatabaseConnect, Calcurate):
    """
    EXAMPLE_INFO
    - 원본 값에 EXAMPLE_INFO key값과 위치 추가
    - 검색 조건기준은 전일 00:00시 부터 23:59까지
    """

    def __init__(self):
        super().__init__()

    def run(self, input_time, options="day"):
        while True:
            if self.time_check("EXAMPLE_INFO", input_time):
                self.process()
                time.sleep(60)
            time.sleep(30)

    def process(self, y=-1):
        self.mssql.open()
        self.tibero.open()

        today = self.calcurate_days(0)
        yesterday = self.calcurate_days(y)
        self.mssql.update_wheres(
            "EXAMPLE_INFO",
            {
                "OWNER_CD": "",
                "OWNER_NM": "",
                "USR_ID": "",
                "USR_PWD": "",
                "SEND_NM": "",
                "RECV_TEL": "",
                "RECV_NM": "",
            },
            "( REG_DATE >= ? ) AND ( REG_DATE < ? )",
            [yesterday, today]
        )

        recodes = self.mssql.select_wheres_lock(
            "EXAMPLE_INFO",
            "( REG_DATE >= ? ) AND ( REG_DATE < ? )",
            [yesterday, today]
        )

        for i, r in enumerate(recodes):
            try:
                data = list(r)
                data.append(cfg.groupName)

                self.tibero.insert_all("SPC501M", data)
                cfg.log.info(f"[ EXAMPLE_INFO ] {data}")
                del data
            except Exception as ex:
                cfg.log.warning(f"[ EXAMPLE_INFO ] : {ex}")

        self.mssql.close()
        self.tibero.close()

        del today, yesterday, recodes

    def rand_data(self, size):
        string_pool = string.ascii_letters + string.digits
        random_list = [random.choice(string_pool) for _ in range(size)]
        result = ''.join(random_list)
        return result

    def virtual_make(self, size=100, seconds=0.01):
        for _ in range(size):
            a = self.rand_data(11)
            b = self.rand_data(4)
            c = self.rand_data(4)
            d = self.rand_data(20)
            e = self.rand_data(20)
            reg_date = datetime.datetime.now() + timedelta(days=-1)

            columns = [
                "a", "b", "c", "d", "e", "reg_date"
            ]
            params = [
                a, b, c, d, e, reg_date
            ]
            self.mssql.insert_columns("EXAMPLE_INFO", columns, params)
            time.sleep(seconds)
