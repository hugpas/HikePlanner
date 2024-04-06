import subprocess
import sys

def run_command(command):
    try:
        subprocess.run(command, check=True, shell=True)
    except subprocess.CalledProcessError as e:
        print(f"Fehler beim Ausführen des Befehls: {e.cmd}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Verwendung: python update_container.py <AZURE_STORAGE_CONNECTION_STRING>")
        sys.exit(1)

    azure_storage_connection_string = sys.argv[1]

    # Zieht das neueste Docker-Image
    run_command("docker pull hugpas05/hikeplanner:latest")

    # Stoppt den laufenden Container
    run_command("docker stop hikeplanner || true")

    # Entfernt den gestoppten Container
    run_command("docker rm hikeplanner || true")

    # Startet einen neuen Container mit dem aktualisierten Image
    run_command(f"docker run --name hikeplanner -e AZURE_STORAGE_CONNECTION_STRING='{azure_storage_connection_string}' -p 9001:80 -d hugpas05/hikeplanner")

    # Restartet die Azure Container Instance
    run_command("az container restart --resource-group mdm-hikeplanner --name mdm-hikeplanner")
