import os
import re
import subprocess

# Caminho da pasta do projeto
project_path = "."

# Expressão regular para capturar imports
pattern = re.compile(r'^\s*(?:import|from)\s+([\w\-\.]+)')

libs = set()

# --- Coleta os imports de todos os .py ---
ignore_dirs = {".venv", "venv", "__pycache__", ".ipynb_checkpoints", ".streamlit"}

for root, dirs, files in os.walk(project_path):
    # remove diretórios indesejados da varredura
    dirs[:] = [d for d in dirs if d not in ignore_dirs]

    for file in files:
        if file.endswith(".py"):
            file_path = os.path.join(root, file)
            try:
                with open(file_path, encoding="utf-8") as f:
                    lines = f.readlines()
            except UnicodeDecodeError:
                try:
                    with open(file_path, encoding="latin-1") as f:
                        lines = f.readlines()
                    print(f"⚠️  Aviso: {file_path} contém caracteres não UTF-8 (usando latin-1).")
                except Exception as e:
                    print(f"❌ Erro ao ler {file_path}: {e}")
                    continue  # pula o arquivo problemático

            for line in lines:
                match = pattern.match(line)
                if match:
                    lib = match.group(1).split('.')[0]
                    libs.add(lib)

# --- Mapeamento para nomes reais de pacotes no PyPI (corrige nomes internos) ---
substituicoes = {
    "sklearn": "scikit-learn",
    "cv2": "opencv-python",
    "PIL": "Pillow",
    "yaml": "PyYAML"
}

libs_final = sorted({substituicoes.get(lib, lib) for lib in libs})

import sys as _sys
import pkgutil

# --- Remove módulos da biblioteca padrão do Python ---
# Coleta todos os módulos nativos disponíveis
modulos_padroes = {m.name for m in pkgutil.iter_modules()}
modulos_padroes.update({
    "os", "sys", "io", "re", "pathlib", "tempfile", "subprocess", "json", "typing"
})

# Remove pacotes que fazem parte da stdlib
libs_final = sorted({substituicoes.get(lib, lib) for lib in libs if lib not in modulos_padroes})

print("\n📦 Pacotes detectados (após filtragem):")
for lib in libs_final:
    print(f"  - {lib}")

# --- Captura versões instaladas via pip show ---
def get_version(package):
    try:
        out = subprocess.check_output(["pip", "show", package], text=True)
        for line in out.splitlines():
            if line.startswith("Version:"):
                return line.split(":", 1)[1].strip()
    except subprocess.CalledProcessError:
        return None

requirements = []
for lib in libs_final:
    version = get_version(lib)
    if version:
        requirements.append(f"{lib}=={version}")
    else:
        requirements.append(lib)

# --- Salva o requirements.txt ---
with open("requirements.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(requirements))

print("\n✅ Arquivo requirements.txt gerado com sucesso!")
print("Conteúdo final:\n" + "-" * 40)
print("\n".join(requirements))
print("-" * 40)

