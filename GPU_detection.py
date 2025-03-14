import platform
import subprocess

def detect_gpu_linux():
    try:
        # Get GPU information from lspci
        result = subprocess.run(['lspci', '-nnk'], capture_output=True, text=True)
        output = result.stdout.lower()

        if 'vga' in output or '3d controller' in output:
            if 'intel' in output:
                return "Integrated GPU (Intel)"
            elif 'nvidia' in output:
                return "External GPU (NVIDIA)"
            elif 'amd' in output or 'radeon' in output:
                return "External GPU (AMD)"
            else:
                return "GPU detected but brand unknown"
        else:
            return "No GPU detected"

    except Exception as e:
        return f"Error detecting GPU: {e}"

def detect_gpu_windows():
    try:
        # Use wmic to get GPU details
        result = subprocess.run(['wmic', 'path', 'win32_videocontroller', 'get', 'caption'], capture_output=True, text=True)
        output = result.stdout.lower()

        if "intel" in output:
            return "Integrated GPU (Intel)"
        elif "nvidia" in output:
            return "External GPU (NVIDIA)"
        elif "amd" in output or "radeon" in output:
            return "External GPU (AMD)"
        else:
            return "GPU detected but brand unknown"

    except Exception as e:
        return f"Error detecting GPU: {e}"

def main():
    os_name = platform.system()

    if os_name == "Linux":
        gpu_status = detect_gpu_linux()
    elif os_name == "Windows":
        gpu_status = detect_gpu_windows()
    else:
        gpu_status = "Unsupported OS"

    print(f"GPU Detection Result: {gpu_status}")

if __name__ == "__main__":
    main()
