# Librerias

import os
import random
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.autograd import Variable
import time

# Arquitectura


class Network3(nn.Module):

    def __init__(self, input_size, nb_action):
        super(Network3, self).__init__()
        self.input_size = input_size
        self.nb_action = nb_action
        # Combinacion Lineal de toda la data
        self.fc1 = nn.Linear(input_size, 30)

        # Combinacion Lineal de toda la data
        self.fc2 = nn.Linear(30, nb_action)

    def forward(self, state):
        x = torch.tanh(self.fc1(state))
        q_values = self.fc2(x)
        return q_values

# Experience Replay


class ReplayMemory3(object):

    def __init__(self, capacity):
        self.capacity = capacity
        self.memory = []

    def push(self, event):
        self.memory.append(event)
        if len(self.memory) > self.capacity:
            del self.memory[0]

    def sample(self, batch_size):
        samples = zip(*random.sample(self.memory, batch_size))
        return map(lambda x: Variable(torch.cat(x, 0)), samples)

# DQN


class Dqn3(object):

    def __init__(self, input_size, nb_action, gamma):
        self.start = time.time()
        self.gamma = gamma  # Para las penalizaciones
        self.model = Network3(input_size, nb_action)
        self.memory = ReplayMemory3(capacity=100000)
        # variante del descenso del Gradiente
        self.optimizer = optim.Adam(params=self.model.parameters())
        self.last_state = torch.Tensor(input_size).unsqueeze(
            0)  # Tensor Vacio de dimension [0,3]
        self.last_action = 0
        self.last_reward = 0
        self.reward_window = []

    def select_action(self, state):  # Selecciona una accion
        # Probabilidades del estado actual:
        probs = F.softmax(self.model(Variable(state))*100)
        action = probs.multinomial(len(probs))
        #print(f"Action : {action}")
        #print(f"Action : {type(action)}")
        return action.data[0, 0]

    def learn(self, batch_states, batch_actions, batch_rewards, batch_next_states):
        #print("Salida model :", end=" ")
        # print(self.model(batch_states).shape)#Salidas
        # Le pasamos la orientacion, y las 3 acciones
        # print((batch_states).shape)

        # Conseguimos el output del Modelo.
        # Gather hace la eleccion, con unsqueeze agregamos una dimension para seguir
        # trabajando con la eleccion, y despues con squeeze le bajamos a la dimension inicial
        # para obtener las salidas del Modelo
        batch_outputs = self.model(batch_states).gather(
            1, batch_actions.unsqueeze(1)).squeeze(1)

        # print(batch_outputs.shape)
        # print(self.model(batch_next_states))
        # Recibe una tupla de dimension 3 y devuelve el maximo valor
        # de cada una de las tuplas evaluadas, y se almacena en batch_next_outputs
        # print(batch_next_outputs)
        batch_next_outputs = self.model(batch_next_states).detach().max(1)[0]

        # Q(s,a) = R(s,a) + gamma*max(Q(s',a))
        # Q(varios) para el lote examinado
        batch_targets = batch_rewards + self.gamma * batch_next_outputs

        # Calculamos la perdida y tratamos de minimizar la perdida con el Optimizador
        # Adam
        td_loss = F.smooth_l1_loss(batch_outputs, batch_targets)
        self.optimizer.zero_grad()  # -> Poner los gradientes a Cero
        td_loss.backward()  # -> Backpropagation, obtenemos las gradientes
        self.optimizer.step()  # -> actualizando los pesos con Adam

    def update(self, new_state, new_reward):
        # Convierte el estado a un tensor float, y le aumenta 1 dimension
        new_state = torch.Tensor(new_state).float().unsqueeze(0)

        # Agregando a la memoria un evento, el evento es:
        # El estado actual, la accion, la recompensa, y el estado siguiente
        # last_state es el estado actual
        # last_reward -> la recompensa inmediata
        # new_state -> el estado siguiente
        self.memory.push((self.last_state, torch.LongTensor(
            [int(self.last_action)]), torch.Tensor([self.last_reward]), new_state))

        # Le pasamos un estado, y con select_action elije la accion
        # a tomar, de las probabilidades con la multinomial
        # tomando una accion [0,1,2]
        new_action = self.select_action(new_state)

        # Si la memoria de eventos se llena significa que
        # Empezamos a aprender tomando 100 muestras
        # Y lo mandamos a aprender, siempre y cuando tengamos
        # + de 100 muestras

        if len(self.memory.memory) > 100:
            # print(time.time() - self.start) #Tiempo que demora en entrar
            batch_states, batch_actions, batch_rewards, batch_next_states = self.memory.sample(
                100)
            self.learn(batch_states, batch_actions,
                       batch_rewards, batch_next_states)
        self.last_state = new_state
        self.last_action = new_action
        self.last_reward = new_reward
        if len(self.reward_window) > 1000:
            del self.reward_window[0]
        return new_action

    def score(self):
        return sum(self.reward_window) / (len(self.reward_window) + 1)  # Truco para no dividir entre 0

    def save(self):
        torch.save({'state_dict': self.model.state_dict(),
                    'optimizer': self.optimizer.state_dict(),
                    }, './saveBrain/last_brain3.pth')

    def load(self):
        if os.path.isfile('last_brain3.pth'):
            print("=> cargar checkpoint... ")
            checkpoint = torch.load('./saveBrain/last_brain3.pth')
            self.model.load_state_dict(checkpoint['state_dict'])
            self.optimizer.load_state_dict(checkpoint['optimizer'])
            print("hecho !")
        else:
            print("no checkpoint encontrado...")
