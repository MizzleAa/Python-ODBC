import pyodbc


class ODBC:
    """ODBC : 양방향 db 특성상 orm을 할 수 없는 구조를 직면해서 odbc구조를 orm화 시킴
    """

    def __init__(self, driver: str, server: str, database: str, dsn: str, uid: str, pwd: str):
        """ODBC , __init__

        ODBC Class

        Args :
            driver : driver
            server : server
            database : database
            dsn : DNS
            uid : 계정 ID
            pwd : 계정 PWD

        Return :
            None

        Parameter :
            __connect : ODBC를 연결한다.
            __cursor : SQL Access를 선언한다.
        """
        self.database = database
        self.dsn = dsn
        self.uid = uid
        self.pwd = pwd
        self.driver = driver
        self.server = server
        '''
        if driver is None:
            self.__connect = pyodbc.connect(
                DATABASE=database,
                DSN=dsn,
                UID=uid,
                PWD=pwd
            )

        else:
            self.__connect = pyodbc.connect(
                DRIVER=driver,
                SERVER=server,
                DATABASE=database,
                UID=uid,
                PWD=pwd
            )

        self.__cursor = self.__connect.cursor()

        self.encoding()
        self.decoding()
        '''
        self.open()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def open(self):
        if self.driver is None:
            self.__connect = pyodbc.connect(
                DATABASE=self.database,
                DSN=self.dsn,
                UID=self.uid,
                PWD=self.pwd
            )

        else:
            self.__connect = pyodbc.connect(
                DRIVER=self.driver,
                SERVER=self.server,
                DATABASE=self.database,
                UID=self.uid,
                PWD=self.pwd
            )

        self.__cursor = self.__connect.cursor()

        self.encoding()
        self.decoding()

    def decoding(self, codec='utf-8'):
        """ODBC , decoding

        ODBC decoding을 정의한다.

        Args :
            codec : database codec을 정의한다.
        Return :
            None

        Parameter :
            None
        """
        self.__connect.setdecoding(pyodbc.SQL_CHAR, encoding=codec)
        self.__connect.setdecoding(pyodbc.SQL_WCHAR, encoding=codec)
        # self.__connect.setdecoding(pyodbc.SQL_WMETADATA, encoding=codec)

    def encoding(self, codec='utf-8'):
        """ODBC , encoding

        ODBC encoding를 정의한다.

        Args :
            codec : database codec을 정의한다.
        Return :
            None

        Parameter :
            None
        """

        self.__connect.setencoding(encoding=codec)

    def commit(self):
        """ODBC , commit

        commit

        Args :
            None

        Return :
            None

        Parameter :
            None
        """
        self.__connect.commit()

    def close(self):
        """ODBC , close

        close

        Args :
            None

        Return :
            None

        Parameter :
            None
        """
        self.__cursor.close()
        self.__connect.close()

    def execute(self, sql, params=None):
        """ODBC , execute

        execute

        Args :
            None

        Return :
            None

        Parameter :
            None
        """
        self.__cursor.execute(sql, params or ())

    def fetchall(self):
        """ODBC , fetchall

        fetchall

        Args :
            None

        Return :
            None

        Parameter :
            None
        """
        return self.__cursor.fetchall()

    def fetchone(self):
        """ODBC , fetchone

        fetchone

        Args :
            None

        Return :
            None

        Parameter :
            None
        """
        return self.__cursor.fetchone()

    def select_all(self, table):
        """ODBC , select_all

        table 정보 조회

        Args :
            table ( str ) : table 정의

        Return :
            fetchall

        Parameter :
            sql ( str ) : select * from ~
        """
        sql = f"select * from {table}"
        self.__cursor.execute(sql)
        return self.fetchall()

    def select_all_lock(self, table):
        """ODBC , select_all

        table 정보 조회

        Args :
            table ( str ) : table 정의

        Return :
            fetchall

        Parameter :
            sql ( str ) : select * from ~
        """
        sql = f"select * from {table} with (nolock)"
        self.__cursor.execute(sql)
        return self.fetchall()

    def select_all_count(self, table):
        """ODBC , select_all_count

        table 정보 조회에 따른 row 개수 조회

        Args :
            table ( str ) : table 명칭

        Return :
            fetchall

        Parameter :
            sql ( str ) : select count(*) from ~
        """
        sql = f"select count(*) from {table}"
        self.__cursor.execute(sql)
        return int(self.fetchone()[0])

    def select_wheres_count(self, table, wheres, params):
        """ODBC , select_wheres_count

        table 정보 조회

        Args :
            table ( str ) : table 명칭
            wheres ( str ) : 조건 기준
            params ( list ) : 조건에 충족된 값

        Return :
            fetchall

        Parameter :
            sql ( str ) : select count(*) from {table} where {wheres}
        """

        sql = f"select count(*) from {table} where {wheres}"
        self.__cursor.execute(sql, params)
        return int(self.fetchone()[0])

    def select_wheres_count_lock(self, table, wheres, params):
        """ODBC , select_wheres_count

        table 정보 조회

        Args :
            table ( str ) : table 명칭
            wheres ( str ) : 조건 기준
            params ( list ) : 조건에 충족된 값

        Return :
            fetchall

        Parameter :
            sql ( str ) : select count(*) from {table} where {wheres}
        """

        sql = f"select count(*) from {table} with (nolock) where {wheres}"
        self.__cursor.execute(sql, params)
        return int(self.fetchone()[0])

    def select_columns(self, table, params):
        """ODBC , select_columns

        table 정보 조회

        Args :
            table ( str ) : table 명칭
            params ( list ) : 조건에 충족된 값

        Return :
            fetchall

        Parameter :
            sql ( str ) : select {key} from {table}
        """
        sql = f"select"
        key = ",".join(params)

        sql = f"{sql} {key} from {table}"

        self.__cursor.execute(sql)
        return self.fetchall()

    def select_wheres(self, table, wheres, params):
        """ODBC , select_columns

        table 정보 조회

        Args :
            table ( str ) : table 명칭
            params ( list ) : 조건에 충족된 값

        Return :
            fetchall

        Parameter :
            sql ( str ) : select * from {table} where {wheres}
        """
        sql = f"select * from {table} where {wheres}"
        # print(sql)
        self.__cursor.execute(sql, params)
        return self.fetchall()

    def select_wheres_lock(self, table, wheres, params):
        """ODBC , select_wheres_lock

        table 정보 조회

        Args :
            table ( str ) : table 명칭
            params ( list ) : 조건에 충족된 값

        Return :
            fetchall

        Parameter :
            sql ( str ) : select * from {table} with (nolock) where {wheres}
        """
        sql = f"select * from {table} with (nolock) where {wheres}"
        self.__cursor.execute(sql, params)
        return self.fetchall()

    def insert_all(self, table, params):
        """ODBC , insert_all

        table 정보 삽입

        Args :
            table ( str ) : table 명칭
            params ( list ) : 조건에 충족된 값

        Return :
            fetchall

        Parameter :
            sql ( str ) : insert into {table} values ",".join(["?" for i in range(len(params))])
        """
        sql = f"insert into {table} values"
        value = ",".join(["?" for i in range(len(params))])

        sql = f"{sql} ( {value} )"
        self.__cursor.execute(sql, params)
        self.__connect.commit()

    def insert_columns(self, table, columns, params):
        """ODBC , insert_columns

        table 정보 삽입

        Args :
            table ( str ) : table 명칭
            columns ( list ) : 입력할 컬럼
            params ( list ) : 입력에 충족된 값

        Return :
            fetchall

        Parameter :
            sql ( str ) : insert into {table}
        """

        sql = f"insert into {table}"
        key = ",".join(columns)
        value = ",".join(["?" for column in columns])

        sql = f"{sql} ({key}) values ({value})"

        self.__cursor.execute(sql, params)
        self.__connect.commit()

    def delete_all(self, table):
        """ODBC , delete_all

        table 정보 삭제

        Args :
            table ( str ) : table 명칭

        Return :
            fetchall

        Parameter :
            sql ( str ) : select * from {table} where {wheres}
        """

        sql = f"delete from {table}"
        self.__cursor.execute(sql)
        self.__connect.commit()

    def delete_wheres(self, table, wheres, params):
        """ODBC , delete_wheres

        table 정보 조회

        Args :
            table ( str ) : table 명칭

        Return :
            fetchall

        Parameter :
            sql ( str ) : delete * from {table} where {wheres}
        """

        sql = f"delete from {table} where {wheres}"
        self.__cursor.execute(sql, params)
        self.__connect.commit()

    def update_wheres(self, table, maps, wheres, params):
        tmp = []
        for k, v in enumerate(maps):
            tmp.append(f"{v} = '{maps[v]}'")
        set_sql = ",".join(tmp)

        sql = f"update {table} set {set_sql} where {wheres}"
        self.__cursor.execute(sql, params)
        self.__connect.commit()

    def get_table_columns(self):
        columns = [
            {'name': column[0], 'type': column[1]}
            for column in self.__cursor.description
        ]
        return columns
