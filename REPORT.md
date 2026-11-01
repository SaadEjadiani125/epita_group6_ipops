# TP 2 — Student Report: Modern Python Tooling & Live API Systems

Student Name: Saad Ejadiani  
EPITA Login: saad.ejadiani@epita.fr  
Assigned API Group: Group 6 — Geolocation & IP Ops (IPinfo.io)  
Date: 31/10/2026  
TestPyPI Live Package URL:** To be completed after deployment.

---

## Step 0: Assigned Group Verification

- Group Command Output:
- Assigned Domain: Group 6 — Geolocation & IP Ops (IPinfo.io)
- Project Directory Name: EngToolsLab2 

---

## Part 1: Environment Isolation with `uv`

### 1. Comparison of `sys.executable` & `sys.prefix`

[Global sys.executable]: /Library/Frameworks/Python.framework/Versions/3.14/bin/python3

[uv sys.executable]: /Users/saadejadiani/Projects/EngToolsLab2/.venv/bin/python

[Global sys.prefix]: /Library/Frameworks/Python.framework/Versions/3.14

[uv sys.prefix]: /Users/saadejadiani/Projects/EngToolsLab2/.venv

**Analysis:**

The global Python interpreter uses the system-wide Python installation, whereas `uv run` executes the script using the project's virtual environment. This isolates the project's dependencies from the global Python installation. Unlike manually activating a virtual environment, `uv run` automatically selects the correct environment when executing a command.

---

## Part 2: Live API Connection & 12-Factor Secret Hygiene

### 1. Git Status Output:
$ git status

On branch main

Your branch is up to date with 'origin/main'.

Changes to be committed:

   (use "git restore --staged <file>..." to unstage)

	 new file:   .env.template

Changes not staged for commit:

  (use "git add <file>..." to update what will be committed)

  (use "git restore <file>..." to discard changes in working directory)

	modified:   .gitignore

	modified:   REPORT.md

	modified:   pyproject.toml

	modified:   uv.lock

Untracked files:

  (use "git add <file>..." to include in what will be committed)

	scripts/test_api.py

	src/engtoolslab2/client.py

	src/engtoolslab2/config.py
### 2. Live API Response (Redacted)

```json
{
  "status": "LIVE_SUCCESS",
  "ip": "[REDACTED]",
  "city": "Le Kremlin-Bicêtre",
  "region": "Île-de-France",
  "country": "FR",
  "org": "AS56339 Ionis Group - Ionis Schools of Technology and Management SAS"
}
```

### 3. Security Analysis

**Why is storing secrets in environment variables superior to putting them in configuration files like `config.json` or `settings.yaml`?**

1. Environment variables keep sensitive credentials separate from source code, reducing the risk of accidentally exposing API keys when sharing or pushing a project to GitHub.

2. They allow different credentials to be used in development and production without modifying application code, making credential management and rotation easier.

**Why are default fallbacks like `os.getenv("API_KEY", "default")` dangerous for production secrets?**

A default fallback can hide missing configuration by silently using an invalid or insecure credential. This can make configuration errors difficult to detect. Production secrets should be explicitly provided and validated.

## Part 3: Dependency Hygiene & Semantic Versioning

### 1. Dependency Tree (`uv tree`)


engtoolslab2 v0.1.0
├── python-dotenv v1.2.4
├── requests v2.34.2
│   ├── certifi v2026.10.23
│   ├── charset-normalizer v3.5.2
│   ├── idna v3.20
│   └── urllib3 v2.8.0
├── rich v15.0.0
│   ├── markdown-it-py v4.2.0
│   │   └── mdurl v0.1.2
│   └── pygments v2.21.0
└── pytest v9.2.0 (group: dev)
    ├── iniconfig v2.3.1
    ├── packaging v26.3
    ├── pluggy v1.7.0
    └── pygments v2.21.0


- **Direct dependencies:** 

      python-dotenv, requests, and rich. pytest is a development-only dependency.

- **Transitive dependencies pulled in by `requests` / `rich`:

	- requests: certifi, charset-normalizer, idna, urllib3.

	- rich: markdown-it-py, pygments.

	- markdown-it-py: mdurl.

### 2. Lockfile & SemVer Analysis
1. **Meaning of version specifiers:**

   - `requests = "^2.31.0": Allows versions from 2.31.0 up to, but not including, 3.0.0.

   - urllib3 = "~=2.2.1": Allows versions from 2.2.1 up to, but not including, 2.3.0.

   - rich = "==13.7.1": Allows only version 13.7.1.

2. **If an upstream author releases `3.0.0`, will `^2.31.0` install it? Why or why not?**  
  
	 No. The caret constraint allows compatible updates within major version 2 but excludes 	 version 3.0.0. Even when using uv lock --upgrade, uv respects the declared version 		constraint.

3. **What is the fundamental difference between `pyproject.toml` (declaration) and `uv.lock` (pinning)?**  

   -pyproject.toml declares the project's dependencies and their allowed version ranges.uv.lock records the exact versions selected for the project, including transitive dependencies and package hashes. This makes installations more consistent and reproducible.

4. **How do the SHA-256 cryptographic hashes in `uv.lock` protect against supply chain attacks?**  

 The `uv.lock` file contains SHA-256 hashes for package files, including their source distributions and wheels. These hashes allow `uv` to verify the integrity of downloaded packages. When a package is downloaded, its hash can be compared with the expected hash in the lockfile. If they do not match, this can indicate that the file has been corrupted or modified. This helps protect against certain supply-chain attacks by detecting unexpected changes to package files. 




## Part 4: Package Build & TestPyPI Deployment

### 1. TestPyPI Deployment Details

- **TestPyPI Package Name:** `epita_saadejadiani_ipops`
- **Public URL:** https://test.pypi.org/project/epita-saadejadiani-ipops/

- **CLI installation and execution output:**

The package was installed and executed from the `/tmp` directory, outside the original project directory.

Command used:

```bash
uv run --with epita-saadejadiani-ipops --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ epita-saadejadiani-cli
```

Execution output:

Installed 11 packages

EPITA Engineering Tools — Session 2

Live System Telemetry: LIVE_SUCCESS

Property       Value
status         LIVE_SUCCESS
ip             [Public IP address]
city           Paris
region         Île-de-France
country        FR
org            AS5410 Bouygues Telecom SA


The installation and execution were successful. The CLI retrieved live geolocation information from the IPinfo API and displayed it using a Rich dashboard.

### 2. Packaging Theory

**What is the difference between an `sdist` (.tar.gz) and a Wheel (.whl)?**


An `sdist` (source distribution) is an archive containing the package's source code and the files needed to build it. When installing an sdist, the package generally needs to be built on the user's machine.

A Wheel is a pre-built distribution containing the package in an installable format. It allows package managers to install the files directly without building the package from source.

** Why are Wheels significantly faster and safer to install on client machines?**


Wheels are generally faster because they are already built, so the installation process does not need to compile or build the package from source.

They are also generally safer because installation does not require running the package's build process on the client's machine. This reduces the need to execute build scripts or build-backend code during installation. However, a Wheel is not automatically safe; its contents and publisher must still be trusted.



## Part 5: Professional Debugging Challenge (No `print()`!)

### 1. Root Cause Analysis

Using the VS Code Debug Console, I inspected the runtime types:

- `record["volume"]`: `<class 'str'>`
- `record["weight"]`: `<class 'str'>`

The `split(",")` method returns strings. Therefore, multiplying `volume` by `weight` caused a `TypeError` because Python cannot multiply two strings.

### 2. Conditional Breakpoint

I set a conditional breakpoint on the following line:


impact = compute_weighted_metric(record["volume"], record["weight"])

Condition: `idx == 2`

This makes the debugger stop when processing the third record.

### 3. Step Into and Call Stack

I used Step Into (F11) to enter `compute_weighted_metric()`.

The Call Stack showed:

1. `compute_weighted_metric`
2. `aggregate_telemetry`
3. `<module>`

### 4. The Fix

I converted `volume` and `weight` to floating-point numbers inside `parse_api_record()`:


"volume": float(parts[2]),
"weight": float(parts[4])


### 5. Verified Execution Output

Command:

uv run python scripts/debug_challenge.py

Output:

Aggregate Result: {'successful_entries': 3, 'total_volume': 650.0, 'avg_volume': 216.66666666666666, 'high_impact_count': 1}
