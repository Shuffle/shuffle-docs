import os
import json
from openai import OpenAI

VECTOR_STORE_ID = os.environ["VECTOR_STORE_ID"]
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

MAP_FILE = ".github/openai-file-map.json"

# Load or init mapping
if os.path.exists(MAP_FILE):
    with open(MAP_FILE) as f:
        mapping = json.load(f)
else:
    mapping = {}

def parse_json_env(name):
    raw = os.environ.get(name, "[]")
    try:
        return json.loads(raw)
    except Exception:
        return []

added_files = parse_json_env("FILES_ADDED")
modified_files = parse_json_env("FILES_MODIFIED")
deleted_files = parse_json_env("FILES_DELETED")

def upload_and_attach(path):
    with open(path, "rb") as f:
        uploaded = client.files.create(
            file=f,
            purpose="vectorstore"
        )

    client.vector_stores.files.create(
        vector_store_id=VECTOR_STORE_ID,
        file_id=uploaded.id
    )

    mapping[path] = uploaded.id
    print(f"Synced {path} -> {uploaded.id}")

# Added
for path in added_files:
    upload_and_attach(path)

# Modified (delete old first, then upload new)
for path in modified_files:
    if path in mapping:
        client.vector_stores.files.delete(
            vector_store_id=VECTOR_STORE_ID,
            file_id=mapping[path]
        )
    upload_and_attach(path)

# Deleted
for path in deleted_files:
    if path in mapping:
        client.vector_stores.files.delete(
            vector_store_id=VECTOR_STORE_ID,
            file_id=mapping[path]
        )
        del mapping[path]

# Persist mapping
with open(MAP_FILE, "w") as f:
    json.dump(mapping, f, indent=2)
