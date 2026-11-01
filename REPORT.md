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

Changes not staged for commit:

	modified:   .gitignore
	modified:   REPORT.md
	modified:   pyproject.toml
	modified:   uv.lock

Untracked files:

	.env.template
	scripts/test_api.py
	src/engtoolslab2/client.py
	src/engtoolslab2/config.py

no changes added to commit


To be completed with the output of `git status`.

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
