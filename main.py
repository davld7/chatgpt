import openai
import config
import typer
from rich import print
from rich.table import Table
"""
Al comienzo del programa, importa los módulos necesarios, incluidos openai,
config.py (archivo con la clave API), typer, Table y print desde rich.
"""

"""
main(): Esta es la función principal que ejecuta todo el programa.
Configura la clave API y crea un contexto inicial para el asistente de IA.
Luego crea un ciclo donde puede ingresar entradas de chat y recibir respuestas del asistente.
"""
def main():
    openai.api_key = config.api_key

    print("\n🗨️ [bold blue]ChatGPT API con Python.[/bold blue]\n")
    table = Table("Comando", "Descripción")
    table.add_row("exit", "Salir de la aplicación")
    table.add_row("new", "Crear una nueva conversación")
    table.add_row("context", "Cambiar el contexto del asistente")
    print(table)
    """
    Luego, el programa presenta una tabla de comandos disponibles al usuario mediante la función
    Table().
    """

    # Contexto inicial del asistente
    initial_context = {"role": "system", "content": "Eres un asistente muy útil"}
    context = initial_context
    messages = [context]
    """
    Luego, el programa define el contexto inicial para el asistente de IA, que es un diccionario
    con dos partes, "rol" y "contenido", que representan el propósito del contexto y
    el contenido del texto del contexto, respectivamente.
    """

    while True:
        content = __prompt()

        if content == "new":
            print("\n🗨️ ¡Nueva conversación creada!")
            context = initial_context
            messages = [context]
            content = __prompt()

        # Cambiar el contexto del asistente
        if content == "context":            
            context_content = typer.prompt("\n¿Cuál es el nuevo contexto?")
            context = {"role": "system", "content": context_content}
            messages = [context]
            content = __prompt()
            
        messages.append({"role": "user", "content": content})

        response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)

        response_content = response.choices[0].message.content

        messages.append({"role": "assistant", "content": response_content})
        """
        Luego, el programa ingresa a un ciclo donde recopila la entrada del usuario, agrega
        la entrada del usuario a una lista de mensajes, solicita a la IA que genere una respuesta
        basada en la lista de mensajes proporcionados y agrega la respuesta resultante a la
        lista de mensajes.
        """

        # Respuesta generada por el asistente
        print(f"\n[bold green]> [/bold green] [green]{response_content}[/green]")

"""
__prompt(): esta es una función de ayuda que recupera la entrada del usuario (un prompt)
durante la conversación. También maneja el caso en el que el usuario quiere salir del programa.
"""
def __prompt() -> str:
    prompt = typer.prompt("\nprompt")

    if prompt == "exit":
        exit = typer.confirm("\n¿Estás seguro?🖐️")
        if exit:
            print("\n¡Hasta luego!👋\n")
            raise typer.Exit
        return __prompt()
    
    return prompt

"""
La línea if __name__ == "__main__": se utiliza para comprobar si el script se está ejecutando
como un programa principal, es decir, si se ha ejecutado desde la línea de comandos o consola,
y que no se ha importado como un módulo a otro script. 

Si la línea anterior es verdadera, entonces typer.run(main) es llamado. Esto ejecutará la
función main que contiene el código principal del programa.  
"""
if __name__ == "__main__":
    typer.run(main)