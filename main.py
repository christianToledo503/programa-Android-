# -*- coding: utf-8 -*-
# En ocasiones el widget TextInput muestra un error para
# solucionar instala xclip 
# $ sudo apt-get install xclip
import kivy
import os
import sqlite3
import mysql.connector
from kivy.config import Config
Config.set("graphics","width","340")
Config.set("graphics","hight","640")

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.label import Label 
from kivy.uix.screenmanager import ScreenManager, Screen 
from kivy.uix.screenmanager import FadeTransition
from kivy.properties import StringProperty
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.lang import Builder
#para el escaner#
import cv2
import numpy as np
from pyzbar.pyzbar import decode
from kivy.clock import Clock
import time
import pygame
from kivy.uix.checkbox import CheckBox
from kivy.clock import Clock
from kivy.uix.textinput import TextInput
from kivy.graphics import Color, Rectangle
from kivy.animation import Animation
from kivy.lang import Builder
from kivy.uix.gridlayout import GridLayout
from kivy.properties import BooleanProperty
from kivy.uix.behaviors import DragBehavior
from kivy.properties import NumericProperty
from kivy.animation import Animation
from kivy.uix.widget import Widget
from babel.numbers import format_number
import locale
#################
from kivy.lang import Builder


######3
def connect_to_database(host, username, password, database):
    try:
        # Establecer la conexión a la base de datos
        con = mysql.connector.connect(
            host=host,
            user=username,
            password=password,
            database=database
        )
        print("¡Conexión exitosa a la base de datos!")
        return con
    except mysql.connector.Error as e:
        print("Error al conectarse a la base de datos:", e)
        return None

# Configuración de la conexión
host = '149.50.138.155'  # Dirección IP del servidor de la base de datos
username = 'marcelo1234'  # Usuario de la base de datos
password = '1234'  # Contraseña de la base de datos
database = 'clientes'  # Nombre de la base de datos

# Intentar conectar a la base de datos
conexion = connect_to_database(host, username, password, database)

# Si la conexión fue exitosa, puedes ejecutar consultas SQL, etc.
#if conexion:
    # Por ejemplo, crear un cursor para ejecutar consultas
#    cursor = conexion.cursor()
    # Ejecutar una consulta
#    cursor.execute("SELECT * FROM producto")
    # Obtener los resultados
#    resultados = cursor.fetchall()
    # Hacer algo con los resultados
#    print(resultados)
    # Cerrar la conexión cuando hayas terminado
    #conexion.close()

class MessagePopup(Popup):
    pass

class MainWid(ScreenManager):
    def __init__(self,**kwargs):
        super(MainWid,self).__init__()
        self.APP_PATH = os.getcwd()
        
        self.StartWid = StartWid(self)
        self.DataBaseWid = DataBaseWid(self)
        self.InsertDataWid = BoxLayout()
        self.UpdateDataWid = BoxLayout()
        self.Popup = MessagePopup()
        self.CarritoWid = CarritoWid(self)
        
        self.conexion = conexion
        

        wid = Screen(name='start')
        wid.add_widget(self.StartWid)
        self.add_widget(wid)

        wid = Screen(name='database')
        wid.add_widget(self.DataBaseWid)
        self.add_widget(wid)

        wid = Screen(name='insertdata')
        wid.add_widget(self.InsertDataWid)
        self.add_widget(wid)
        
        wid = Screen(name='updatedata')
        wid.add_widget(self.UpdateDataWid)
        self.add_widget(wid)

        wid = Screen(name='carrito')
        wid.add_widget(self.CarritoWid)
        self.add_widget(wid)
        self.goto_start()   
        


    def goto_carrito(self):
        #self.CarritoWid.check_memory()
        #if hasattr(self.ids, 'container'):
        #    self.ids.container.clear_widgets() 
        self.current = 'carrito'



    def goto_start(self):
        self.current = 'start'

        
    def goto_database(self):
        self.DataBaseWid.check_memory()
        self.current = 'database'
        #self.DataBaseWid.go_to_bottom()

    def goto_insertdata(self):
        self.InsertDataWid.clear_widgets()
        wid = InsertDataWid(self)
        self.InsertDataWid.add_widget(wid)
        self.current = 'insertdata'

    def goto_updatedata(self,data_id):
        self.UpdateDataWid.clear_widgets()
        wid = UpdateDataWid(self,data_id)
        self.UpdateDataWid.add_widget(wid)
        self.current = 'updatedata'


class CarritoWid(BoxLayout):
    
    data_widget = ObjectProperty(None)
    def __init__(self, mainwid, **kwargs):
        super(CarritoWid, self).__init__()
        self.mainwid = mainwid
        self.productos_en_carrito = []
        self.last_scan_time = {}
        self.total = 0
        self.counter = 0  # Inicializamos el contador
        self.DataWid2 = DataWid2(self.mainwid)
        #Builder.load_string(producto)
        total = NumericProperty(0)  # Agrega la propiedad total
        self.vector = {}
        self.conexion = conexion
        
    def on_widget_touch_down(self, instance, touch):
        if touch.is_double_tap:  # Verificar si es un doble clic
            if instance.collide_point(*touch.pos):  # Verificar si el toque está dentro del widget
                 
                self.ids.container.remove_widget(instance)
                # Llamar al método disminuir_cantidad_cero de DataWid2
                if hasattr(instance, 'disminuir_cantidad_cero'):
                    instance.disminuir_cantidad_cero()   
    
    def check_memory(self):
        
        # Inicializamos el total en 0
        con = connect_to_database(host, username, password, database)
        cursor = con.cursor()
        termino_busqueda = self.ids.ti_ingresar.text.strip().lower()

        if termino_busqueda:
            query = 'SELECT codigo, producto, costo, precio, cantidad, imagen FROM producto WHERE codigo = %s'
            cursor.execute(query, (termino_busqueda,))
        else:
            query = 'SELECT codigo, producto, costo, precio, cantidad, imagen FROM producto'
            cursor.execute(query)

        for i in cursor:
            
            wid = DataWid2(self.mainwid)
            r1 = 'Código: ' + str(i[0]) + '\n'
            r2 = str(i[1]) + '\n'
            r3 = 'Precio: ' + '$' + str(i[3]) + '\n'
            
            wid.precio_inv=i[3] # precio individual
            self.total += i[3] # Acumulamos el valor de i[3] al total

            self.vector.update({i[0]:i[3]})


            wid.data_id = str(i[0])
            wid.data = r1 + r2 + r3
            wid.data_imagen = i[5]
            #print(wid.precio_inv)
            wid.bind(on_touch_down=self.on_widget_touch_down)
            self.ids.container.add_widget(wid)
            print(self.vector)
            
            

        con.close()
        

    def go_to_bottom(self):
        # Obtiene la instancia del ScrollView y realiza el scroll al final
        scroll_view = self.ids.container.parent
        scroll_view.scroll_y = 0

    def agregar(self):
        # Verifica si el TextInput (id_ingresar) está vacío
        if not self.ids.ti_ingresar.text.strip():
            # Si está vacío, no hagas nada
            return
        pygame.mixer.init()
        self.sonido = pygame.mixer.Sound("beep.mp3")
        self.sonido.play()
        # Si no está vacío, llama a la función check_memory
        self.check_memory()
        self.go_to_bottom()
        # Limpiar el TextInput (ti_ingresar)
        self.ids.ti_ingresar.text = ""

        self.actualizar_total()
        
    
    def hacer_foco_en_textinput(self):
        # Asegúrate de importar el módulo adecuado (puede variar según tu estructura de archivos)
        # from kivy.uix.textinput import TextInput

        # Reemplaza 'self.ids.ti_ingresar' con tu identificador real
        ti_ingresar = self.ids.ti_ingresar if hasattr(self.ids, 'ti_ingresar') else None

        if ti_ingresar and isinstance(ti_ingresar, TextInput):
            ti_ingresar.focus = True
    

      # Diccionario para almacenar el tiempo del último escaneo de cada código

    def escanear(self):
        # Cambia el índice de la cámara si es necesario
        cap = cv2.VideoCapture(0)

        # Ancho de la cámara
        cap.set(3, 160)
        cap.set(4, 120)

        # Leer credenciales.txt
        with open('credenciales.txt') as f:
            # Lee y separa en un arreglo los datos 
            mydatalist = f.read().splitlines()

        # Variable para controlar el tiempo entre escaneos
        tiempo_anterior = time.time()

        while True:
            success, img = cap.read()

            if not success:
                print("Error: No se pudo leer el fotograma.")
                break

            # Verifica si la decodificación fue exitosa
            decoded_objects = decode(img)

            for barcode in decoded_objects:
                mydata = barcode.data.decode('utf-8')
                print(mydata)

                # Verifica si el código ya ha sido escaneado recientemente
                if mydata in self.last_scan_time:
                    tiempo_actual = time.time()
                    tiempo_transcurrido = tiempo_actual - self.last_scan_time[mydata]

                    # Si ha pasado menos de 0.5 segundos desde el último escaneo, ignora este escaneo
                    if tiempo_transcurrido < 0.5:
                        continue

                # Si el código no ha sido escaneado recientemente, actualiza su tiempo de escaneo
                self.last_scan_time[mydata] = time.time()

                # Realiza las acciones necesarias con el código escaneado
                # Por ejemplo, copiar el código escaneado al TextInput (ti_ingresar) y luego llamar al método agregar()
                self.ids.ti_ingresar.text = mydata
                self.agregar()

                # Definir el color para dibujar el polígono
                color = (0, 255, 0)  # Color verde

                # Coordenada del barcode    
                pts = np.array([barcode.polygon], np.int32)
                pts = pts.reshape((-1, 1, 2))

                cv2.polylines(img, [pts], True, color, 5)  # Dibuja el polígono

                # Muestra el resultado en la esquina superior izquierda
                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(img, mydata, (10, 30), font, 1, color, 2, cv2.LINE_AA)

            cv2.imshow('Result', img)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Liberar la cámara y cerrar las ventanas
        cap.release()
        
    def actualizar_total(self):
        
        self.ids.label_total.text = f'$ {self.formatear_numero(float(self.total))}'
        
    ##################### formaterar número #############

    def formatear_numero(self,numero):
        locale.setlocale(locale.LC_ALL, 'es_ES.UTF-8')
        #return format_number(numero, locale='es',format='0.00')
        return locale.format_string("%.2f", numero, grouping=True) 
    #####################################################
 
    
class StartWid(BoxLayout):
    def __init__(self,mainwid,**kwargs):
        super(StartWid,self).__init__()
        self.mainwid = mainwid
        
    def create_database(self):
        self.conexion = conexion
        self.mainwid.goto_database()
     
    def go_to_carrito(self):
        self.mainwid.goto_carrito()

class DataBaseWid(BoxLayout):

    def __init__(self,mainwid,**kwargs):
        super(DataBaseWid,self).__init__()
        self.mainwid = mainwid
        ti_busca = self.ids.ti_busca
        ti_busca.font_size = 24 
        ti_busca.bind(text=self.on_search_text_change)
        self.conexion = conexion
    

    ##################### formaterar número #############

    def formatear_numero(self,numero):
        locale.setlocale(locale.LC_ALL, 'es_ES.UTF-8')
        #return format_number(numero, locale='es',format='0.00')
        return locale.format_string("%.2f", numero, grouping=True) 
    #####################################################



    def go_to_bottom(self):
        # Obtiene la instancia del ScrollView y realiza el scroll al final
        scroll_view = self.ids.container.parent
        scroll_view.scroll_y = 0

    def goto_start(self):
        self.parent.goto_start()

    def on_search_text_change(self, instance, value):
        # Aquí puedes manejar el cambio de texto en el TextInput
        # El parámetro 'value' contiene el nuevo texto
        termino_busqueda = value
        self.filter_widgets(termino_busqueda)

    def get_all_widgets_method1(self):
        # Implementa esta función para recuperar todos los widgets originales
        # Asegúrate de tener correctamente implementada esta función
        all_widgets = [widget for widget in self.ids.container.children]
        return all_widgets

    def filter_widgets(self, termino_busqueda):
        widgets_a_eliminar = []

        # Verifica si el término de búsqueda está vacío o contiene solo espacios en blanco
        if not termino_busqueda.strip():
            # Si está vacío, recupera todos los widgets
            all_widgets = self.get_all_widgets_method1()
            print("Recuperando todos los widgets:", all_widgets)
            for widget in all_widgets:
                widget.opacity = 1
        else:
            # Realiza la búsqueda y la eliminación de widgets
            for widget in self.ids.container.children:
                # Verifica si el widget tiene un atributo 'data'
                if hasattr(widget, 'data') and termino_busqueda.lower() in widget.data.lower():
                    widget.opacity = 1  # Hace que el widget sea visible
                else:
                    widget.opacity = 0  # Oculta el widget
                    widgets_a_eliminar.append(widget)

            # Elimina los widgets que no cumplen con las condiciones
            for widget in widgets_a_eliminar:
                self.ids.container.remove_widget(widget)

    def on_search_text_change(self, instance, value):
        termino_busqueda = value.strip().lower()

        if not termino_busqueda:  # Verifica si el término de búsqueda está vacío
            self.check_memory()  # Recarga todos los widgets originales
        else:
            self.filter_widgets(termino_busqueda)        

    



    def go_to_bottom(self):
        # Obtiene la instancia del ScrollView y realiza el scroll al final
        scroll_view = self.ids.container.parent
        scroll_view.scroll_y = 0
        ###########
    
    def check_memory(self):
        self.ids.container.clear_widgets()
        con = connect_to_database(host, username, password, database)
        cursor = con.cursor()
        cursor.execute('select codigo, producto, costo, precio, cantidad, imagen from producto')
        for i in cursor:
            wid = DataWid(self.mainwid)
            r1 = 'Código: '+str(i[0]) +'\n'
            r2 = str(i[1]) + '\n'
            r3 = 'Precio: '+'$'+ str(i[3])+'\n'
            r4 = 'stock: '+ str(i[4])
            wid.data_id = str(i[0])

            wid.data = r1+r2+r3+r4
            wid.data_imagen= i[5]
            self.ids.container.add_widget(wid)
        wid = NewDataButton(self.mainwid)
        self.ids.container.add_widget(wid)
        con.close()
        

class UpdateDataWid(BoxLayout):
    def __init__(self,mainwid,data_id,**kwargs):
        super(UpdateDataWid,self).__init__()
        self.mainwid = mainwid
        self.data_id = data_id
        self.check_memory()


    ##################### formaterar número #############

    def formatear_numero(self,numero):
        locale.setlocale(locale.LC_ALL, 'es_ES.UTF-8')
        #return format_number(numero, locale='es',format='0.00')
        return locale.format_string("%.2f", numero, grouping=True) 
    #####################################################


    def check_memory(self):
        #con = sqlite3.connect(self.mainwid.DB_PATH)
        con = connect_to_database(host, username, password, database)
        cursor = con.cursor()
        s = 'SELECT codigo, producto, costo, precio, cantidad, imagen FROM producto WHERE codigo='
        cursor.execute(s + self.data_id)
        for i in cursor:
            self.ids.ti_codigo.text = str(i[0])  # Considerando que id es el primer campo
            self.ids.ti_producto.text = str(i[1])
            self.ids.ti_costo.text = str(i[2])
            self.ids.ti_precio.text = str(i[3])
            self.ids.ti_cantidad.text = str(i[4])
            self.ids.ti_imagen.text = str(i[5])
        con.close()

    

    def update_data(self):
        con = connect_to_database(host, username, password, database)
        cursor = con.cursor()
        d0 = self.ids.ti_codigo.text
        d1 = self.ids.ti_producto.text
        d2 = self.ids.ti_costo.text
        d3 = self.ids.ti_precio.text
        d4 = self.ids.ti_cantidad.text
        d5 = self.ids.ti_imagen.text
        a1 = (d0, d1, d2, d3, d4, d5)
        s1 = 'UPDATE producto SET'
        s2 = 'codigo=%s, producto="%s", costo=%s, precio=%s, cantidad=%s, imagen="%s" ' % a1
        s3 = 'WHERE codigo=%s' % self.data_id  # Cambiar de codigo a id
        try:
            cursor.execute(s1 + ' ' + s2 + ' ' + s3)
            con.commit()
            con.close()
            self.mainwid.goto_database()
        except Exception as e:
            message = self.mainwid.Popup.ids.message
            self.mainwid.Popup.open()
            self.mainwid.Popup.title = "Data base error"
            if '' in a1:
                message.text = 'Uno o más campos están vacíos'
            else:
                message.text = str(e)
            con.close()
        

    def delete_data(self):
        con = connect_to_database(host, username, password, database)
        cursor = con.cursor()
        s = 'delete from producto where codigo='+self.data_id
        cursor.execute(s)
        con.commit()
        con.close()
        self.mainwid.goto_database()
        #self.DataBaseWid.go_to_bottom()

    def back_to_dbw(self):
        self.mainwid.goto_database()

class InsertDataWid(BoxLayout):
    def __init__(self,mainwid,**kwargs):
        super(InsertDataWid,self).__init__()
        self.mainwid = mainwid

    def insert_data(self):
        con = connect_to_database(host, username, password, database) 
        cursor = con.cursor()
        d1 = self.ids.ti_codigo.text
        d2 = self.ids.ti_producto.text
        d3 = self.ids.ti_costo.text
        d4 = self.ids.ti_precio.text
        d5 = self.ids.ti_cantidad.text
        d6 = self.ids.ti_imagen.text
        a1 = (d1,d2,d3,d4,d5,d6)
        s1 = 'INSERT INTO producto(codigo, producto, costo, precio, cantidad, imagen)'
        s2 = 'VALUES(%s,"%s",%s,%s,%s,"%s")' % a1
        try:
            cursor.execute(s1+' '+s2)
            con.commit()
            con.close()
            self.mainwid.goto_database()
        except Exception as e:
            message = self.mainwid.Popup.ids.message
            self.mainwid.Popup.open()
            self.mainwid.Popup.title = "Data base error"
            if '' in a1:
                message.text = 'Uno o más campos están vacíos'
            else: 
                message.text = str(e)
            con.close()

    def back_to_dbw(self):
        self.mainwid.goto_database()
    
class DataWid(BoxLayout):
    def __init__(self,mainwid,**kwargs):
        super(DataWid,self).__init__()
        self.mainwid = mainwid
        
    def update_data(self,data_id):
        self.mainwid.goto_updatedata(data_id)

class DataWid2(BoxLayout):
    swipe_threshold = NumericProperty(100)
    id_cantidad = ObjectProperty()

    def __init__(self,mainwid,**kwargs):
        super(DataWid2,self).__init__()
        self.mainwid = mainwid
        self.precio_inv = 0
    
    def update_data(self,data_id):
        self.mainwid.goto_updatedata(data_id)
    
    def eliminar_widget(self):
        # Elimina este widget del contenedor principal
        if self.data_id:
            self.mainwid.remove_widget_by_id(self.data_id)
    
    def checkbox_checked(self, active):
        if active:
            print("CheckBox está marcado")
        else:
            print("CheckBox está desmarcado")

    def toggle_checkbox(self, checkbox):
        checkbox.active = True
        Clock.schedule_once(lambda dt: setattr(checkbox, 'active', False), 0.2)  # Desactivar después de 500 milisegundos
     

    def on_checkbox_active(self, checkbox, value):
        if value:
            self.incrementar_cantidad()
            self.toggle_checkbox(checkbox)
            

    def incrementar_cantidad(self):
        label_cantidad = self.ids.id_cantidad
        self.cantidad_actual = int(label_cantidad.text)
        self.cantidad = self.cantidad_actual + 1
        label_cantidad.text = str(self.cantidad)
        
        # Acceder a la variable 'vector' desde CarritoWid
        carrito_widget = self.mainwid.CarritoWid
        if carrito_widget:
            vector = carrito_widget.vector
            print(vector)  # Haz lo que necesites con el vector aquí

            # Calcular subtotal
            subtotal = self.precio_inv * self.cantidad
            print("Subtotal:", subtotal)  # Imprimir subtotal
            # Actualizar la etiqueta self.total con el nuevo subtotal
            carrito_widget.total += subtotal - self.cantidad_actual*self.precio_inv
            carrito_widget.actualizar_total()  # Actualizar la etiqueta
        

    def on_checkbox_active_resta(self, checkbox, value):
        if value:
            self.disminuir_cantidad()
            self.toggle_checkbox(checkbox)
            

    def disminuir_cantidad(self):
        label_cantidad = self.ids.id_cantidad
        self.cantidad = int(label_cantidad.text)
        if self.cantidad > 1:
            self.cantidad -= 1
            label_cantidad.text = str(self.cantidad)

        # Acceder a la variable 'vector' desde CarritoWid
        carrito_widget = self.mainwid.CarritoWid
        if carrito_widget:
            vector = carrito_widget.vector
            
            subtotal = self.precio_inv * self.cantidad
            carrito_widget.total -= self.precio_inv
            carrito_widget.actualizar_total()
    
    
    def disminuir_cantidad_cero(self):
            label_cantidad = self.ids.id_cantidad
            cantidad = int(label_cantidad.text)
            precio_inv = self.precio_inv
            
            # Calcular el subtotal del producto antes de disminuir la cantidad
            subtotal = precio_inv * cantidad

            # Actualizar la cantidad
            if cantidad > 0:
                cantidad -= 1
                label_cantidad.text = str(cantidad)

            # Acceder al CarritoWid para actualizar el total
            carrito_widget = self.mainwid.CarritoWid
            if carrito_widget:
                vector = carrito_widget.vector
                carrito_widget.total -= subtotal  # Restar el subtotal del total
                carrito_widget.actualizar_total()

class NewDataButton(Button):
    def __init__(self,mainwid,**kwargs):
        super(NewDataButton,self).__init__()
        self.mainwid = mainwid
        self.data = ''
        
    def create_new_product(self):
        self.mainwid.goto_insertdata()

class FloatInput(TextInput):
    # Creamos una propiedad para almacenar el texto anterior
    previous_text = StringProperty("")

    def __init__(self, **kwargs):
        super(FloatInput, self).__init__(**kwargs)
        # Enlazamos el evento on_text para capturar los cambios de texto
        self.bind(text=self.on_text)

    def on_text(self, instance, value):
        # Si el nuevo texto no es un número flotante, restauramos el texto anterior
        try:
            float(value)
            self.previous_text = value
        except ValueError:
            self.text = self.previous_text

class IntInput(TextInput):
    previous_text = StringProperty("")

    def __init__(self, **kwargs):
        super(IntInput, self).__init__(**kwargs)
        self.bind(text=self.on_text)

    def on_text(self, instance, value):
        try:
            int(value)
            self.previous_text = value
        except ValueError:
            self.text = self.previous_text

class MainApp(App):
    def build(self):
        return MainWid()
        
if __name__ == '__main__':
    MainApp().run()
