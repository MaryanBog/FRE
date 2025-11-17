# run_tests.py
# Adds the correct src path to PYTHONPATH and runs pytest.

import sys
import subprocess
import pathlib
import os

def main():
    project_root = pathlib.Path(__file__).resolve().parent
    src_dir = project_root / "src"
    tests_dir = project_root / "tests"

    print("Project root:", project_root)
    print("src:", src_dir)
    print("tests:", tests_dir)

    if not src_dir.exists():
        print("ERROR: src directory not found:", src_dir)
        sys.exit(1)

    # Add src/ to PYTHONPATH
    env = os.environ.copy()
    env["PYTHONPATH"] = str(src_dir)

    print("PYTHONPATH set to:", env["PYTHONPATH"])
    print("\nRunning pytest...\n")

    result = subprocess.run(
        [sys.executable, "-m", "pytest", "-q"],
        env=env,
        cwd=str(project_root)
    )

    if result.returncode == 0:
        print("\nALL TESTS PASSED")
    else:
        print("\nTESTS FAILED")
        sys.exit(result.returncode)

if __name__ == "__main__":
    main()
