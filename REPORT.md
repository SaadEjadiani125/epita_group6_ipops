Part 1 – Python Environment

1. Comparing the two runs

Global execution (python3 scripts/inspect_env.py)

sys.executable: /Library/Frameworks/Python.framework/Versions/3.14/bin/python3

sys.prefix: /Library/Frameworks/Python.framework/Versions/3.14

Python version: 3.14.3

Is in virtual environment? False

Execution using uv (uv run python scripts/inspect_env.py)

sys.executable: /Users/saadejadiani/Projects/EngToolsLab2/.venv/bin/python

sys.prefix: /Users/saadejadiani/Projects/EngToolsLab2/.venv

Python version: 3.14.8

Is in virtual environment? True

Comparison and explanation

When running the script globally, Python uses the interpreter installed on my system. Its executable is located in /Library/Frameworks/Python.framework/Versions/3.14/bin/python3, and its sys.prefix points to the global Python installation. The values of sys.prefix and sys.base_prefix are identical, which indicates that Python is not running inside a virtual environment.

When running the script with uv run, a different Python interpreter is used. Its executable is located inside my project's .venv directory, and sys.prefix points to that directory. In this case, sys.prefix and sys.base_prefix are different, confirming that Python is running inside a virtual environment.

The Python versions are also different: the global execution uses Python 3.14.3, while uv run uses Python 3.14.8.

uv run automatically detects the project's virtual environment and executes the command using its Python interpreter. It also makes sure the environment is synchronized with the project's dependencies. This allows the project to use an isolated environment without manually running source .venv/bin/activate. Instead of modifying the current shell's environment, uv run handles the environment setup for the command being executed
