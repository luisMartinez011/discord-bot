import discord
import json
import os

# Crea un cliente de Discord
intents = discord.Intents.all()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    #Mensaje de bienvenida
    print('Bot conectado como {0.user}'.format(client))




@client.event
async def on_message(message):
    # Verifica que el mensaje provenga de un usuario y no del bot
    if message.author == client.user:
        return 
    
        # Verifica si el mensaje fue enviado en el canal "noticias-deportivas"
    if str(message.channel) == "noticias-deportivas":
        await message.channel.send(f'¡Hola {message.author.display_name}! Para configurar tus preferencias deportivas, usa el comando !configurar.')

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
            deporte = 'general'

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
                await message.channel.send('¿Cuál es el nombre de la fuente?')
                respuesta_nombre_fuente = await client.wait_for('message', check=lambda m: m.author == message.author)
                fuente = "si"
        if(fuente == "si"): 
            fuente = respuesta_nombre_fuente.content
        else:fuente = 'todas'
          
        frecuencia = None
        while frecuencia not in ['diario', 'semanal', 'mensual']:
            await message.channel.send('¿Con qué frecuencia deseas recibir noticias? (diario/semanal/mensual)')
            respuesta_frecuencia = await client.wait_for('message', check=lambda m: m.author == message.author)
            frecuencia = respuesta_frecuencia.content.lower()
            
        # diccionario con la configuración
        configuracion = {
            'deporte': deporte,
            'fuente': fuente,
            'frecuencia': frecuencia
        }

        # configuración a formato JSON
        configuracion_json = json.dumps(configuracion)
        print(configuracion_json)

        #TODO  Envía la configuración al backend


        await message.channel.send('¡Gracias! Tus preferencias han sido guardadas exitosamente. Aquí están tus preferencias:\n\nDeporte: {}\nFuente: {}\nFrecuencia: {}'.format(configuracion['deporte'], configuracion['fuente'], configuracion['frecuencia']))

# Token de autenticación del bot de Discord   se ocupa generar un token en https://discord.com/developers/applications
# y usarala como variable de entorno
token = os.getenv('DISCORD_TOKEN')
# Inicia el bot de Discord
client.run(token)
