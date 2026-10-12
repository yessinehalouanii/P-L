from pathlib import Path
from backend.db import DB_PATH, init_db
from backend.seed import seed_if_empty
if DB_PATH.exists():
    DB_PATH.unlink()
init_db(); seed_if_empty()
print('STEPS demo data reset to the original Harbour Crest Resort sample.')
