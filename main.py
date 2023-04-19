import openai
import config
import typer
from rich import print
from rich.table import Table

def main():
    openai.api_key = config.api_key

    print("\n🗨️ [bold blue]ChatGPT API con Python.[/bold blue]\n")
    table = Table("Comando", "Descripción")
    table.add_row("exit", "Salir de la aplicación")
    table.add_row("new", "Crear una nueva conversación")
    table.add_row("context", "Cambiar el contexto del asistente")
    print(table)

    # Contexto inicial del asistente
    initial_context = {"role": "system", "content": "Eres un asistente muy útil"}
    context = initial_context
    messages = [context]

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

        print(f"\n[bold green]> [/bold green] [green]{response_content}[/green]")

def __prompt() -> str:
    prompt = typer.prompt("\nprompt")

    if prompt == "exit":
        exit = typer.confirm("\n¿Estás seguro?🖐️")
        if exit:
            print("\n¡Hasta luego!👋\n")
            raise typer.Exit
        return __prompt()
    
    return prompt

if __name__ == "__main__":
    typer.run(main)