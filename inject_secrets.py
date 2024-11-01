import os
import subprocess
import json
import platform
import argparse

# Global variable for setting the default shell (can be modified if needed)
DEFAULT_SHELL = "cmd"

def detect_shell():
    """Attempt to detect the shell being used."""
    if platform.system() == "Windows":
        # Check for PowerShell or Command Prompt
        parent_process = os.getenv("COMSPEC") or os.getenv("SHELL")
        if 'powershell' in parent_process.lower():
            return 'powershell'
        return 'cmd'
    else:
        # On non-Windows systems, we assume a Bash-like environment
        return os.getenv("SHELL", "bash").split('/')[-1]

def get_op_env_vars():
    """Get environment variables that contain 'op://'."""
    op_env_vars = {key: value for key, value in os.environ.items() if value.startswith("op://")}
    return op_env_vars

def create_inject_json(op_env_vars):
    """Create the JSON payload expected by 'op inject'."""
    inject_json = {key: value for key, value in op_env_vars.items()}
    return json.dumps(inject_json)

def inject_secrets(inject_json):
    """Call `op inject` to get secrets for environment variables."""
    result = subprocess.run(['op', 'inject', '--format', 'json'], 
                            input=inject_json, capture_output=True, text=True)
    return json.loads(result.stdout)

def print_exports_for_shell(injected_secrets, shell):
    """Output the appropriate commands to export secrets based on the shell."""
    if shell == 'bash' or shell == 'zsh':
        for key, value in injected_secrets.items():
            print(f'export {key}="{value}"')
    elif shell == 'powershell':
        for key, value in injected_secrets.items():
            print(f'$env:{key}="{value}"')
    elif shell == 'cmd':
        for key, value in injected_secrets.items():
            print(f'set {key}={value}')
    else:
        raise ValueError(f"Unsupported shell: {shell}")

def main(shell=None):
    # Get environment variables that contain 'op://'
    op_env_vars = get_op_env_vars()

    # Create the `op inject` required JSON format 
    inject_json = create_inject_json(op_env_vars)
    
    # Use `op inject` to fetch the secrets
    injected_secrets = inject_secrets(inject_json)
    
    # Output the correct commands to set environment variables for the detected shell
    if not shell:
        shell = detect_shell()
    print_exports_for_shell(injected_secrets, shell)

if __name__ == "__main__":
    # Argument parser just for --shell flag
    parser = argparse.ArgumentParser(description="Inject 1Password secrets into environment variables.")
    parser.add_argument('--shell', type=str, help="Specify the shell (e.g., bash, powershell, cmd).")
    args = parser.parse_args()

    # Use the provided shell argument or fallback to default (auto detection)
    shell_to_use = args.shell or detect_shell() or DEFAULT_SHELL
    main(shell=shell_to_use)
