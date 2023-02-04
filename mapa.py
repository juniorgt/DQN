# Construccion del entorno

# Librerias
import numpy as np

# Agregamos todas las librerias propias de Kivy

# Esta linea es para que el clic derecho no ponga un punto rojo, Ademas de limitar los fps

from kivy.config import Config
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
Config.set('graphics', 'maxfps', '20')

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
# from kivy.uix.button import Button
from kivy.uix.actionbar import ActionBar
from kivy.graphics import Color, Line
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock


# Importaremos Nuestras clases de aprendizaje por refuerzo profundo
from q_dl import Dqn
from q_dl2 import Dqn2
from q_dl3 import Dqn3
from q_dl4 import Dqn4

# Introduciendo last_x y last_y, usados para mantener el último punto en la memoria cuando dibujamos la arena en el mapa
last_x = 0
last_y = 0
n_points = 0
length = 0

# Creando la mente de nuestra IA, la lista de acciones y la variable de recompensa
brain = Dqn(4, 3, 0.9)
action2rotation = [0, 20, -20]
reward = 0

brain2 = Dqn2(4, 3, 0.9)
action2rotation2 = [0, 20, -20]
reward2 = 0


brain3 = Dqn3(4, 3, 0.9)
action2rotation3 = [0, 20, -20]
reward3 = 0

brain4 = Dqn4(4, 3, 0.9)
action2rotation4 = [0, 20, -20]
reward4 = 0
# Inicializando el mapa
first_update = True
conteo = 0

list_reward_car_one = []
list_reward_car_two = []
list_reward_car_three = []
list_reward_car_four = []


def init():
    global sand
    global goal_x
    global goal_y
    global goal_x2
    global goal_y2
    global goal_x3
    global goal_y3
    global goal_x4
    global goal_y4
    global first_update
    # sand = np.zeros((longueur, largeur))
    sand = np.zeros((800, 600))  # TODO Cambiar al FINAL se puede mejorar
    goal_x = 20
    goal_y = 424 - 20
    goal_x2 = 20
    goal_y2 = 424 - 20
    goal_x3 = 20
    goal_y3 = 424 - 20
    goal_x4 = 20
    goal_y4 = 424 - 20
    first_update = False


# Inicializando la ultima distancia del carro a la meta

last_distance = 0
last_distance2 = 0
last_distance3 = 0
last_distance4 = 0
# La clase car nos permitirá rastrear los parametros del carrito, además desde aqui
# podemos detectar la arena (obstaculo principal) del entorno y
# podemos manipular el movimiento de las acciones resultantes de nuestro Dqn.


class Car(Widget):

    # Inicializamos todos los parametros del entorno
    # Comenzamos por inicializar el angulo, la velocidad y los sensores del carro.
    angle = NumericProperty(0)
    rotation = NumericProperty(0)
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)
    sensor1_x = NumericProperty(0)
    sensor1_y = NumericProperty(0)
    sensor1 = ReferenceListProperty(sensor1_x, sensor1_y)
    sensor2_x = NumericProperty(0)
    sensor2_y = NumericProperty(0)
    sensor2 = ReferenceListProperty(sensor2_x, sensor2_y)
    sensor3_x = NumericProperty(0)
    sensor3_y = NumericProperty(0)
    sensor3 = ReferenceListProperty(sensor3_x, sensor3_y)
    # Inicializamos además las señales que recibe cada sensor.
    signal1 = NumericProperty(0)
    signal2 = NumericProperty(0)
    signal3 = NumericProperty(0)

    def move(self, rotation):
        self.pos = Vector(*self.velocity) + self.pos
        self.rotation = rotation
        self.angle = self.angle + self.rotation
        # Actualizamos los sensores dado el movimiento y giro del carrito.
        # Sensor1 siempre al frente del carrito.
        self.sensor1 = Vector(30, 0).rotate(self.angle) + self.pos
        # Sensores 2 y 3 ubicados en posiciones izquierda y derecha a 30 grados del frente.
        self.sensor2 = Vector(30, 0).rotate((self.angle+30) % 360) + self.pos
        self.sensor3 = Vector(30, 0).rotate((self.angle-30) % 360) + self.pos
        # Actualizamos lectura de la señales de los sensores, aqui queremos obtener la presencia de arena
        # por lo que calcularemos la densidad de arena encontrada por el sensor, sumando los puntos
        # que son arena (Que se encuentren En un rango cuadrado de 20 pixeles de lado) y dividiendolos entre
        # el area (400 px).
        self.signal1 = int(np.sum(sand[int(self.sensor1_x)-10:int(
            self.sensor1_x)+10, int(self.sensor1_y)-10:int(self.sensor1_y)+10]))/400.
        # print(self.signal1)
        self.signal2 = int(np.sum(sand[int(self.sensor2_x)-10:int(
            self.sensor2_x)+10, int(self.sensor2_y)-10:int(self.sensor2_y)+10]))/400.
        self.signal3 = int(np.sum(sand[int(self.sensor3_x)-10:int(
            self.sensor3_x)+10, int(self.sensor3_y)-10:int(self.sensor3_y)+10]))/400.
        # Si algun sensor cae dentro de los margenes de la ventana, se dará como obstaculo de densidad 1.
        if self.sensor1_x > longueur-10 or self.sensor1_x < 10 or self.sensor1_y > largeur-10 or self.sensor1_y < 10:
            self.signal1 = 1.
        if self.sensor2_x > longueur-10 or self.sensor2_x < 10 or self.sensor2_y > largeur-10 or self.sensor2_y < 10:
            self.signal2 = 1.
        if self.sensor3_x > longueur-10 or self.sensor3_x < 10 or self.sensor3_y > largeur-10 or self.sensor3_y < 10:
            self.signal3 = 1.


class Car2(Widget):
    angle = NumericProperty(0)
    rotation = NumericProperty(0)
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)
    sensor1_x = NumericProperty(0)
    sensor1_y = NumericProperty(0)
    sensor1 = ReferenceListProperty(sensor1_x, sensor1_y)
    sensor2_x = NumericProperty(0)
    sensor2_y = NumericProperty(0)
    sensor2 = ReferenceListProperty(sensor2_x, sensor2_y)
    sensor3_x = NumericProperty(0)
    sensor3_y = NumericProperty(0)
    sensor3 = ReferenceListProperty(sensor3_x, sensor3_y)
    signal1 = NumericProperty(0)
    signal2 = NumericProperty(0)
    signal3 = NumericProperty(0)

    def move(self, rotation):
        self.pos = Vector(*self.velocity) + self.pos
        self.rotation = rotation
        self.angle = self.angle + self.rotation
        self.sensor1 = Vector(30, 0).rotate(self.angle) + self.pos
        self.sensor2 = Vector(30, 0).rotate((self.angle+30) % 360) + self.pos
        self.sensor3 = Vector(30, 0).rotate((self.angle-30) % 360) + self.pos
        self.signal1 = int(np.sum(sand[int(self.sensor1_x)-10:int(
            self.sensor1_x)+10, int(self.sensor1_y)-10:int(self.sensor1_y)+10]))/400.
        self.signal2 = int(np.sum(sand[int(self.sensor2_x)-10:int(
            self.sensor2_x)+10, int(self.sensor2_y)-10:int(self.sensor2_y)+10]))/400.
        self.signal3 = int(np.sum(sand[int(self.sensor3_x)-10:int(
            self.sensor3_x)+10, int(self.sensor3_y)-10:int(self.sensor3_y)+10]))/400.
        if self.sensor1_x > longueur-10 or self.sensor1_x < 10 or self.sensor1_y > largeur-10 or self.sensor1_y < 10:
            self.signal1 = 1.
        if self.sensor2_x > longueur-10 or self.sensor2_x < 10 or self.sensor2_y > largeur-10 or self.sensor2_y < 10:
            self.signal2 = 1.
        if self.sensor3_x > longueur-10 or self.sensor3_x < 10 or self.sensor3_y > largeur-10 or self.sensor3_y < 10:
            self.signal3 = 1.


class Car3(Widget):
    angle = NumericProperty(0)
    rotation = NumericProperty(0)
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)
    sensor1_x = NumericProperty(0)
    sensor1_y = NumericProperty(0)
    sensor1 = ReferenceListProperty(sensor1_x, sensor1_y)
    sensor2_x = NumericProperty(0)
    sensor2_y = NumericProperty(0)
    sensor2 = ReferenceListProperty(sensor2_x, sensor2_y)
    sensor3_x = NumericProperty(0)
    sensor3_y = NumericProperty(0)
    sensor3 = ReferenceListProperty(sensor3_x, sensor3_y)
    signal1 = NumericProperty(0)
    signal2 = NumericProperty(0)
    signal3 = NumericProperty(0)

    def move(self, rotation):
        self.pos = Vector(*self.velocity) + self.pos
        self.rotation = rotation
        self.angle = self.angle + self.rotation
        self.sensor1 = Vector(30, 0).rotate(self.angle) + self.pos
        self.sensor2 = Vector(30, 0).rotate((self.angle+30) % 360) + self.pos
        self.sensor3 = Vector(30, 0).rotate((self.angle-30) % 360) + self.pos
        self.signal1 = int(np.sum(sand[int(self.sensor1_x)-10:int(
            self.sensor1_x)+10, int(self.sensor1_y)-10:int(self.sensor1_y)+10]))/400.
        self.signal2 = int(np.sum(sand[int(self.sensor2_x)-10:int(
            self.sensor2_x)+10, int(self.sensor2_y)-10:int(self.sensor2_y)+10]))/400.
        self.signal3 = int(np.sum(sand[int(self.sensor3_x)-10:int(
            self.sensor3_x)+10, int(self.sensor3_y)-10:int(self.sensor3_y)+10]))/400.
        if self.sensor1_x > longueur-10 or self.sensor1_x < 10 or self.sensor1_y > largeur-10 or self.sensor1_y < 10:
            self.signal1 = 1.
        if self.sensor2_x > longueur-10 or self.sensor2_x < 10 or self.sensor2_y > largeur-10 or self.sensor2_y < 10:
            self.signal2 = 1.
        if self.sensor3_x > longueur-10 or self.sensor3_x < 10 or self.sensor3_y > largeur-10 or self.sensor3_y < 10:
            self.signal3 = 1.


class Car4(Widget):

    # Inicializamos todos los parametros del entorno
    # Comenzamos por inicializar el angulo, la velocidad y los sensores del carro.
    angle = NumericProperty(0)
    rotation = NumericProperty(0)
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)
    sensor1_x = NumericProperty(0)
    sensor1_y = NumericProperty(0)
    sensor1 = ReferenceListProperty(sensor1_x, sensor1_y)
    sensor2_x = NumericProperty(0)
    sensor2_y = NumericProperty(0)
    sensor2 = ReferenceListProperty(sensor2_x, sensor2_y)
    sensor3_x = NumericProperty(0)
    sensor3_y = NumericProperty(0)
    sensor3 = ReferenceListProperty(sensor3_x, sensor3_y)
    # Inicializamos además las señales que recibe cada sensor.
    signal1 = NumericProperty(0)
    signal2 = NumericProperty(0)
    signal3 = NumericProperty(0)

    def move(self, rotation):
        self.pos = Vector(*self.velocity) + self.pos
        self.rotation = rotation
        self.angle = self.angle + self.rotation
        # Actualizamos los sensores dado el movimiento y giro del carrito.
        # Sensor1 siempre al frente del carrito.
        
        self.sensor1 = Vector(30, 0).rotate(self.angle) + self.pos
        # Sensores 2 y 3 ubicados en posiciones izquierda y derecha a 30 grados del frente.
        self.sensor2 = Vector(30, 0).rotate((self.angle+30) % 360) + self.pos
        self.sensor3 = Vector(30, 0).rotate((self.angle-30) % 360) + self.pos
        # Actualizamos lectura de la señales de los sensores, aqui queremos obtener la presencia de arena
        # por lo que calcularemos la densidad de arena encontrada por el sensor, sumando los puntos
        # que son arena (Que se encuentren En un rango cuadrado de 20 pixeles de lado) y dividiendolos entre
        # el area (400 px).
        
        self.signal1 = int(np.sum(sand[int(self.sensor1_x)-10:int(
            self.sensor1_x)+10, int(self.sensor1_y)-10:int(self.sensor1_y)+10]))/400.

        # print(self.signal1)
        self.signal2 = int(np.sum(sand[int(self.sensor2_x)-10:int(
            self.sensor2_x)+10, int(self.sensor2_y)-10:int(self.sensor2_y)+10]))/400.
        
        self.signal3 = int(np.sum(sand[int(self.sensor3_x)-10:int(
            self.sensor3_x)+10, int(self.sensor3_y)-10:int(self.sensor3_y)+10]))/400.
        
        # Si algun sensor cae dentro de los margenes de la ventana, se dará como obstaculo de densidad 1.
        if self.sensor1_x > longueur-10 or self.sensor1_x < 10 or self.sensor1_y > largeur-10 or self.sensor1_y < 10:
            self.signal1 = 1.
        if self.sensor2_x > longueur-10 or self.sensor2_x < 10 or self.sensor2_y > largeur-10 or self.sensor2_y < 10:
            self.signal2 = 1.
        if self.sensor3_x > longueur-10 or self.sensor3_x < 10 or self.sensor3_y > largeur-10 or self.sensor3_y < 10:
            self.signal3 = 1.


class Ball1(Widget):
    pass


class Ball2(Widget):
    pass


class Ball3(Widget):
    pass


class Ball4(Widget):
    pass


class Ball5(Widget):
    pass


class Ball6(Widget):
    pass


class Ball7(Widget):
    pass


class Ball8(Widget):
    pass


class Ball9(Widget):
    pass


class Ball10(Widget):
    pass


class Ball11(Widget):
    pass


class Ball12(Widget):
    pass


class Game(Widget):

    car = ObjectProperty(None)
    car2 = ObjectProperty(None)
    car3 = ObjectProperty(None)
    car4 = ObjectProperty(None)
    ball1 = ObjectProperty(None)
    ball2 = ObjectProperty(None)
    ball3 = ObjectProperty(None)
    ball4 = ObjectProperty(None)
    ball5 = ObjectProperty(None)
    ball6 = ObjectProperty(None)
    ball7 = ObjectProperty(None)
    ball8 = ObjectProperty(None)
    ball9 = ObjectProperty(None)
    ball10 = ObjectProperty(None)
    ball11 = ObjectProperty(None)
    ball12 = ObjectProperty(None)
    stats_widget = None
    scores = []

    def serve_car(self):
        self.car.center = self.center
        self.car.velocity = Vector(6, 0)

        self.car2.center = self.center
        self.car2.velocity = Vector(6, 0)

        self.car3.center = self.center
        self.car3.velocity = Vector(6, 0)

        self.car4.center = self.center
        self.car4.velocity = Vector(6, 0)

    def update(self, dt):

        global brain
        global brain2
        global brain3
        global brain4
        global reward
        global reward2
        global reward3
        global reward4
        global conteo
        global last_distance
        global last_distance2
        global last_distance3
        global last_distance4
        global goal_x
        global goal_y
        global goal_x2
        global goal_y2
        global goal_x3
        global goal_y3
        global goal_x4
        global goal_y4
        global longueur
        global largeur

        longueur = self.width
        largeur = self.height
        if first_update:
            init()

        update_sand = True
        if update_sand:
            sand = np.zeros((int(self.width), int(self.height)))
            update_sand = False

        # Diferencia de x-coordenadas entre la meta y el carrito.
        xx = goal_x - self.car.x
        # Diferencia de y-coordenadas entre la meta y el carrito.
        yy = goal_y - self.car.y
        xx2 = goal_x2 - self.car2.x
        yy2 = goal_y2 - self.car2.y
        xx3 = goal_x3 - self.car3.x
        yy3 = goal_y3 - self.car3.y
        xx4 = goal_x4 - self.car4.x
        yy4 = goal_y4 - self.car4.y

        orientation = Vector(*self.car.velocity).angle((xx, yy))/180.
        orientation2 = Vector(*self.car2.velocity).angle((xx2, yy2))/180.
        orientation3 = Vector(*self.car3.velocity).angle((xx3, yy3))/180.
        orientation4 = Vector(*self.car4.velocity).angle((xx4, yy4))/180.

        state = [orientation, self.car.signal1,
                 self.car.signal2, self.car.signal3]
        state2 = [orientation2, self.car2.signal1,
                  self.car2.signal2, self.car2.signal3]
        state3 = [orientation3, self.car3.signal1,
                  self.car3.signal2, self.car3.signal3]
        state4 = [orientation4, self.car4.signal1,
                  self.car4.signal2, self.car4.signal3]
        action = brain.update(state, reward)
        action2 = brain2.update(state2, reward2)
        action3 = brain3.update(state3, reward3)
        action4 = brain4.update(state4, reward4)

        rotation = action2rotation[action]
        rotation2 = action2rotation2[action2]
        rotation3 = action2rotation3[action3]
        rotation4 = action2rotation4[action4]

        self.car.move(rotation)
        self.car2.move(rotation2)
        self.car3.move(rotation3)
        self.car4.move(rotation4)

        distance = np.sqrt((self.car.x - goal_x)**2 + (self.car.y - goal_y)**2)
        distance2 = np.sqrt((self.car2.x - goal_x2)**2 +
                            (self.car2.y - goal_y2)**2)
        distance3 = np.sqrt((self.car3.x - goal_x3)**2 +
                            (self.car3.y - goal_y3)**2)
        distance4 = np.sqrt((self.car4.x - goal_x4)**2 +
                            (self.car4.y - goal_y4)**2)

        # Actualizamos las posiciones de los sensores en el mapa.
        self.ball1.pos = self.car.sensor1
        self.ball2.pos = self.car.sensor2
        self.ball3.pos = self.car.sensor3

        self.ball4.pos = self.car2.sensor1
        self.ball5.pos = self.car2.sensor2
        self.ball6.pos = self.car2.sensor3

        self.ball7.pos = self.car3.sensor1
        self.ball8.pos = self.car3.sensor2
        self.ball9.pos = self.car3.sensor3

        self.ball10.pos = self.car4.sensor1
        self.ball11.pos = self.car4.sensor2
        self.ball12.pos = self.car4.sensor3

        self.scores.append(brain.score())


        #************************ ZONA DE RECOMPENSAS ******************************************

        # Cuando el carrito1 se encuentra en obstaculo disminuye su velocidad a 1.
        if sand[int(self.car.x), int(self.car.y)] > 0 or self.car.collide_widget(self.car2) or self.car.collide_widget(self.car3) or self.car.collide_widget(self.car4):
            self.car.velocity = Vector(1, 0).rotate(self.car.angle)
            reward = -1
        # Caso contrario el carrito1 mantiene una velocidad de 6.
        else:
            self.car.velocity = Vector(6, 0).rotate(self.car.angle)
            reward = -0.2
            if distance < last_distance:
                reward = 0.1

        # Actualizamos lectura de sensores del carro 1 para que detecte cuando choca con otro carro.
        if self.ball1.collide_widget(self.car2) or self.ball1.collide_widget(self.car3) or self.ball1.collide_widget(self.car4):
            self.car.signal1 = 1.0
       

        if self.ball2.collide_widget(self.car2) or self.ball2.collide_widget(self.car3) or self.ball2.collide_widget(self.car4):
        	self.car.signal2 = 1.0

        if self.ball3.collide_widget(self.car2) or self.ball3.collide_widget(self.car3) or self.ball3.collide_widget(self.car4):
        	self.car.signal3 = 1.0
        #----------------------------------------------------------------------------------

        # Cuando el carrito2 se encuentra en obstaculo disminuye su velocidad a 1.
        if sand[int(self.car2.x), int(self.car2.y)] > 0 or self.car2.collide_widget(self.car) or self.car2.collide_widget(self.car3) or self.car2.collide_widget(self.car4):
            self.car2.velocity = Vector(1, 0).rotate(self.car2.angle)
            reward2 = -1
        # Caso contrario el carrito2 mantiene una velocidad de 6.
        else:
            self.car2.velocity = Vector(6, 0).rotate(self.car2.angle)
            reward2 = -0.2
            if distance2 < last_distance2:
                reward2 = 0.1

        # Actualizamos lectura de sensores del carro 2 para que detecte cuando choca con otro carro.
        if self.ball4.collide_widget(self.car) or self.ball4.collide_widget(self.car3) or self.ball4.collide_widget(self.car4):
            self.car2.signal1 = 1.0
        

        if self.ball5.collide_widget(self.car) or self.ball5.collide_widget(self.car3) or self.ball5.collide_widget(self.car4):
            self.car2.signal2 = 1.0

        if self.ball6.collide_widget(self.car) or self.ball6.collide_widget(self.car3) or self.ball6.collide_widget(self.car4):
            self.car2.signal3 = 1.0
        #----------------------------------------------------------------------------------

        # Cuando el carrito3 se encuentra en obstaculo disminuye su velocidad a 1.
        if sand[int(self.car3.x), int(self.car3.y)] > 0 or self.car3.collide_widget(self.car) or self.car3.collide_widget(self.car2) or self.car3.collide_widget(self.car4):
            self.car3.velocity = Vector(1, 0).rotate(self.car3.angle)
            reward3 = -1
        # Caso contrario el carrito3 mantiene una velocidad de 6.
        else:
            self.car3.velocity = Vector(6, 0).rotate(self.car3.angle)
            reward3 = -0.2
            if distance3 < last_distance3:
                reward3 = 0.1

        # Actualizamos lectura de sensores del carro 3 para que detecte cuando choca con otro carro.
        if self.ball7.collide_widget(self.car) or self.ball7.collide_widget(self.car2) or self.ball7.collide_widget(self.car4):
            self.car3.signal1 = 1.0
        # print(self.signal1)

        if self.ball8.collide_widget(self.car) or self.ball8.collide_widget(self.car2) or self.ball8.collide_widget(self.car4):
        	self.car3.signal2 = 1.0

        if self.ball9.collide_widget(self.car) or self.ball9.collide_widget(self.car2) or self.ball9.collide_widget(self.car4):
        	self.car3.signal3 = 1.0
        #----------------------------------------------------------------------------------

        # Cuando el carrito4 se encuentra en obstaculo disminuye su velocidad a 1.
        if sand[int(self.car4.x), int(self.car4.y)] > 0 or self.car4.collide_widget(self.car) or self.car4.collide_widget(self.car2) or self.car4.collide_widget(self.car3):
            self.car4.velocity = Vector(1, 0).rotate(self.car4.angle)
            reward4 = -1
        # Caso contrario el carrito4 mantiene una velocidad de 6.
        else:
            self.car4.velocity = Vector(6, 0).rotate(self.car4.angle)
            reward4 = -0.2
            if distance4 < last_distance4:
                reward4 = 0.1

        if self.ball10.collide_widget(self.car) or self.ball10.collide_widget(self.car2) or self.ball10.collide_widget(self.car3):
            self.car4.signal1 = 1.0
        # print(self.signal1)

        if self.ball11.collide_widget(self.car) or self.ball11.collide_widget(self.car2) or self.ball11.collide_widget(self.car3):
        	self.car4.signal2 = 1.0

        if self.ball12.collide_widget(self.car) or self.ball12.collide_widget(self.car2) or self.ball12.collide_widget(self.car3):
        	self.car4.signal3 = 1.0

        # Si el carrito logra salirse de los bordes del mapa, se dará una penalidad de -1.
        if self.car.x < 10:
            self.car.x = 10
            reward = -1
        if self.car.x > self.width - 10:
            self.car.x = self.width - 10
            reward = -1
        if self.car.y < 10:
            self.car.y = 10
            reward = -1
        if self.car.y > self.height - 10:
            self.car.y = self.height - 10
            reward = -1

        if distance < 100:
            goal_x = self.width-goal_x
            goal_y = self.height-goal_y

        last_distance = distance

        if self.car2.x < 10:
            self.car2.x = 10
            reward2 = -1
        if self.car2.x > self.width - 10:
            self.car2.x = self.width - 10
            reward2 = -1
        if self.car2.y < 10:
            self.car2.y = 10
            reward2 = -1
        if self.car2.y > self.height - 10:
            self.car2.y = self.height - 10
            reward2 = -1

        if distance2 < 100:
            goal_x2 = self.width-goal_x2
            goal_y2 = self.height-goal_y2

        last_distance2 = distance2

        if self.car3.x < 10:
            self.car3.x = 10
            reward3 = -1
        if self.car3.x > self.width - 10:
            self.car3.x = self.width - 10
            reward3 = -1
        if self.car3.y < 10:
            self.car3.y = 10
            reward3 = -1
        if self.car3.y > self.height - 10:
            self.car3.y = self.height - 10
            reward3 = -1

        if distance3 < 100:
            goal_x3 = self.width-goal_x3
            goal_y3 = self.height-goal_y3

        last_distance3 = distance3

        if self.car4.x < 10:
            self.car4.x = 10
            reward4 = -1
        if self.car4.x > self.width - 10:
            self.car4.x = self.width - 10
            reward4 = -1
        if self.car4.y < 10:
            self.car4.y = 10
            reward4 = -1
        if self.car4.y > self.height - 10:
            self.car4.y = self.height - 10
            reward4 = -1

        if distance4 < 100:
            goal_x4 = self.width-goal_x4
            goal_y4 = self.height-goal_y4

        # *******************************************************************************

        last_distance4 = distance4
        stats = {
            'Distance to Dest from car 1': "{0:.2f}".format(last_distance),
            'Distance to Dest from car 2': "{0:.2f}".format(last_distance2),
            'Distance to Dest from car 3': "{0:.2f}".format(last_distance3),
            'Distance to Dest from car 4': "{0:.2f}".format(last_distance4),
            'Car 1 sensors': 'R [{0:.1f}] B [{1:.1f}] Y [{2:.1f}]'.format(self.car.signal1,
                                                                          self.car.signal2,
                                                                          self.car.signal3),
            'Car 2 sensors': 'R [{0:.1f}] B [{1:.1f}] Y [{2:.1f}]'.format(self.car2.signal1,
                                                                          self.car2.signal2,
                                                                          self.car2.signal3),
            'Car 3 sensors': 'R [{0:.1f}] B [{1:.1f}] Y [{2:.1f}]'.format(self.car3.signal1,
                                                                          self.car3.signal2,
                                                                          self.car3.signal3),
            'Car 4 sensors': 'R [{0:.1f}] B [{1:.1f}] Y [{2:.1f}]'.format(self.car4.signal1,
                                                                          self.car4.signal2,
                                                                          self.car4.signal3),
            'Last reward car 1': "{0:.2f}".format(reward),
            'Last reward car 2': "{0:.2f}".format(reward2),
            'Last reward car 3': "{0:.2f}".format(reward3),
            'Last reward car 4': "{0:.2f}".format(reward4),
        }

        list_reward_car_one.append(reward)
        list_reward_car_two.append(reward2)
        list_reward_car_three.append(reward3)
        list_reward_car_four.append(reward4)


        if self.stats_widget is not None:
            self.stats_widget.update_stats(stats)


class StatsWidget(GridLayout):

    first_update = True
    labels = {}

    def __init__(self, **kwargs):
        super(StatsWidget, self).__init__(**kwargs)

    def update_stats(self, stats):
        if self.first_update:
            self.first_update = False
            self.rows = len(stats)
            for key, value in stats.items():
                self.labels[key] = Label(text=value)
                self.add_widget(Label(text=key))
                self.add_widget(self.labels[key])
        else:
            for key, value in stats.items():
                self.labels[key].text = value


class TopPanel(BoxLayout):
    stats_widget = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(TopPanel, self).__init__(**kwargs)


class MyPaintWidget(Widget):

    def on_touch_down(self, touch):
        global length, n_points, last_x, last_y
        with self.canvas:
            Color(0.8, 0.7, 0)
            d = 10.
            touch.ud['line'] = Line(points=(touch.x, touch.y), width=10)
            last_x = int(touch.x)
            last_y = int(touch.y)
            n_points = 0
            length = 0
            sand[int(touch.x), int(touch.y)] = 1

    def on_touch_move(self, touch):
        global length, n_points, last_x, last_y
        if touch.button == 'left':
            touch.ud['line'].points += [touch.x, touch.y]
            x = int(touch.x)
            y = int(touch.y)
            length += np.sqrt(max((x - last_x)**2 + (y - last_y)**2, 2))
            #n_points += 1.
            #density = n_points/(length)
            density = 0.3
            touch.ud['line'].width = int(20 * density + 1)
            sand[int(touch.x) - 10: int(touch.x) + 10,
                 int(touch.y) - 10: int(touch.y) + 10] = 1
            last_x = x
            last_y = y


class TopMenuWidget(ActionBar):
    save_brain_button = ObjectProperty(None)
    load_btn = ObjectProperty(None)
    clear_btn = ObjectProperty(None)


class RootWidget(BoxLayout):
    pass


class CarApp(App):

    def build(self):
        self.game_widget = Game()
        self.game_widget.serve_car()
        Clock.schedule_interval(self.game_widget.update, 1.0/60.0)
        self.painter = MyPaintWidget()

        self.game_widget.add_widget(self.painter)

        action_bar = TopMenuWidget()
        action_bar.save_brain_button.bind(on_release=self.save)
        action_bar.load_btn.bind(on_release=self.load)
        action_bar.clear_btn.bind(on_release=self.clear_canvas)

        self.top_panel = TopPanel()
        self.game_widget.stats_widget = self.top_panel.stats_widget

        root = RootWidget()
        root.add_widget(action_bar)
        root.add_widget(self.top_panel)
        root.add_widget(self.game_widget)
        return root

    def clear_canvas(self, obj):
        global sand
        self.painter.canvas.clear()
        sand = np.zeros((800, 600))

    def save(self, obj):
        print("Guardando la memoria...")
        brain.save()
        brain2.save()
        brain3.save()
        brain4.save()
        np.savetxt("./rewards/reward_one.txt", list_reward_car_one)
        np.savetxt("./rewards/reward_two.txt", list_reward_car_two)
        np.savetxt("./rewards/reward_three.txt", list_reward_car_three)
        np.savetxt("./rewards/reward_four.txt", list_reward_car_four)

    def load(self, obj):
        print("Cargando la ultima memoria de IA...")
        brain.load()
        brain2.load()
        brain3.load()
        brain4.load()


# Corriendo todo
if __name__ == '__main__':
    CarApp().run()
