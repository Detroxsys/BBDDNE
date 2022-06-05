#Integrantes 
#Marcela Cruz Larios 
#Yeudiel Lara Moreno
#Pablo David Castillo del Valle


import Backend
import bcrypt #Debe instalarse !pip install bcrypt
import redis
import os
import pyshorteners  #Debe Instalarse !pip install pyshorteners
#from fun_ws_admin import consultar_intersección, consultar_lista_usuarios

clear = lambda: os.system('cls')
db = Backend.DB()
#db.resetDataBase()
Usuario = None
Admin = False
Options = [1, 2, 3]
categorias = ["Arte", "Ciencia", "Tecnología", "Entretenimiento", "Deportes"]


def clear():
    # for windows
    if os.name == 'nt':
        _ = os.system('cls')

    # for mac and linux
    else:
        _ = os.system('clear')


# Login y register de usuario
def register_user(username, password, flag=0):
    if Usuario:
        print(
            "Ya hay un usuario logueado debe cerrar sesión para crear un usuario nuevo"
        )
        return

    if not db.get_password(username):
        passwordcode = password.encode()
        sal = bcrypt.gensalt()
        password_hasheada = bcrypt.hashpw(passwordcode, sal)
        if flag:
            db.add_user(username, password_hasheada, is_admin=1)
            return 
        else:
            db.add_user(username, password_hasheada)
            clear()
            print("El usuario se registró exitosamente\n")
    elif flag==1:
        return
    else:
        print("Usuario ya registrado")
    return


def login_user(username, password):
    global Usuario
    if Usuario:
        print("Ya hay un usuario logueado")
        return
    if not db.get_password(username):
        print("El usuario no esta registrado")
        return
    tempUser = db.get_user(username)
    if bcrypt.checkpw(password.encode(), tempUser[b'password']):
        Usuario = username
        print("Ok, las contraseñas coinciden, usuario logueado")
    else:
        print("Contraseña incorrecta")
    return


def is_admin(username):
    global Usuario
    global Admin
    if Usuario:
        r = db.is_admin(username)
        if r.decode() == '1':
            Admin = True
        else:
            Admin = False
    return


def cerrar_sesion():
    global Usuario
    Usuario = None
    Admin = False
    return


#Acciones de usuario
#Acortar una URL
def ShortUrl(url):
    s = pyshorteners.Shortener()
    return (s.tinyurl.short(url))


#Añade una nueva URL
def RegUrl():
    print("Introduzca la URL que quiere acortar")
    url = input().strip()
    result = db.get_url_info(Usuario, url)
    while (result != {}):
        print("Ese Url ya ha sido acortado")
        print(result[b'short_url'].decode("utf8"))
        print("¿Desea salir?[y/n]")
        temp = input().strip()
        if (temp == "y"):
            return
        print("Introduzca la URL que quiere acortar")
        url = input().strip()
        result = db.get_url_info(Usuario, url)

    shurl = pyshorteners.Shortener().tinyurl.short(url)
    print("¿Desea que su URL sea pública? (y/n)")
    priv = input().strip()
    while (priv not in ["y", "n"]):
        print("Respuesta no válida")
        print("¿Desea que su URL sea pública? (y/n)")
        priv = input().strip()
    if priv == "y":
        priv = 1
    else:
        priv = 0

    print("Agregue su URL a una categoría")
    print(", ".join(categorias))
    cat = input().strip()
    while (cat not in categorias):
        print("Debe elegir una categoría válida")
        print("Agregue su URL a una categoría")
        print(", ".join(categorias))
        cat = input().strip()
    print("\nSu URL acortado es:\n" + shurl)
    db.add_url(Usuario, url, shurl, cat, priv)
    db.add_to_category(Usuario, cat, url)


#Cambia la categoría de una URL
def CatUrl():
    print("¿Que URL quieres editar?")
    url = input().strip()
    result = db.get_url_info(Usuario, url)
    while (result == {}):
        print("Ese Url no ha sido acortado")
        print("¿Desea salir?[y/n]")
        temp = input().strip()
        if (temp == "y"):
            return
        print("¿Que URL quieres editar?")
        url = input().strip()
        result = db.get_url_info(Usuario, url)
    print("La categoría de ese URL es:")
    print(db.get_url_info(Usuario, url)[b'category'].decode("utf8"))
    print("¿A que categoría desea cambiar?")
    print(", ".join(categorias))
    cat = input().strip()
    while (cat not in categorias):
        print("Debe elegir una categoría válida")
        print("¿A que categoría desea cambiar?")
        print(", ".join(categorias))
        cat = input().strip()
    print("Categoria cambiada")
    db.update_category(Usuario, cat, url)
    db.update_url_category(Usuario, url, cat)


#Cambio de privacidad Url
def PrivUrl():
    print("¿Que Url quieres editar?")
    url = input().strip()
    result = db.get_url_info(Usuario, url)
    while (result == {}):
        print("Ese Url no ha sido acortado")
        print("¿Desea salir?[y/n]")
        temp = input().strip()
        if (temp == "y"):
            return
        print("¿Que URL quieres editar?")
        url = input().strip()
        result = db.get_url_info(Usuario, url)
    priv = db.get_url_info(Usuario, url)[b'status'].decode("utf8")
    if (priv == "0"):
        priv = "Privado"
    else:
        priv = "Publico"
    print("Este Url es " + priv)
    print("¿A que categoría desea cambiar?[Publico/Privado]")
    rpriv = input().strip()
    while (rpriv not in ["Publico", "Privado"]):
        print("Debe elegir una opción válida")
        print("¿A que categoría desea cambiar?[Publico/Privado]")
        rpriv = input()
    if (rpriv == "Privado"):
        rpriv = 0
    else:
        rpriv = 1
    db.update_url_status(Usuario, url, rpriv)


# Funciones de wishlist
def consultar_wishlist(username):
    res = db.get_wishlist(username)
    if res == -1:
        print('Tu wishlist está vacía')
    elif res:
        print('Tu wishlist es:')
        for i in res:
            print(i.decode())
    else:
        print('Hubo un problema, vuelve a intentarlo.')
    return


def agregar_a_wishlist(username):
    print('Introduce el url que deseas añadir a la wishlist.')
    url = input().strip()
    result = db.get_url_info(Usuario, url)
    while (result == {}):
        print("Ese Url no ha sido acortado")
        print("¿Desea salir?[y/n]")
        temp = input().strip()
        if (temp == "y"):
            return
        print("¿Que URL quieres editar?")
        url = input().strip()
        result = db.get_url_info(Usuario, url)
    result = db.add_to_wishlist(username, url)
    if result:
        print('La URL \n{}\n se agregó exitosamente a tu wishlist'.format(url))
        return
    else:
        print('Hubo un problema, vuelve a intentarlo.')
    return


def eliminar_de_wishlist(username):
    wl = db.get_wishlist(username)
    if wl == -1:
        print("Tu wishlist está vacía")
        return
    print('Introduce el url que deseas eliminar de la wishlist.')
    url = input().strip()
    if url.encode() in wl:
        result = db.remove_from_wishlist(username, url)
        if result:
            print(
                'La URL \n{}\n se eliminó exitosamente de tu wishlist.'.format(
                    url))
            return
        else:
            print('Hubo un problema, vuelve a intentarlo.')
    else:
        print('La URL \n{}\n no está en tu wishlist.'.format(url))
    return


# Acciones de categorías
def consultar_categorias(username):
    print('Introduce la categoría que deseas consultar')
    print(", ".join(categorias))
    cat = input().strip()
    while (cat not in categorias):
        print("Debe elegir una categoría válida")
        print('Introduce la categoría que deseas consultar')
        print(", ".join(categorias))
        cat = input().strip()
    res = db.get_category(username, cat)
    if res == -1:
        print("Aún no añades ninguna URL a esta categoría")
    elif res:
        print("Las URLs en la categoría {} son:".format(cat))
        for i in res:
            print(i.decode())
    else:
        print('Hubo un problema, vuelve a intentarlo.')
    return


# Acciones de Admin
def consultar_lista_usuarios():
    res = db.get_users()
    if res:
        print('La lista de usuarios es la siguiente:')
        for i in res:
            print(i.decode())
        print("\n")
    else:
        print('Hubo en error, vuelve a intentarlo.')


def consultar_intersección():
    print('Introduce el primer nombre de usuario')
    user1 = input().strip()
    result = db.get_user(user1)
    while (result == {}):
        print("El usuario ingresado no existe.")
        print("¿Desea salir?[y/n]")
        temp = input().strip()
        if (temp == "y"):
            return
        print("Introduce el primer nombre de usuario")
        user1 = input().strip()
        result = db.get_user(user1)
    print('Introduce la categoría del usuario {} a consultar'.format(user1))
    print(", ".join(categorias))
    cat1 = input().strip()
    while (cat1 not in categorias):
        print("Debe elegir una categoría válida")
        print('Introduce la categoría que deseas consultar')
        print(", ".join(categorias))
        cat1 = input().strip()
    print('Introduce el segundo nombre de usuario')
    user2 = input().strip()
    result = db.get_user(user1)
    while (result == {}):
        print("El usuario ingresado no existe.")
        print("¿Desea salir?[y/n]")
        temp = input().strip()
        if (temp == "y"):
            return
        print("Introduce el primer nombre de usuario")
        user2 = input().strip()
        result = db.get_user(user1)
    print('Introduce la categoría del usuario {} a consultar'.format(user2))
    print(", ".join(categorias))
    cat2 = input().strip()
    while (cat1 not in categorias):
        print("Debe elegir una categoría válida")
        print('Introduce la categoría que deseas consultar')
        print(", ".join(categorias))
        cat2 = input().strip()

    res1 = db.get_category(user1, cat1)
    res2 = db.get_category(user2, cat2)

    if res1 == -1 or res2 == -1:
        print('La intersección de las categorias es vacía.')
        return
    else:
        res = db.get_cat_intersection(user1, user2, cat1, cat2)
        if res:
            print('La intersección de las categorias es:')
            for i in res:
                print(i.decode())
        else:
            print('Hubo un problema, vuelve a intentarlo.')

#Crear administrador por defecto en caso de que no exista. 
register_user("ADMIN", "123", flag=1)
while True:
    print(" Menú ")
    print("0. Cerrar Programa")
    print("1. Registrarse")
    print("2. Ingresar")

    if Usuario != None:
        print(f"Bienvenido {Usuario}")

    print("¿Qué accion desea realizar?")
    n = int(input())
    clear()
    if n not in Options:
        db.db.save()
        break
    if n == 1:
        username = input("Elija un nombre de usuario: ").strip()
        password = input("Elija una contraseña:").strip()
        register_user(username, password)
    elif n == 2:
        username = input("Ingrese nombre de usuario:").strip()
        password = input("Ingrese la contraseña:").strip()
        login_user(username, password)

    is_admin(username)
    if Usuario and not Admin:
        while True:
            print("Menú principal")
            print("1. URLS")
            print("2. Wishlist")
            print("3. Categorías")
            print("4. Cerrar sesión")
            a = int(input("Seleccione una opción\n"))
            clear()
            if a == 1:
                while True:
                    print("Acciones de URLS")
                    print("1. Añadir nueva URL y acortarla")
                    print("2. Administrar privacidad de urls")
                    print("3. Administrar categorías de urls")
                    print("4. Regresar al menú principal")
                    m = int(input("¿Qué accion desea realizar?\n"))
                    clear()
                    if m == 1:
                        RegUrl()
                    elif m == 2:
                        PrivUrl()
                    elif m == 3:
                        CatUrl()
                    elif m == 4:
                        break
            elif a == 2:
                while True:
                    print("Acciones de Wishlist")
                    print("1. Consultar Wishlist")
                    print("2. Añadir URL a Wishlist")
                    print("3. Eliminar URL de Wishlist")
                    print("4. Regresar al menú principal")
                    m = int(input("¿Qué accion desea realizar?\n"))
                    clear()
                    if m == 1:
                        consultar_wishlist(username)
                    elif m == 2:
                        agregar_a_wishlist(username)
                    elif m == 3:
                        eliminar_de_wishlist(username)
                    elif m == 4:
                        break
            elif a == 3:
                while True:
                    print("Acciones de categorías")
                    print("1. Consultar categoría")
                    print("2. Regresar al menú principal")
                    m = int(input("¿Qué accion desea realizar?\n"))
                    clear()
                    if m == 1:
                        consultar_categorias(username)
                    elif m == 2:
                        break
            elif a == 4:
                cerrar_sesion()
                break

    if Usuario and Admin:
        while True:
            print("Acciones de administrador:")
            print("1. Consultar lista de usuarios")
            print("2. Intersectar categorías de dos usuarios")
            print("3. Cerrar sesión")
            a = int(input("Seleccione una opción\n"))
            clear()
            if a == 1:
                consultar_lista_usuarios()

            elif a == 2:
                consultar_intersección()

            elif a == 3:
                cerrar_sesion()
                break
