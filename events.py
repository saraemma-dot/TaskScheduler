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


@router.post("/events")
def add_event(id:str,tenant_id:str,event_type:str,
             payload:str,idempotency_key:str,created_at:str
             ,conn:sqlite3.Connection=Depends(get_db)):

            now=datetime.now(timezone.utc).isoformat()
            try: 
                conn.execute("""INSERT INTO events(id, tenant_id, 
                                 event_type,payload,idempotency_key,created_at)
                                 VALUES (?,?,?,?,?,?)""",
                   (id,tenant_id,event_type,payload,idempotency_key,now))
                conn.commit()
            except sqlite3.IntegrityError as e : 
                raise HTTPException(status_code=409,detail=str(e))

            return {"id": id, "tenant_id":tenant_id,"event_type":event_type,
            "idempotency_key":idempotency_key,"created_at":now}

@router.get("/events/{id}")
def get_event(id:str,conn:sqlite3.Connection=Depends(get_db)):
    row=conn.execute("""SELECT id, tenant_id, 
                    event_type,payload,idempotency_key,created_at 
                    FROM events WHERE id= ?""",(id,),).fetchone()
    if row is None : 
        raise HTTPException(status_code=404,detail="Event not found")
    
    return dict(row)

    
