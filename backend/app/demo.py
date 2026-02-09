import subprocess
import time
import sys
import httpx


def run_command(command, cwd=None):
    try:
        subprocess.run(command, check=True, shell=True, cwd=cwd)
    except subprocess.CalledProcessError:
        print(f"Error running command: {command}")
        sys.exit(1)


def main():
    print("Starting EX3 End-to-End Demo...")

    # 1. Verify Docker installation
    print("Checking Docker...")
    try:
        subprocess.run(["docker", "--version"], check=True, stdout=subprocess.DEVNULL)
    except Exception:
        print("Docker is not installed or not in PATH.")
        sys.exit(1)

    # 2. Start services
    print("Starting services with 'compose.yaml'...")
    # Using Docker Compose v2
    run_command("docker compose up -d --build")

    # 3. Wait for Health
    print("Waiting for Main Backend health...")
    backend_url = "http://localhost:8000/health"
    retries = 30
    for i in range(retries):
        try:
            response = httpx.get(backend_url)
            if response.status_code == 200:
                print("Backend is HEALTHY.")
                break
        except Exception:
            pass
        print(f"Waiting... ({i + 1}/{retries})")
        time.sleep(2)
    else:
        print("Backend failed to become healthy.")
        # Retrieve logs for debugging
        run_command("docker compose logs main-backend")
        sys.exit(1)

    print("\nStack is ready!")
    print("Frontend: http://localhost:8501")
    print("Backend:  http://localhost:8000")
    print("AI Service is running internally.")

    print("\nInstructions for Manual Verification (Video Recording):")
    print("1. Open http://localhost:8501")
    print("2. Create a new creature (e.g. 'Griffon').")
    print("3. Verify the avatar is generated.")
    print("4. Verify the creature appears in the list.")

    input("\nPress Enter to stop the stack and exit...")
    run_command("docker compose down")
    print("Demo stopped.")


if __name__ == "__main__":
    main()
