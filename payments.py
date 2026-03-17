from fastapi import APIRouter,Depends,HTTPException
from pydantic import BaseModel,Field
import database
import sqlite3 
from typing import Generator
from datetime import datetime,timezone

router=APIRouter()


def get_db()->Generator [sqlite3.Connection,None,None]:
    conn=sqlite3.connect('eventscheduler.db')
    conn.row_factory = sqlite3.Row
    try:       
        print('connection to db has been established')
        yield conn #gives the resource to the endpoint

    finally :
        conn.close()

@router.get("/payments/{id}")
def get_payment(id:str,conn:sqlite3.Connection=Depends(get_db)):
        row=conn.execute("""SELECT id, account_id,amount,made_at 
                            FROM payments WHERE id= ?""",(id,),).fetchone()
        if row is None : 
            raise HTTPException(status_code=404,detail="Payment not found")
    
        return dict(row)

@router.post("/payments")
def add_payment(id:str,account_id:str,amount:str,
                 conn:sqlite3.Connection=Depends(get_db)):
            now=datetime.now(timezone.utc).isoformat()
            try: 
                conn.execute("""INSERT INTO payments(id,account_id, 
                                 amount,made_at)
                                 VALUES (?,?,?,?)""",
                   (id,account_id,amount,now))
                conn.commit()
            except sqlite3.IntegrityError as e : 
                raise HTTPException(status_code=409,detail=str(e))

            return {"id": id, "account_id":account_id,"amount":amount,"made_at":now}