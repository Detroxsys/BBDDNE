import pandas as pd
import datetime
import redis

class RDB:
    def __init__(self):
        self.db= redis.Redis(host='127.0.0.1', port=6379, db=0, charset="utf-8", decode_responses=True)
    
    def resetDataBase(self):
        self.db.flushdb()
        return 

    def empezarDia(self, restantes):
        self.resetDataBase()
        for index, row in restantes.iterrows():
            key= 'Productos:'+row[0]
            result= self.db.set(key, int(row[1]))
        return result

    def get_sobrantes(self, producto):
        key="Productos:"+producto
        result = self.db.get(key)
        return int(result)

    def producidos(self, producto, producido):
        key="Productos:"+producto
        result= self.db.set(key, self.get_sobrantes(producto)+producido)
        return result

    def comprados(self, producto, comprado):
        key="Productos:"+producto
        result= self.db.set(key, self.get_sobrantes(producto)-comprado)
        return result

    def gastosExtra(self, gastado, concepto, user):
        hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        key1='gastoExtra:Gasto:'
        key2='gastoExtra:Concepto:'
        key3='gastoExtra:Hora:'
        key4='gastoExtra:Usuario:'
        self.db.rpush(key1, gastado)
        self.db.rpush(key2, concepto)
        self.db.rpush(key3, hora)
        self.db.rpush(key4, user)
        return 

    def gastosExtraTotales(self):
        gastos= self.db.lrange('gastoExtra:Gasto:', 0, -1)
        return sum(map(int, gastos))

    def ingresosExtra(self, ingresado, concepto, user):
        hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        key1='ingresoExtra:Ingreso:'
        key2='ingresoExtra:Concepto:'
        key3='ingresoExtra:Hora:'
        key4='ingresoExtra:Usuario:'
        self.db.rpush(key1, ingresado)
        self.db.rpush(key2, concepto)
        self.db.rpush(key3, hora)
        self.db.rpush(key4, user)
        return

    def ingresosExtraTotales(self):
        gastos= self.db.lrange('ingresoExtra:Ingreso:', 0, -1)
        return sum(map(int, gastos))

    def dfIngresosExtra(self):
        tiempos=[]
        for i in self.db.lrange('ingresoExtra:Hora:', 0, -1):
            tiempos.append(datetime.strptime(i, "%Y-%m-%d %H:%M:%S"))
        ingdict={'Fecha': tiempos, 'Concepto':self.db.lrange('ingresoExtra:Concepto:', 0, -1), \
            'Ingreso': self.db.lrange('ingresoExtra:Ingreso:', 0, -1), 'Usuario': self.db.lrange('ingresoExtra:Usuario:', 0, -1)}
        ingdf=pd.DataFrame.from_dict(data=ingdict)
        return( ingdf)

    def dfGastosExtra(self):
        tiempos=[]
        for i in self.db.lrange('gastoExtra:Hora:', 0, -1):
            tiempos.append(datetime.strptime(i, "%Y-%m-%d %H:%M:%S"))
        gastdict= {'Fecha': tiempos, 'Concepto':self.db.lrange('gastoExtra:Concepto:', 0, -1), \
            'Costo': self.db.lrange('gastoExtra:Gasto:', 0, -1), 'Usuario': self.db.lrange('gastoExtra:Usuario:', 0, -1)}
        gastodf=pd.DataFrame.from_dict(data=gastdict)
        return(gastodf)

    def CerrarDia(self, restantes):
        productos=[]
        cantidad=[]
        for index, row in restantes.iterrows():
            productos.append(row[0])
            cantidad.append(int(self.get_sobrantes(row[0])))
        df=pd.DataFrame()
        df['Producto']=productos
        df['Cantidad']=cantidad
        return(df)