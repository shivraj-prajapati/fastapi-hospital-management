from typing import Annotated
import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status
from crud import create_item
from database.database import get_db
from models.models import Inventory
from schemas.schema import InventoryCreate

router = APIRouter()

@router.post("/inventory/",status_code=status.HTTP_201_CREATED)
async def create_inventory(inventory: InventoryCreate, db: Annotated[Session, Depends(get_db)]):
    new_inventory = Inventory(**inventory.model_dump())
    db.add(new_inventory)
    db.commit()
    db.refresh(new_inventory)
    if not new_inventory:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create inventory.")
    return new_inventory
    

@router.get("/inventory", status_code=status.HTTP_200_OK)
async def get_all_inventory(db: Annotated[Session, Depends(get_db)]):
    inventory = db.query(Inventory).all()
    if not inventory:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No inventory found.")
    return inventory

@router.get("/inventory/{item_id}", status_code=status.HTTP_200_OK)
async def get_inventory(item_id: uuid.UUID, db: Annotated[Session, Depends(get_db)]):
    inventory = db.query(Inventory).filter(Inventory.item_id == item_id).first()
    if not inventory:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Inventory item not found.")
    return inventory

@router.put("/inventory/{item_id}", status_code=status.HTTP_202_ACCEPTED)
async def update_inventory(item_id: uuid.UUID, inventory: InventoryCreate, db: Annotated[Session, Depends(get_db)]):
    update_inventory = db.query(Inventory).filter(Inventory.item_id == item_id).first()
    if not update_inventory:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Inventory item not found.')
    for key, value in inventory.model_dump().items():
        setattr(update_inventory, key, value)
    db.commit()
    db.refresh(update_inventory)
    return update_inventory

@router.delete("/inventory/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_inventory(item_id: uuid.UUID, db: Annotated[Session, Depends(get_db)]):
    inventory = db.query(Inventory).filter(Inventory.item_id == item_id).first()
    if not inventory:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Inventory item not found.")
    db.delete(inventory)
    db.commit()
    return {"detail": "Inventory item deleted successfully"}