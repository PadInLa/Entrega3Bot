import logging
# import matlab.engine
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ConversationHandler


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

GENDER, PHOTO, LOCATION, BIO = range(4)

# eng = matlab.engine.start_matlab()
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

\- /f1: Recibe los coeficientes del polinomio característico asociado a una relación de re-currencia lineal, homogénea, con coeficientes constantes, de grado k y muestra cuál sería la forma de la solución según el teorema correspondiente.

\- /f2: Muestra la expresión con los valores de las constantes (c0,c1, . . . ,ck) y la solución de la relación de recurrencia

\- /f3: Dado  un  sitio  web  estatico, se implementa un modelo de cadenas de Markov para generar un texto ficticio

\- /f4: Genera un grafo una vez se le introduzcan los siguienters datos:
    \- E: Número de aristas\.
    \- V: Número de vértices\.
    \- K: Grado máximo de los vértices\.
    _*Comando:*_ /grafo [E, V, K]
    El comando puede ejecutarse de las siguientes formas:
    *Ejemplo:*
    1\. /grafo \[1, 2, 3\]
    2\. /grafo \(1, 2, 3\)
    3\. /grafo 1, 2, 3
        """

        # Enviar una descripción cualquieray los botones para escoger.
        update.message.reply_text(texto)

    def f1_input(self, update, context):
        logger.info("El usuario ha solicitado función generadora.")
        # Recibimos la solicitud del servidor.
        query = update.callback_query
        query.message.reply_text('Digite la ogf = f(x) = ')
        return 0
    
    def f1(self, update, context):
        ogf = update.message.text
        # eng.FGO(ogf)
        update.message.reply_text(f'El ogf es: {ogf}')
        return ConversationHandler.END
        

    def f2_input_RR(self, update, context):
        logger.info("El usuario ha solicitado su información.")
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
        # eng.coef(RR, a, i0)
        update.message.reply_text(f'el resultado es: {self.RR} {self.a} {self.i0}')
        return ConversationHandler.END
        
        
        
        

    def f3(self, update, context):
        query = update.callback_query
        query.answer()
        name = query.message.chat.first_name
        id = query.message.chat.id
        logger.info(f"El usuario {name} ha solicitado una imagen\\.")
        img = open("src/images/uninorte.jpg", "rb")
        query.bot.sendPhoto(chat_id=id, photo=img)

    def f4(self, update, context):
        name = update.message.chat.first_name
        logger.info(f"El usuario {name} ha solicitado un grafo\\.")
        info = update.message.text
        info = info.replace("/grafo", "").strip()
        try:
            values = eval(info)
            if len(values) > 3:
                update.message.reply_text("Hay un error con sus parámetros, revise e intente nuevamente\\.")
            else:
                aristas = values[0]
                vertices = values[1]
                grado = values[2]
                img = open("src/images/uninorte.jpg", "rb")
                # graficarGrafo(aristas, vertices, grado)
                update.message.reply_text(f"Número de aristas: {aristas}\nNúmero de vértices: {vertices}\nGrado máximo: {grado}")
                update.message.reply_text("La imagen se está enviando...")
                id = update.message.chat.id
                update.message.bot.sendPhoto(chat_id=id, photo=img)
        except Exception as e:
            logger.info("Ha ocurrido un error generando el grafo.")
            print(e)
            update.message.reply_text("Ha ocurrido un error. Por favor revise los parámetros e intente nuevamente.")

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
        
            