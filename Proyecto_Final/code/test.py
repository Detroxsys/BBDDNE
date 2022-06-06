from numpy import product
import mysql_queries as db_mysql

products = db_mysql.get_all_productos()
products_names = products['nombre'].to_list()
products_redis = products[['nombre', 'cantidad_disp']].copy()
products_price = products.set_index('nombre')
products_price = products_price['precio_unit'].to_dict()

print(products_names)
print(products_redis)
print(products_price)
