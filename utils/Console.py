from colorama import init, Fore

# Inicializa colorama
class console:
    init()
    def __init__(self):
        pass
    def error(message):
        print(f"❌ {Fore.RED}[ERROR]{Fore.WHITE} {message}")

    def warn(message):
        print(f"☢️  {Fore.YELLOW}[WARNING]{Fore.WHITE} {message}")

    def log(message):
        print(f"✅ {Fore.GREEN}[INFO]{Fore.WHITE} {message}")

