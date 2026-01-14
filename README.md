# suspension_unsuspension_canvas

Utilities to suspend and unsuspend accounts or enrollments in Canvas LMS.  
This repository contains scripts and helpers to interact with the Canvas API for performing bulk or individual suspend/unsuspend operations. The README below is a template — update the placeholders (script names, examples, and configuration) to match the actual files and usage in this repository.

## Features
- Suspend or unsuspend Canvas users or course enrollments via the Canvas REST API.
- Support for single operations and bulk operations (CSV or batch).
- Configurable API endpoint and token through environment variables.
- Idempotent operations with basic logging and error reporting.

## Prerequisites
- Python 3.8+ (or the version used by project)
- requests, and tkinter
- pip
- A Canvas API token with permission to manage users/enrollments
- Network access to your Canvas instance

## Installation
1. Clone the repository:
   git clone https://github.com/aphiwut-j/suspension_unsuspension_canvas.git
   cd suspension_unsuspension_canvas

2. (Recommended) Create and activate a virtual environment:
   python -m venv .venv
   source .venv/bin/activate  # macOS/Linux
   .venv\Scripts\activate     # Windows

3. Install dependencies:
   pip install request tkinter
   
## Usage
Update the following usage examples to match the actual script names in this repo.

Suspend a single user by user id:
python app.py

Unsuspend a single user:
python app.py

Bulk suspend from CSV (CSV columns: Student No):
python app.py

## Examples
Example cURL (for quick manual test — replace values):
curl -X PUT \
  -H "Authorization: Bearer $CANVAS_API_TOKEN" \
  "$CANVAS_API_URL/accounts/1/users/12345/suspend"

Example Python snippet:
```python
import os, requests

API_URL = os.environ["CANVAS_API_URL"]
TOKEN = os.environ["CANVAS_API_TOKEN"]
headers = {"Authorization": f"Bearer {TOKEN}"}

resp = requests.put(f"{API_URL}/accounts/1/users/12345/suspend", headers=headers)
resp.raise_for_status()
print("Suspended:", resp.json())
```


## Contributing
Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch: git checkout -b feature/describe-change
3. Commit changes with a descriptive message
4. Open a pull request describing the change and motivation

Add an issue for larger changes or design discussions before implementing.

## License
Add a license file (e.g., `LICENSE`) to this repository and update this section with the license name and short summary.

## Contact
For questions or support, open an issue on this repository or contact the maintainer: [aphiwut-j](https://github.com/aphiwut-j).

Notes:
- Replace script names and examples above with the actual filenames and usage implemented in this repository.
- Your CSV/Excel file for lthe ist of students must only have one column called "Student No" and the "Student No" must only contain digits in the integer format (will be automatically formatted in the app)
