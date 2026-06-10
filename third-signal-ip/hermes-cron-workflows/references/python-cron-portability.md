# Python Script Portability for Cron Workflows

When writing standalone Python scripts to be executed by Hermes background cron jobs (especially with `no_agent=true`), you must design for extreme portability.

## The Dependency Trap
Hermes executes scripts using its internal `venv` or the system Python. You cannot guarantee that external PyPI packages (like `requests`, `pandas`, or `beautifulsoup4`) are installed in the execution environment. Attempting to run scripts with external dependencies will frequently result in `ModuleNotFoundError` crashes.

## Best Practices
1. **Zero External Dependencies:** Build your entire script using only the Python Standard Library.
2. **Network Requests:** Use `urllib.request` and `json` instead of the `requests` library.
    ```python
    import urllib.request
    import json
    
    req = urllib.request.Request("http://api.endpoint", headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read().decode())
    ```
3. **File System:** Use `os`, `glob`, and `shutil`. 

By adhering to the standard library, your cron jobs will execute flawlessly regardless of the host environment's `pip` state.