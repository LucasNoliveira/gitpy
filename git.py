import subprocess
import re

def git_status():
    try:
        result = subprocess.run(["git", "status", "-s"], check=True, capture_output=True, text=True)
        modified_files = [file.strip() for file in result.stdout.strip().split('\n') if file.strip()]
        files_dict = {str(index + 1): re.sub(r'^M\s+', '', file) for index, file in enumerate(modified_files)}

        if not files_dict:
            print("Sem arquivos modificados.")
            return {}

        print("Arquivos modificados:")
        for index, file in files_dict.items():
            print(f"{index}: {file}")

        return files_dict
    except subprocess.CalledProcessError as e:
        print(f"Erro ao obter o status dos arquivos: {e}")
        return {}

def git_add(files):
    try:
        subprocess.run(["git", "add"] + files, check=True)
        print("Arquivos adicionados com sucesso.")
    except subprocess.CalledProcessError as e:
        print(f"Erro ao adicionar arquivos: {e}")

def git_commit(message):
    try:
        subprocess.run(["git", "commit", "-m", message], check=True)
        print("Commit realizado com sucesso.")
    except subprocess.CalledProcessError as e:
        print(f"Erro ao realizar o commit: {e}")

def git_push(branch='main'):
    try:
        subprocess.run(["git", "push", "origin", branch], check=True)
        print("Push realizado com sucesso.")
    except subprocess.CalledProcessError as e:
        print(f"Erro ao realizar o push: {e}")

if __name__ == "__main__":
    files_dict = git_status()
    if files_dict:
        selected_numbers = input("Digite os números dos arquivos a serem adicionados (separados por espaço): ").split()
        files = [files_dict[num] for num in selected_numbers if num in files_dict]
        if files:
            commit_message = input("Digite a mensagem do commit: ")

            git_add(files)
            git_commit(commit_message)
            git_push()
        else:
            print("Nenhum arquivo selecionado para adicionar.")
