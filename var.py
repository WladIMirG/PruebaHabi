from typing import TypedDict

class Data_type:
    class Adapter(TypedDict, total=False):
        host: str
        port: int
        
    class Inmueble(TypedDict, total=False):
        pass

    class Query(TypedDict, total=False):
        year    : str
        city    : str
        status  : str

class SQL_code:
    l       : list = ['FROM municipios m',
                      'inner',
                      'JOIN inmuebles i',
                      'ON m.id = i.City_code']
    keys    : list = ("adress","city_name","city_code","status","price","descrip")
    
    def __init__(self, query : Data_type.Query) -> None:
            self.query = query
    
    def text(self) -> str:
        l = ['SELECT',
             ', '.join(self.keys),
             ' '.join(self.l),
             'WHERE',
             self.city() if self.city() else '',
             'OR',
             self.year() if self.year() else '',
             'OR',
             self.status() if self.status() else '',
             ';']
        l = ' '.join(l)
        return ' '.join(l.split())
    
    def city(self) -> str:
        try:
            t = 'm.city_name = '
            a = [' '.join([t, '"'+i+'"']) for i in self.query['city']]
            return ' AND '.join(a)
        except KeyError:
            return None
        
    def year(self) -> str:
        try:
            t = 'i.Year ='
            a = [' '.join([t, i]) for i in self.query['year']]
            return ' AND '.join(a)
        except KeyError:
            return None

    def status(self) -> str:
        try:
            t = 'i.Status = '
            a = [' '.join([t, '"'+i+'"']) for i in self.query['status']]
            return ' AND '.join(a)
        except KeyError:
            return None

    
    