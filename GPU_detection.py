import platform
import subprocess

def enumerate_gpus_linux():
    try:
        # Run lspci command and filter VGA/3D controllers
        result = subprocess.run(['lspci', '-nnk'], capture_output=True, text=True)
        output = result.stdout.lower()

        gpu_list = []
        lines = output.split("\n")
        for i, line in enumerate(lines):
            if "vga" in line or "3d controller" in line:
                gpu_info = line.strip()
                
                # Check the next lines for driver details
                vendor = "Unknown GPU"
                if "intel" in gpu_info:
                    vendor = "Integrated GPU (Intel)"
                elif "nvidia" in gpu_info:
                    vendor = "External GPU (NVIDIA)"
                elif "amd" in gpu_info or "radeon" in gpu_info:
                    vendor = "External GPU (AMD)"
                
                # Append GPU info to list
                gpu_list.append(f"{vendor}: {gpu_info}")

        return gpu_list if gpu_list else ["No GPU detected"]

    except Exception as e:
        return [f"Error detecting GPUs: {e}"]

def enumerate_gpus_windows():
    try:
        # Use WMIC to list all GPUs
        result = subprocess.run(['wmic', 'path', 'win32_videocontroller', 'get', 'caption'], capture_output=True, text=True)
        output = result.stdout.strip().split("\n")[1:]  # Skip the header

        gpu_list = [gpu.strip() for gpu in output if gpu.strip()]
        return gpu_list if gpu_list else ["No GPU detected"]

    except Exception as e:
        return [f"Error detecting GPUs: {e}"]

def main():
    os_name = platform.system()

    if os_name == "Linux":
        gpu_list = enumerate_gpus_linux()
    elif os_name == "Windows":
        gpu_list = enumerate_gpus_windows()
    else:
        gpu_list = ["Unsupported OS"]

    print("\n=== GPU Enumeration Results ===")
    for gpu in gpu_list:
        print(gpu)

if __name__ == "__main__":
    main()
