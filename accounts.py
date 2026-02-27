from fastapi import FastAPI,Depends,HTTException
from pydantic import BaseModel,Field
import database
import sqlite3 
from typing import Generator
from datetime import datetime,timezone


def get_db()->Generator [sqlite3.Connection,None,None]:
    conn=sqlite3.connect('eventscheduler.db')
    conn.row_factory = sqlite3.Row
    try:       
        print('connection to db has been established')
        yield conn #gives the resource to the endpoint

    finally :
        conn.close()


@app.post("/accounts")
def add_account(id: str,user_id:str,created_at:str,
                conn:sqlite3.Connection=Depends(get_db)):

            now=datetime.now(timezone.utc).isoformat()
            try: 
                conn.execute("""INSERT INTO accounts (id, user_id, 
                                 created_at, updated_at)
                                 VALUES (?,?,?,?)""",
                   (id,user_id,created_at,now,now))
                conn.commit()
            except sqlite3.IntegrityError as e : 
                raise HTTPException(status_code=409,detail=str(e))

            return {"id": id, "user_id":user_id,"created_at":now}




@app.put("/accounts/{id}/touch")
def touch_account(id: str,created_at:str,conn:sqlite3.Connection=Depends(get_db)):
    now=datetime.now(timezone.utc).isoformat()
    result=conn.execute("""UPDATE accounts SET 
                        updated_at=?
                        WHERE id= ?""",(id,now))
    conn.commit()

    if result.rowcount == 0:
        raise HTTPException(status_code=404,detail="Account not found")
    return {"status": "account updated","updated_at": now}

