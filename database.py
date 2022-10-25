from typing import Optional, Tuple, List, Literal

import psycopg2


class Database:
    def __init__(self, **connection_params: dict):
        try:
            self.__connection = psycopg2.connect(**connection_params)
            self.__cursor = self.__connection.cursor()
        except Exception:
            self.__connection = None
            raise Exception('Ошибка соединения с БД!')

    def select(self,
               table: str,
               fields: Optional[List[str]] = None,
               joins: Optional[List[Tuple[str, str]]] = None,
               group_by: Optional[List[str]] = None,
               order_by: Optional[List[Tuple[str, Literal['DESC', 'ASC']]]] = None,
               where: Optional[str] = None,
               having: Optional[str] = None
               ) -> List[tuple]:

        fields = fields if fields else ['*']

        query_str = 'SELECT ' + ', '.join(fields) + '\nFROM ' + table

        if joins:
            query_str += '\nJOIN ' + '\nJOIN '.join([
                tab + ' ON ' + rule for tab, rule in joins
            ])

        if where:
            query_str += '\nWHERE ' + where

        if group_by:
            query_str += '\nGROUP BY ' + ", ".join(group_by)

        if having:
            query_str += '\nHAVING ' + having

        if order_by:
            query_str += '\nORDER BY ' + ', '.join([
                f'{key} {option}' for key, option in order_by
            ])

        query_str += ';'
        print('Запрос:')
        print(query_str)
        self.__cursor.execute(query_str)
        return self.__cursor.fetchall()

    def __del__(self):
        if self.__connection is not None:
            self.__cursor.close()
            self.__connection.close()
            print('Соединение с БД закрыто!')
