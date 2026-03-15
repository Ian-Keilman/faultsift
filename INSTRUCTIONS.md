# How to Use

### 1. Clone the repo

(use windows powershell)
```powershell
git clone https://github.com/yourusername/faultsift.git
cd faultsift
```

### 2. Create and activate a virtual environment
```powershell
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install dependencies
```powershell
pip install -r requirements.txt
```

### 4. Run the demo
```powerhsell
python -m faultsift.cli demo
```
You should see a report with matched categories, severity counts, total score, and top hits.

### 5. Analyze log file
```powershell
python -m faultsift.cli analyze sample.log
```

Here's an example command you can use:
```powershell
@"
system boot ok
failed password for root
permission denied
kernel panic - not syncing
segfault at 0
"@ | Set-Content sample.log
```

Then, you can analyze it with this:
```powershell
python -m faultsift.cli analyze sample.log
```

#### Here's everything that it should show:

- total number of suspicious matches
- total score across all matches (score is how severe. check rules.py if you want to know more)
- counts by severity
- counts by category
- top matched lines
- Higher-scoring hits are treated as more severe or more important.

#### Running tests

To run the test suite:
```powershell
pytest
```
If you want to see the exact PowerShell checks used during development, including rule checks, scanner checks, scoring checks, reporter checks, and CLI checks, see LOCALTEST.md. 
It should be above README.md.
