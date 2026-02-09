import sys

sys.path.insert(0, ".")
from sqlmodel import SQLModel

"""
Utility to inspect registered SQLModel metadata tables.
"""

print("Tables in metadata:", list(SQLModel.metadata.tables.keys()))
