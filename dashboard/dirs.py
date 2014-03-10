import os

THIS_DIR = os.path.dirname(os.path.abspath(__file__))

# Directory holding secret information.
SECRETS_DIR = os.path.join(os.path.dirname(THIS_DIR), "secrets")

LOOKUPS_DIR = os.path.join(THIS_DIR, "lookups")

CONFIG_DIR = os.path.join(THIS_DIR, "config")

CACHE_DIR = os.path.join(os.path.dirname(THIS_DIR), "cache")
