import sys
import os

# Ensure project root is on sys.path so "invoice_qc" can be imported
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# Now import the FastAPI app from the package
from invoice_qc.api import app as invoice_app

app = invoice_app

