import logging
import matlab.engine
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ConversationHandler
from io import StringIO 
import sys
import networkx as nx
import random
import matplotlib.pyplot as plot
from bs4 import BeautifulSoup
import requests
import re
import string
import random

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

GENDER, PHOTO, LOCATION, BIO = range(4)

class Capturing(list):
    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self
    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        del self._stringio    # free up some memory
        sys.stdout = self._stdout

class Bot:

    # Constructor de nuestra clase.
    def __init__(self):
        pass

    # Definimos el método de inicio.
    def start(self, update, context):
        logger.info("El usuario ha iniciado el bot.")
        name = update.message.chat.first_name
        # Definimos los botones que podrá elegir el usuario.
        options = [
            [InlineKeyboardButton("Hallar función generadora", callback_data="op1")],
            [InlineKeyboardButton("Hallar función generadora con coeficientes", callback_data="op2")],
            [InlineKeyboardButton("Cadenas de Markov", callback_data="op3")],
            [InlineKeyboardButton("Crear Grafo", callback_data="op4")],
        ]
        texto = f"¡Bienvenido, {name}\\! Es un gusto tenerte por acá\\. Si deseas más información sobre los comandos, escribe /ayuda\\."
        reply_markup = InlineKeyboardMarkup(options)
        update.message.reply_text(texto, parse_mode='MarkdownV2', reply_markup=reply_markup)

    def ayuda(self, update, context):
        # Obtenemos el nombre del usuario.
        name = update.message.chat.first_name
        logger.info(f"El usuario {name} ha solicitado ayuda.")
        texto = """
Hola, es un gusto poder ayudarte, mis comandos son:
*Funciones:*
\- /start: Inicia el bot

\- Hallar función generadora: Recibe los coeficientes del polinomio característico asociado a una relación de re-currencia lineal, homogénea, con coeficientes constantes, de grado k y muestra cuál sería la forma de la solución según el teorema correspondiente.

\- Hallar función generadora con coeficientes: Muestra la expresión con los valores de las constantes (c0,c1, . . . ,ck) y la solución de la relación de recurrencia

\- Cadenas de Markov: Dado  un  sitio  web  estatico, se implementa un modelo de cadenas de Markov para generar un texto ficticio

\- Crear Grafo: Genera un grafo una vez se le introduzcan los siguienters datos:
    \- E: Número de aristas\.
    \- V: Número de vértices\.
    \- K: Grado máximo de los vértices\.
        """
        # Enviar una descripción cualquieray los botones para escoger.
        update.message.reply_text(texto)

    def f1_input_RR(self, update, context):
        logger.info("El usuario ha solicitado f1.")
        # Recibimos la solicitud del servidor.
        
        query = update.callback_query
        query.message.reply_text('Digita la RR=[cn;-cn1;-cn2;...;-cnk]=')
        return 0

    def f1_input_a(self, update, context):
        self.RR1 = update.message.text
        
        # Recibimos la solicitud del servidor.
        update.message.reply_text('Digita las c.i. a=[a0; a1;...,ak]=')
        return 1

    def f1(self, update, context):
        self.a1 = update.message.text
        script = f"""function res=coefpol()
%% Datos de Entrada
clc;clear; syms n;syms c0;syms c1;
RR={self.RR1}
a={self.a1}
%% Proceso
R=roots(RR);
k=length(a);
MR=zeros(k);
for cont=1:k
    MR(cont,:)=R.^(cont-1);
end
b=[c1;c0];
info_R=tabulate(R);
t=size(info_R,1);
m=info_R(:,2);
%for i=1:t

sol=dot(b,R.^n);
%% Información de Salida
sol
res = ['[', strjoin(arrayfun(@char,sol,'uniform',0), ', '), ']'];
end
        """
        self.crearfun(script, "coefpol")
        eng = matlab.engine.start_matlab()
        with Capturing() as output:
            eng.coefpol(nargout=1, stdout=sys.stdout)
        update.message.reply_text(output)
        return ConversationHandler.END
    
    def crearfun(self, script, nombre):
        with open(f"{nombre}.m","w+") as f:
            f.write(script)    

    def f2_input_RR(self, update, context):
        logger.info("El usuario ha solicitado f2.")
        # Recibimos la solicitud del servidor.
        
        query = update.callback_query
        query.message.reply_text('Digita la RR=[cn;-cn1;-cn2;...;-cnk]=')
        return 0

    def f2_input_a(self, update, context):
        self.RR = update.message.text
        
        # Recibimos la solicitud del servidor.
        update.message.reply_text('Digita las c.i. a=[a0; a1;...,ak]=')

        return 1
    
    def f2_input_i0(self, update, context):
        self.a = update.message.text
        
        update.message.reply_text('Digita i0=')
        return 2
    
    def f2_result(self, update, context):
        self.i0 = update.message.text
        script = f"""function sol=coef()
%% Datos de Entrada
clc;clear all;syms n;
RR={self.RR}
a={self.a}
i0={self.i0}
%% Proceso
R=roots(RR);
k=length(a);
MR=zeros(k);
for cont=1:k
    MR(cont,:)=R.^(i0+cont-1);
end
b=MR\\a;
info_R=tabulate(R);
t=size(info_R,1);
m=info_R(:,2);
%for i=1:t

sol=dot(b,R.^n);
%% Información de Salida
sol
end
        """
        self.crearfun(script, "coef")
        eng = matlab.engine.start_matlab()
        with Capturing() as output:
            eng.coef(nargout=1, stdout=sys.stdout)
        update.message.reply_text("\n".join(output))
        return ConversationHandler.END

    def f3_input(self, update, context):
        logger.info("El usuario ha solicitado f3.")
        # Recibimos la solicitud del servidor.
        
        query = update.callback_query
        query.message.reply_text('Digite la pagina web a consultar: ')
        return 0

    def f3(self, update, context):
        self.f3 = update.message.text
        url = self.f3
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")

        contenido = soup.html
        texto = []
        for string in contenido.strings:
            texto.append(string)

        texto = self.limpiar_texto(str(texto))
        update.message.reply_text(f"Original: \n\n{texto}", parse_mode="MarkdownV2")

        letras = list(texto)
        dic = {}
        for letra in letras:
            if letra not in dic.keys():
                dic[letra] = 1
            else:
                dic[letra] += 1

        freqa = 0
        for llave in dic.keys():
            freq = dic[llave]/len(letras)
            freqa += freq
            dic[llave] = [freqa]

        frecuencias = []
        for llaves in dic.keys():
            faq = float(str(dic.get(llaves)).replace("[", "").replace("]", ""))
            frecuencias.append(faq)

        final = []
        for strings in letras:
            ran = random.random()
            prob = min(frecuencias, key=lambda x:abs(x-ran))
            for cadena in dic.keys():
                if prob == float(str(dic.get(cadena)).replace("[", "").replace("]", "")):
                    final.append(str(cadena))

        final = (self.limpiar_texto(str(final))).replace(" ", "")
        update.message.reply_text(f"Markov K \= 0: \n\n{final}", parse_mode="MarkdownV2")
        return ConversationHandler.END
        
    def limpiar_texto(self, text: str):
        text = re.sub(r"\\n", "", text)
        text = re.sub(r'[^\w\s]', '', text)
        text = re.sub(r'[0-9]+', '', text)
        text = re.sub(' +', ' ', text)
        return text

    def f4_input_V(self, update, context):
        logger.info("El usuario ha solicitado f4.")
        # Recibimos la solicitud del servidor.
        
        query = update.callback_query
        query.message.reply_text('Digite el número de vertices del grafo: ')
        return 0

    def f4_input_E(self, update, context):
        self.V = update.message.text
        logger.info("El usuario ha solicitado f4.")
        # Recibimos la solicitud del servidor.
        
        update.message.reply_text('Digite el número de aristas: ')
        return 1

    def f4_input_K(self, update, context):
        self.E = update.message.text
        
        update.message.reply_text('Digite el número de máximo de aristas por vértices: ')
        return 2

    def f4(self, update, context):
        self.K = update.message.text
        name = update.message.chat.first_name
        logger.info(f"El usuario {name} ha solicitado un grafo\\.")
        aristas = self.E
        vertices = self.V
        grado = self.K
        self.hacer_grafo(int(self.V),int(self.E),int(self.K))
        img = open("src/images/grafo.png", "rb")
        update.message.reply_text(f"Número de aristas: {aristas}\nNúmero de vértices: {vertices}\nGrado máximo: {grado}")
        update.message.reply_text("La imagen se está enviando...")
        id = update.message.chat.id
        update.message.bot.sendPhoto(chat_id=id, photo=img)
        return ConversationHandler.END
    
    def dibujar_grafos(self, nodes, grafo):
        nodes = set(nodes)
        G=nx.Graph()

        for node in nodes:
            G.add_node(node)
            
        for edge in grafo:
            G.add_edge(edge[0], edge[1])

        pos = nx.shell_layout(G)
        nx.draw(G, pos)

        plot.savefig("src/images/grafo.png")
        plot.close()

    def hacer_grafo(self,n,e,k):
        grafo = []
        nodes = [] 
        
        if (n*k)/2 >= e and n>k: 
            for node in range(1,n):
                nodes.append(node)
                                
            while len(grafo) < e:  
                edge = random.randint(0,k-1)
                nodoA = random.choice(nodes) 
                
                if self.ver_peso(nodoA,grafo) <=k and (nodoA,edge) not in grafo and (edge,nodoA) not in grafo:
                    grafo.append((nodoA,edge))
                elif self.ver_peso(nodoA,grafo) > k: print(f"{nodoA}excedio el peso")

            self.dibujar_grafos(nodes, grafo)

    def ver_peso(self,node,grafo):
        cont=0
        for edge in grafo:
            if node in edge:
                cont+=1
                
        return cont

    def menu_opciones(self, update, context):
        query = update.callback_query
        query.answer()
        answer = query.data
        if answer == 'op1':
            self.f1(update, context)
        elif answer == 'op2':
            self.f2(update, context)
        elif answer == 'op3':
            self.f3(update, context)
        elif answer == 'op4':
            self.f4(update, context)