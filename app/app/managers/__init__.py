# ruff: noqa: ERA001
from fastapi_sqlalchemy_toolkit import ModelManager  # noqa: F401

# Create new managers like this:
# item_manager = ModelManager[Item, CreateItemSchema, UpdateItemSchema](Item)
