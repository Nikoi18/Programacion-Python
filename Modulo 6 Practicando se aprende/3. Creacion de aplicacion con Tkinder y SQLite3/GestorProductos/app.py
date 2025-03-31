import sqlite3
from idlelib.colorizer import color_config
from tkinter import ttk
from tkinter import *
from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects import sqlite
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import db
from db import session

"""class Producto(db.Base):
    __tablename__ = "producto"
    __table_args__ = {"sqlite_autoincrement": True}
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    precio = Column(Integer, nullable=False)
    categoria = Column(String(50), nullable=False)
    cantidad = Column(Integer, nullable=False)"""

class VentanaPrincipal():
    db = "database/productos.db"


    def __init__(self, root):

        #self.engine = create_engine('sqlite:///database/productos.db')
        #self.Session = sessionmaker(bind=self.engine)

        self.ventana = root #se cambia la variable root a ventana
        self.ventana.title("App Gestor de Productos") #titulo de la ventana
        self.ventana.resizable(1,1) #activa la redimension de la ventana
        self.ventana.wm_iconbitmap("recursos/principal.ico") #icono de la ventana




        #Creamos el contenedor principal(frame) se puede crear varios contenedore donde se puede
        #almacenar varios widget dentro de un frame
        frame = LabelFrame(self.ventana, text="Registrar un nuevo Producto") #le pasamos la variable self.ventana y le colocamos el titulo
        frame.grid(row=0, column=0, pady=0, columnspan=10)#ubicacion de donde estara el frame fila 0, columna 0 con un margen de 20 y ocupa la columna 1,2 y 3

        #Label Nombre
        self.etiqueta_nombre = Label(frame, text="Nombre: ") #se crea la etiqueta nombre
        self.etiqueta_nombre.grid(row=1, column=0) #ubicacion de la etiqueta


        #Entry caja donde se coloca le informacion
        self.nombre = Entry(frame)
        self.nombre.grid(row=1, column=1)
        self.nombre.focus()


        #Label Precio
        self.etiqueta_precio = Label(frame, text="Precio: ")#se crea la etiqueta precio
        self.etiqueta_precio.grid(row=2, column=0)#ubicacion de la etiqueta

        #entry precio
        self.precio = Entry(frame)
        self.precio.grid(row=2, column=1)

        #Label Categoria
        self.etiqueta_categoria = Label(frame, text="Categoria: ")
        self.etiqueta_categoria.grid(row=3, column=0)

        #Entry Categoria

        self.categoria = Entry(frame)
        self.categoria.grid(row=3, column=1)

        #Label Cantidad
        self.etiqueta_cantidad = Label(frame, text="Cantidad: ")
        self.etiqueta_cantidad.grid(row=4, column=0)

        #Entry Candidad
        self.cantidad= Entry(frame)
        self.cantidad.grid(row=4, column=1)


        # Boton añadir producto
        self.boton_aniadir = ttk.Button(frame, text="Guardar Producto",command=self.add_producto)
        self.boton_aniadir.grid(row=5, columnspan=4, sticky=W + E) #se fuerza con sticky la ocupacion que usara el grid mediante coordenada n,s,e,o

        # Boton Oscuro
        self.modo_oscuro = ttk.Button(frame, text="Oscuro", command=self.modo_oscuro)
        self.modo_oscuro.grid(row=3, column=4)



        # Boton Claro
        self.modo_claro = ttk.Button(frame, text="CLaro", command=self.modo_claro)
        self.modo_claro.grid(row=2, column=4)

        # Mensaje informativo para el usuario
        self.mensaje = Label(text='', fg='red', anchor=CENTER)
        self.mensaje.grid(row=4, column=0, columnspan=5, pady=0, sticky=W + E)

        # Tabla de Productos
        # Estilo personalizado para la tabla
        style = ttk.Style() #se define al odjeto quien tendra el estilo
        style.configure("mystyle.Treeview", higlightthickness=0, bd=0, background="#fcfcfc",
                        font=('Calibri', 11, 'bold'))  # se modifica la fuente de la tablaç
        style.configure("mystyle.Treeview.Heading", background="#fcfcfc",
                        font=('Calibri', 12, 'bold' ))  # Se modifica la uente de las cabeceras
        style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})])

        # Estructura de la tabla
        self.tabla = ttk.Treeview(height=20, columns=("0","1","2"), style="mystyle.Treeview")
        self.tabla.grid(row=5, column=0, columnspan=2)
        self.tabla.heading('#0', text='NOMBRE', anchor=CENTER)  # Encabezado 0
        self.tabla.heading('#1', text='PRECIO', anchor=CENTER)  # Encabezado 1
        self.tabla.heading('#2', text='CATEGORIA', anchor=CENTER) #Encabezado 2
        self.tabla.heading('#3', text='STOCK', anchor=CENTER) #Encabezado 3

        self.boton_eliminar = ttk.Button(text='ELIMINAR', command=self.del_producto)
        self.boton_eliminar.grid(row=6, column=0, sticky=W + E)
        self.boton_editar = ttk.Button(text='EDITAR', command=self.edit_producto)
        self.boton_editar.grid(row=6, column=1, sticky=W + E)

        self.get_productos()

    def modo_oscuro(self):
        self.ventana.config(background="#4a4a4a")
        self.tabla.config()


    def modo_claro(self):
        self.ventana.config(background="#fcfcfc")


    def db_consulta(self, consulta, parametros=()):

       with sqlite3.connect(self.db) as con:
            cursor = con.cursor()
            resultado = cursor.execute(consulta, parametros)
            con.commit()
       return resultado
           #session = self.Session()
           #try:
           #    resultado=session.query(consulta, parametros)
            #   session.commit()
             #  return resultado
           #finally:
            #   session.close()


    def get_productos(self):

        registros_tabla = self.tabla.get_children()
        for fila in registros_tabla:
            self.tabla.delete(fila)

        #query= db.session.query(Producto).order_by("nombre").all()
        query = "SELECT * FROM producto ORDER BY nombre DESC"
        registros = self.db_consulta(query)
        for fila in registros:
            print (fila)
            self.tabla.insert("", 0,text=fila[1], values=fila[2:])
    def validacion_nombre(self):
        return self.nombre.get().strip() != ""

    def validacion_precio(self):
        try:
            precio = float(self.precio.get())
            return precio > 0
        except ValueError:
            return False

    def validacion_categoria(self):
        return self.categoria.get().strip() != ""

    def validacion_cantidad(self):
        try:
            cantidad = int(self.cantidad.get())
            return cantidad > 0
        except ValueError:
            return False


    def add_producto(self):

        if not self.validacion_nombre():
            print("El nombre es obligatorio")
            self.mensaje['text'] = 'El nombre es oligatorio y no puede estar vacio'
            return
        if not self.validacion_precio():
            print("El Precio es obligatorio")
            self.mensaje['text'] = 'El precio es obligatorio y debe ser un numero valido mayor que 0'
            return
        if not self.validacion_categoria():
            print("La categoria es obligatorio")
            self.mensaje['text'] = 'La Categoria es oligatorio y no puede estar vacio'
            return
        if not self.validacion_cantidad():
            print("La cantidad es obligatorio")
            self.mensaje['text'] = 'La cantidad es obligatorio y debe ser un numero valido mayor que 0'
            return



        query = 'INSERT INTO producto VALUES(NULL, ?, ?,?,?)'
        parametros = (self.nombre.get(), self.precio.get(), self.categoria.get(), self.cantidad.get())
        self.db_consulta(query, parametros)
        print("Datos Guardados")
        self.mensaje['text'] = 'producto {} añadido con exito'.format(self.nombre.get())
        self.nombre.delete(0, END) #Borrar el campo nombre del formulario
        self.precio.delete(0, END) #Borrar el campo precio del formulario
        self.categoria.delete(0, END)
        self.cantidad.delete(0, END)
        #print(self.nombre.get())
        #print(self.precio.get())

        self.get_productos()

    def del_producto(self):
        # print(self.tabla.item(self.tabla.selection()))
        #print(self.tabla.item(self.tabla.selection())['text'])
        # print(self.tabla.item(self.tabla.selection())['values'])
        #print(self.tabla.item(self.tabla.selection())['values'][0])

        self.mensaje['text'] = '' # Mensaje inicialmente vacio
        # Comprobacion de que se seleccione un procuto para poder eliminarlo
        try:
            self.tabla.item(self.tabla.selection())['text'][0]
        except IndexError as e:
            self.mensaje['text'] = 'Por favor, seleccione un producto'
            return

        self.mensaje['text'] = ''
        nombre = self.tabla.item(self.tabla.selection())['text']
        query = 'DELETE FROM producto WHERE nombre = ?' # Consulta SQL
        self.db_consulta(query,(nombre,)) #Ejecutar la consulta
        self.mensaje['text'] = 'Producto {} eliminado con exito'.format(nombre)
        self.get_productos() #actualizar la tabla de productos

    def edit_producto(self):
        try:
            nombre = self.tabla.item(self.tabla.selection())['text']
            precio = self.tabla.item(self.tabla.selection())['values'][0]
            categoria = self.tabla.item(self.tabla.selection())['values'][1]
            cantidad = self.tabla.item(self.tabla.selection())['values'][2]
            VentanaEditarProducto(self, nombre, precio,categoria, cantidad, self.mensaje)
        except IndexError:
            self.mensaje['Text'] = 'Por favor, seleccione un producto'

class VentanaEditarProducto():

    def __init__(self, ventana_principal, nombre, precio, categoria, cantidad, mensaje):
        self.ventana_principal = ventana_principal
        self.nombre = nombre
        self.precio = precio
        self.categoria = categoria
        self.cantidad = cantidad
        self.mensaje = mensaje


        self.ventana_editar = Toplevel()
        self.ventana_editar.title("Editar Producto")

        # Creacion del contenedor Frame para la edicion del producto
        frame_ep = LabelFrame(self.ventana_editar, text="Editar el siguiente producto", font=('Calibri',16, 'bold'))
        frame_ep.grid(row=0, columnspan=10, pady=20, padx=20)

        #Label y entry para el Nombre antiguo (solo lectura)
        Label(frame_ep, text="Nombre antiguo: ", font=('Calibri', 13)).grid(row=1, column=0)
        Entry(frame_ep, textvariable=StringVar(self.ventana_editar, value=nombre), state='readonly', font=('Calibri', 13)).grid(row=1, column=1)

        #Label y Entry para el Nombre nuevo
        Label(frame_ep, text="Nombre nuevo: ", font=('Calibri', 13)).grid(row=2, column=0)
        self.input_nombre_nuevo = Entry(frame_ep, font=('Calibri', 13))
        self.input_nombre_nuevo.grid(row=2, column=1)
        self.input_nombre_nuevo.focus()

        # Precio antiguo (solo lectura)
        Label(frame_ep, text="Precio antiguo: ", font=('Calibri', 13)).grid(row=3, column=0)
        Entry(frame_ep, textvariable=StringVar(self.ventana_editar, value=precio), state='readonly', font=('Calibri', 13)).grid(row=3, column=1)

        # Precio nuevo
        Label(frame_ep, text="Precio nuevo: ", font=('Calibri', 13)).grid(row=4, column=0)
        self.input_precio_nuevo = Entry(frame_ep, font=('Calibri', 13))
        self.input_precio_nuevo.grid(row=4, column=1)

        #Categoria Antigua
        Label(frame_ep, text="Categoria antigua: ", font=('Calibri', 13)).grid(row=5, column=0)
        Entry(frame_ep, textvariable=StringVar(self.ventana_editar, value=categoria), state='readonly', font=('Calibri', 13)).grid(row=5, column=1)
        #Categoria nueva
        Label(frame_ep, text="Nueva categoria: ", font=('Calibri', 13)).grid(row=6, column=0)
        self.input_categoria_nuevo = Entry(frame_ep, font=('Calibri', 13))
        self.input_categoria_nuevo.grid(row=6, column=1)

        #Cantidad antigua
        Label(frame_ep, text="Cantidad antigua: ", font=('Calibri', 13)).grid(row=7, column=0)
        Entry(frame_ep, textvariable=StringVar(self.ventana_editar, value=cantidad), state='readonly', font=('Calibri', 13)).grid(row=7, column=1)
        #Cantidad Nueva
        Label(frame_ep, text="Cantidad nueva: ", font=('Calibri', 13)).grid(row=8, column=0)
        self.input_cantidad_nuevo = Entry(frame_ep, font=('Calibri', 13))
        self.input_cantidad_nuevo.grid(row=8, column=1)



        # Boton Actualizar
        self.boton_actualizar = ttk.Button(frame_ep, text="Actualizar Producto", command=self.actualizar)
        self.boton_actualizar.grid(row=9, columnspan=2, sticky=W+E)



    def actualizar(self):
        nuevo_nombre = self.input_nombre_nuevo.get() or self.nombre
        nuevo_precio = self.input_precio_nuevo.get() or self.precio
        nuevo_categoria = self.input_categoria_nuevo.get() or self.categoria
        nuevo_cantidad = self.input_cantidad_nuevo.get() or self.cantidad

        if nuevo_nombre and nuevo_precio and nuevo_categoria and nuevo_cantidad:
            query = 'UPDATE producto SET nombre = ?, precio = ?, categoria = ?, cantidad = ? WHERE nombre = ?'
            parametros = (nuevo_nombre, nuevo_precio, nuevo_categoria, nuevo_cantidad, self.nombre)
            self.ventana_principal.db_consulta(query, parametros)
            self.mensaje['text'] = f'El producto {self.nombre} ha sido actualizado con exito'
        else:
            self.mensaje['text'] = f'No se pudo actualizar el producto {self.nombre}'

        self.ventana_editar.destroy()
        self.ventana_principal.get_productos()




if __name__ == "__main__":
    root = Tk() # Instancia de la ventana principal
    app = VentanaPrincipal(root) # Enviamos y cedemos el control a la clase
    #db.Base.metadata.create_all(bind=db.engine)
    root.mainloop()
