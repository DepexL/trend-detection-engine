# /// script
# requires-python = ">=3.11"
# dependencies = ["huggingface_hub>=0.27"]
# ///
"""
Projekto pasiruošimas: parsisiunčia duomenų rinkinius ir klonuoja reference
repozitorijas. Veikia Windows / macOS / Linux.

Paleidimas:
    uv run bootstrap.py            # duomenų rinkiniai (~760 MB)
    uv run bootstrap.py --check    # tik patikrina, ar aplinka tvarkinga
    uv run bootstrap.py --repos    # + reference repozitorijos (praktikantui nereikia šiuo metu)

Nieko mokamo, jokių raktų nereikia - visi rinkiniai vieši.
"""

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
REFS = ROOT / "refs"

# (HF dataset id, katalogas data/ viduje)
DATASETS = [
    # Išvalyta versija - pagrindinis rinkinys 1 užduočiai.
    (
        "SupritiVijay/tool-reasoning-sft-RESEARCH-dr-tulu-sft-deep-research-agent-data-cleaned-rectified",
        "dr-tulu-sft-cleaned",
    ),
    # Originalas - palyginimui su išvalytu.
    ("rl-research/dr-tulu-sft-data", "dr-tulu-sft-original"),
    # RL užduočių pavyzdžiai - maži, bet pravers vėliau.
    ("rl-research/dr-tulu-rl-data", "dr-tulu-rl"),
]

# (git url, katalogas refs/ viduje)
# Skaitymui projektuojant agentą ir mokymą - praktikanto užduotims NEreikalingos,
# todėl klonuojamos tik su --repos.
REPOS = [
    ("https://github.com/langchain-ai/local-deep-researcher.git", "local-deep-researcher"),
    ("https://github.com/OpenPipe/ART.git", "openpipe-art"),
    ("https://github.com/unslothai/unsloth.git", "unsloth"),
    ("https://github.com/vllm-project/vllm.git", "vllm"),
]


def check_environment() -> bool:
    ok = True

    if shutil.which("git"):
        ver = subprocess.run(
            ["git", "--version"], capture_output=True, text=True
        ).stdout.strip()
        print(f"  [ok] {ver}")
    else:
        print("  [!!] git nerastas - įsidiek: https://git-scm.com/downloads")
        ok = False

    print(f"  [ok] Python {sys.version.split()[0]}")

    try:
        import huggingface_hub  # noqa: F401

        print(f"  [ok] huggingface_hub {huggingface_hub.__version__}")
    except ImportError:
        print("  [!!] huggingface_hub neįsidiegė - ar leidi per 'uv run'?")
        ok = False

    return ok


def download_datasets() -> None:
    from huggingface_hub import snapshot_download

    DATA.mkdir(exist_ok=True)
    for repo_id, dirname in DATASETS:
        target = DATA / dirname
        print(f"\n==> {repo_id}")
        snapshot_download(
            repo_id=repo_id,
            repo_type="dataset",
            local_dir=target,
        )
        print(f"    -> {target}")


def clone_repos() -> None:
    REFS.mkdir(exist_ok=True)
    for url, dirname in REPOS:
        target = REFS / dirname
        if (target / ".git").exists():
            print(f"==> {dirname} jau klonuotas, praleidžiam")
            continue
        print(f"==> klonuojam {dirname}")
        subprocess.run(
            ["git", "clone", "--depth", "1", "--quiet", url, str(target)],
            check=True,
        )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="tik patikrinti aplinką, nieko nesiųsti",
    )
    parser.add_argument(
        "--repos",
        action="store_true",
        help="papildomai klonuoti reference repozitorijas (praktikantui nereikia)",
    )
    args = parser.parse_args()

    print("Aplinkos patikra:")
    if not check_environment():
        print("\nSutvarkyk, kas pažymėta [!!], ir paleisk iš naujo.")
        return 1

    if args.check:
        print("\nViskas tvarkoje. Pilnas paleidimas: uv run bootstrap.py")
        return 0

    download_datasets()
    if args.repos:
        print()
        clone_repos()

    print(f"""
Baigta.
  duomenys -> {DATA}{f'''
  repos    -> {REFS}''' if args.repos else ''}
""")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
