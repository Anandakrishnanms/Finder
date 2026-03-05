#!/usr/bin/env python3
import subprocess
import os
import shutil
import sys

# ===== Required Tools =====
REQUIRED_TOOLS = ["subfinder", "assetfinder", "sublist3r", "httprobe"]

# ===== Dependency Check =====
def check_dependencies():
    print("[*] Checking required tools...\n")
    missing = []

    for tool in REQUIRED_TOOLS:
        if shutil.which(tool) is None:
            missing.append(tool)

    if missing:
        print("[!] Missing tools detected:")
        for m in missing:
            print(f"   - {m}")

        print("\nRun: python3 finder.py --install")
        sys.exit(1)

    print("[✔] All required tools are installed.\n")


# ===== Auto Installer =====


# ===== Banner =====
def banner():
    print(r"""
███████╗██╗███╗   ██╗██████╗ ███████╗██████╗ 
██╔════╝██║████╗  ██║██╔══██╗██╔════╝██╔══██╗
█████╗  ██║██╔██╗ ██║██║  ██║█████╗  ██████╔╝
██╔══╝  ██║██║╚██╗██║██║  ██║██╔══╝  ██╔══██╗
██║     ██║██║ ╚████║██████╔╝███████╗██║  ██║
╚═╝     ╚═╝╚═╝  ╚═══╝╚═════╝ ╚══════╝╚═╝  ╚═╝
""")
    print("              🔎 FINDER 🔎")
    print("        Professional Recon Framework")
    print("               Author: ZeKken")
    print("=" * 60)


# ===== Run Tool =====
def run_tool(command, tool_name, input_data=None):
    print(f"[*] Running {tool_name}...")
    try:
        result = subprocess.run(
            command,
            input=input_data,
            capture_output=True,
            text=True
        )
        return result.stdout.splitlines()
    except Exception as e:
        print(f"[!] Error running {tool_name}: {e}")
        return []


# ===== Clean Results =====
def clean_results(results, domain):
    cleaned = set()
    for line in results:
        line = line.strip()
        if domain in line and not line.startswith("#") and line != "":
            cleaned.add(line)
    return cleaned


# ===== Main =====
if __name__ == "__main__":

    # 🔥 Installer Mode
    if "--install" in sys.argv:
        auto_install()

    banner()

    # 🔎 Check dependencies before scanning
    check_dependencies()

    domain = input("Enter target domain: ").strip()

    # Run enumeration tools
    subfinder_results = run_tool(
        ["subfinder", "-silent", "-d", domain],
        "Subfinder"
    )

    assetfinder_results = run_tool(
        ["assetfinder", "--subs-only", domain],
        "Assetfinder"
    )

    sublist3r_results = run_tool(
        ["sublist3r", "-d", domain, "-o", "/dev/stdout"],
        "Sublist3r"
    )

    # Combine results
    all_results = subfinder_results + assetfinder_results + sublist3r_results

    # Remove duplicates
    unique_subdomains = clean_results(all_results, domain)

    print(f"\n[+] Total unique subdomains found: {len(unique_subdomains)}")

    # ===== Run httprobe to check live subdomains =====
    if unique_subdomains:
        live_results = run_tool(
            ["httprobe"],
            "httprobe (Live Check)",
            input_data="\n".join(unique_subdomains)
        )

        print("\n🌐 Live Subdomains:\n")
        for live in sorted(set(live_results)):
            print(live)

        print(f"\n[*] Total Live: {len(set(live_results))}")
    else:
        print("\n[!] No subdomains found.")
