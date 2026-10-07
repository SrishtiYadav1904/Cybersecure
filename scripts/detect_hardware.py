"""
CyberGuard Hardware Profiler
Autonomously detects CPU, RAM, GPU, VRAM, and runtime environment.
Saves profile to artifacts/hardware_profile.json.
"""
import os
import json
import platform
import psutil

def detect_hardware():
    profile = {
        "os": platform.platform(),
        "python_version": platform.python_version(),
        "cpu": {
            "processor": platform.processor(),
            "physical_cores": psutil.cpu_count(logical=False),
            "logical_cores": psutil.cpu_count(logical=True),
            "cpu_freq_mhz": psutil.cpu_freq().current if psutil.cpu_freq() else None
        },
        "ram": {
            "total_gb": round(psutil.virtual_memory().total / (1024**3), 2),
            "available_gb": round(psutil.virtual_memory().available / (1024**3), 2),
            "percent_used": psutil.virtual_memory().percent
        },
        "gpu": {
            "cuda_available": False,
            "device_count": 0,
            "devices": []
        },
        "recommended_training_config": {
            "mode": "STANDARD",
            "batch_size": 32,
            "n_jobs": max(1, (psutil.cpu_count(logical=True) or 2) - 1),
            "use_gpu": False,
            "feature_dim": 414,
            "pca_components": 30,
            "subword_embed_dim": 384
        }
    }

    try:
        import torch
        if torch.cuda.is_available():
            profile["gpu"]["cuda_available"] = True
            profile["gpu"]["device_count"] = torch.cuda.device_count()
            for i in range(torch.cuda.device_count()):
                props = torch.cuda.get_device_properties(i)
                profile["gpu"]["devices"].append({
                    "id": i,
                    "name": props.name,
                    "total_vram_gb": round(props.total_memory / (1024**3), 2)
                })
            profile["recommended_training_config"]["use_gpu"] = True
    except ImportError:
        pass

    os.makedirs("artifacts", exist_ok=True)
    out_path = os.path.join("artifacts", "hardware_profile.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(profile, f, indent=2)

    print(f"Hardware profile generated: {out_path}")
    print(f"RAM: {profile['ram']['total_gb']} GB total, {profile['ram']['available_gb']} GB available")
    print(f"Logical CPUs: {profile['cpu']['logical_cores']}, Recommended n_jobs: {profile['recommended_training_config']['n_jobs']}")
    return profile

if __name__ == "__main__":
    detect_hardware()
