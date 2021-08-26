from var import Data_type as dt
from var import SQL_code
from mysql.connector import connect

class DB_query:
    
    def run_con(self, host      : str = "localhost",\
                      user      : str = "root",\
                      passwd    : str = "",
                      database  : str = "MySQL") -> None:
        self.cnn = connect(host = host, user = user, passwd = passwd, database = database)
        self.cur = self.cnn.cursor()
    
    def query(self, fil : dt.Query) -> list:
        sql_code = SQL_code(fil).text()
        self.cur.execute(sql_code)
        datos = self.cur.fetchall()
        if datos:
            return self.validar(datos, fil)
    
    def validar(self, datos : list, fil : dt.Query) -> list:
        status_permitidos = ['En_venta', 'Vendido', 'Pre_venta']
        resultado = list()
        for val in datos:
            inm = dt.Inmueble(dict(zip(SQL_code.keys, val)))
            if inm['status'] in fil['status'] \
                and inm['status'] in status_permitidos \
                and inm['city_name'] in fil['city'][0].upper():
                resultado.append(inm)
        return resultado

if __name__ == '__main__':
    buscador = DB_query()
    buscador.run_con("localhost", "root", "unicornio003", "habi")
    print(buscador.query(dt.Query(year = ['2000', '2003', '2001'],
                                  city = ['Abejorral'],
                                  status = ['En_venta', 'Vendido'])))
        