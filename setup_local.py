import os
import subprocess
import sys
from pathlib import Path

# Caminho do ambiente virtual
venv_path = Path(".venv")
requirements = Path("requirements.txt")

def run(cmd, shell=False):
    """Executa comandos de terminal com saída visível."""
    print(f"\n🛠️  Executando: {cmd}")
    subprocess.run(cmd, shell=shell, check=False)

def criar_venv():
    print("\n🐍 Criando ambiente virtual...")
    run([sys.executable, "-m", "venv", ".venv"])

def instalar_dependencias():
    print("\n📦 Instalando dependências...")
    if requirements.exists():
        run([f"{venv_path}/Scripts/pip", "install", "-r", "requirements.txt"], shell=True)
    else:
        run([f"{venv_path}/Scripts/pip", "install", "pandas", "streamlit", "jupyter"], shell=True)
        run([f"{venv_path}/Scripts/pip", "freeze", ">", "requirements.txt"], shell=True)
    print("\n✅ Dependências instaladas e registradas em requirements.txt")

def mostrar_status_git():
    print("\n🔍 Status do Git:")
    run(["git", "status"], shell=True)
    print("\n💡 Para enviar alterações:")
    print("   git add . && git commit -m 'mensagem' && git push origin main")

def instrucoes_finais():
    print("\n🚀 Ambiente configurado com sucesso!")
    print("💻 Para ativar o ambiente:")
    if os.name == "nt":
        print("   .venv\\Scripts\\activate")
    else:
        print("   source .venv/bin/activate")
    print("\n📘 Para abrir o notebook:")
    print("   jupyter notebook")
    print("\n🌐 Para rodar o app Streamlit:")
    print("   streamlit run app.py")

def main():
    print("🧩 Configurando ambiente local do projeto...\n")

    # 1. Cria o ambiente virtual se não existir
    if not venv_path.exists():
        criar_venv()
    else:
        print("✅ Ambiente virtual já existe.")

    # 2. Instala dependências
    instalar_dependencias()

    # 3. Mostra status do repositório
    mostrar_status_git()

    # 4. Instruções finais
    instrucoes_finais()

if __name__ == "__main__":
    main()
