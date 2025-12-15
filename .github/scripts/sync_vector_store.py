import os
import json
import hashlib
from pathlib import Path
from openai import OpenAI

DOCS_DIR = Path("docs")
MAP_FILE = Path(".github/openai-file-map.json")

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
VECTOR_STORE_ID = os.environ.get("OPENAI_DOCS_VS_ID")

if not OPENAI_API_KEY or not VECTOR_STORE_ID:
    raise RuntimeError("Missing OPENAI_API_KEY or OPENAI_DOCS_VS_ID")

client = OpenAI(api_key=OPENAI_API_KEY)

def compute_hash(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

def load_map() -> dict:
    if MAP_FILE.exists():
        with open(MAP_FILE, "r") as f:
            return json.load(f)
    return {}

def save_map(m: dict):
    MAP_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(MAP_FILE, "w") as f:
        json.dump(m, f, indent=2)

def upload_and_attach(path: Path) -> str:
    print(f"Uploading: {path}")

    uploaded = client.files.create(
        file=open(path, "rb"),
        purpose="assistants"
    )

    client.vector_stores.files.create(
        vector_store_id=VECTOR_STORE_ID,
        file_id=uploaded.id
    )

    return uploaded.id

def delete_from_vector_store(file_id: str, path: str):
    try:
        client.vector_stores.files.delete(
            vector_store_id=VECTOR_STORE_ID,
            file_id=file_id
        )
        print(f"Deleted from vector store: {path}")
    except Exception as e:
        print(f"Warning: failed to delete {path}: {e}")

file_map = load_map()

current_files = {}
for f in DOCS_DIR.rglob("*"):
    if f.is_file():
        rel_path = f.as_posix()
        current_files[rel_path] = compute_hash(f)

indexed = 0
deleted = 0

# Handle new + updated files
for path, current_hash in current_files.items():
    if path not in file_map:
        file_id = upload_and_attach(Path(path))
        file_map[path] = {
            "file_id": file_id,
            "hash": current_hash
        }
        indexed += 1

    else:
        # Existing file, check content
        if file_map[path]["hash"] != current_hash:
            delete_from_vector_store(file_map[path]["file_id"], path)
            file_id = upload_and_attach(Path(path))
            file_map[path] = {
                "file_id": file_id,
                "hash": current_hash
            }
            indexed += 1

# Handle deleted files
for path in list(file_map.keys()):
    if path not in current_files:
        delete_from_vector_store(file_map[path]["file_id"], path)
        del file_map[path]
        deleted += 1

save_map(file_map)

print("Sync complete.")
print(f"Uploaded/updated: {indexed}")
print(f"Deleted: {deleted}")