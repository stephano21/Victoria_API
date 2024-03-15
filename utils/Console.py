from colorama import init, Fore, Style

# Inicializa colorama
class Console:
    init()
    def __init__(self):
        pass
    def Error(message):
        print(f"❌ {Fore.RED}[ERROR]{Fore.WHITE} {message}")

    def Warning(message):
        print(f"☢️  {Fore.YELLOW}[WARNING]{Fore.WHITE} {message}")

    def Log(message):
        print(f"✅ {Fore.GREEN}[INFO]{Fore.WHITE} {message}")

