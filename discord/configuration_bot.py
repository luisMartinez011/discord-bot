import discord
import json
import os
import requests
from dotenv import load_dotenv

load_dotenv()

# * Se cargan las variables de entorno
token = os.getenv('DISCORD_TOKEN')
public_key = os.getenv('DISCORD_PUBLIC_KEY')
task_scheduler_link = os.getenv('TASK_SCHEDULER_LAMBDA')

# Crea un cliente de Discord
intents = discord.Intents.all()
client = discord.Client(intents=intents)

mensaje_inicial_enviado = False

@client.event
async def on_ready():
    #Mensaje de bienvenida
    print('Bot conectado como {0.user}'.format(client))


bienvenida = f"soy SBotNews\nMe ecargare de mantenerte informado sobre las nuevas actualizaciones en tus preferencias deportivas, solo hagamos algunas configuraciones antes, escribe ok para continuar"

@client.event
async def on_member_join(member):
    global bienvenida
    canal_bienvenida = discord.utils.get(member.guild.channels, name='noticias-deportivas')
    welcome_message = f"Hola {member.mention}, {bienvenida}"
    await canal_bienvenida.send(welcome_message)



@client.event
async def on_message(message):
    global mensaje_inicial_enviado
    # Verifica que el mensaje provenga de un usuario y no del bot
    if message.author == client.user:
        return

        # Verifica si el mensaje fue enviado en el canal "noticias-deportivas"
    if str(message.channel) == "noticias-deportivas" and not mensaje_inicial_enviado:
        await message.channel.send(f'¡Hola {message.author.display_name}! Para configurar tus preferencias deportivas, usa el comando !configurar.')
        mensaje_inicial_enviado = True

    # Verifica si el mensaje es el comando de configuración inicial
    if message.content.startswith('!configurar'):
        # Obtiene la respuesta del usuario
        await message.channel.send('¿Deseas noticias de un deporte en específico? (sí/no)')
        respuesta_deporte = await client.wait_for('message', check=lambda m: m.author == message.author)
        deporte_respuesta = respuesta_deporte.content.lower()

        # Valida la respuesta del usuario
        while deporte_respuesta not in ['si', 'no']:
            await message.channel.send('Respuesta inválida. ¿Deseas noticias de un deporte en específico? (sí/no)')
            respuesta_deporte = await client.wait_for('message', check=lambda m: m.author == message.author)
            deporte_respuesta = respuesta_deporte.content.lower()

        # Si el usuario responde "sí", pregunta por el deporte específico
        if deporte_respuesta == 'si':
            deporte = None
            while deporte not in ['futbol', 'basquetbol', 'beisbol']:
                await message.channel.send('¿Cuál es el deporte que te interesa? (futbol/basquetbol/beisbol)')
                deporte_respuesta = await client.wait_for('message', check=lambda m: m.author == message.author)
                deporte = deporte_respuesta.content.lower()

        else:
            deporte = 'No'

        fuente = None
        while fuente not in ['si', 'no']:
            await message.channel.send('¿Deseas noticias de una fuente específica? (sí/no)')
            respuesta_fuente = await client.wait_for('message', check=lambda m: m.author == message.author)
            respuesta_fuente = respuesta_fuente.content.lower()
            while respuesta_fuente not in ['si', 'no']:
                await message.channel.send('Respuesta invalida. ¿Deseas noticias de una fuente específica? (sí/no)')
                respuesta_fuente = await client.wait_for('message', check=lambda m: m.author == message.author)
                respuesta_fuente = respuesta_fuente.content.lower()
            if respuesta_fuente == 'no':
                fuente = respuesta_fuente
            elif respuesta_fuente == 'si':
                await message.channel.send('¿Cuál es el nombre de la fuente? (As, Espn, Fansided)')
                respuesta_nombre_fuente = await client.wait_for('message', check=lambda m: m.author == message.author)
                fuente = "si"
        if(fuente == "si"):
            fuente = respuesta_nombre_fuente.content
        else:fuente = 'todas'

        frecuencia = None

        #TODO: Hacer una comprabacion donde solo se acepten numeros
        while frecuencia== None:
            await message.channel.send('¿Con qué frecuencia deseas recibir noticias? (solo poner la cantidad de horas en numero ej: 1)')
            respuesta_frecuencia = await client.wait_for('message', check=lambda m: m.author == message.author)
            frecuencia = respuesta_frecuencia.content.lower()

        # diccionario con la configuración
        configuracion = {
            'deporte': deporte,
            'fuente': fuente,
            'frecuencia': frecuencia,
            #TODO: Poner un nombre del server
            'nombre_server': "T1"
        }

        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }

        # Realizar la solicitud GET con un cuerpo
        response = requests.get(task_scheduler_link, json=configuracion, headers=headers)
        print(response)


        # configuración a formato JSON
        configuracion_json = json.dumps(configuracion)
        print(configuracion_json)

        #TODO  Envía la configuración al backend


        await message.channel.send('¡Gracias! Tus preferencias han sido guardadas exitosamente. Aquí están tus preferencias:\n\nDeporte: {}\nFuente: {}\nFrecuencia: {}'.format(configuracion['deporte'], configuracion['fuente'], configuracion['frecuencia']))

# Inicia el bot de Discord
client.run(token)
