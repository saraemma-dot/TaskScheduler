from fastapi import FastAPI,Depends,HTTException
from pydantic import BaseModel,Field
import database
import sqlite3 
from typing import Generator
from datetime import datetime,timezone

app=FastAPI()


def get_db()->Generator [sqlite3.Connection,None,None]:
    conn=sqlite3.connect('eventscheduler.db')
    conn.row_factory = sqlite3.Row
    try:       
        print('connection to db has been established')
        yield conn #gives the resource to the endpoint

    finally :
        conn.close()
    
@app.get("/deliveries")
def get_delivery(id:str,conn:sqlite3.Connection=Depends(get_db)):
    row=conn.execute("""SELECT * ,
                        FROM deliveries WHERE id= ?""",(id,),).fetchone()
    if row is None : 
        raise HTTPException(status_code=404,ddetail="User not found")
    
    return dict(row)

@app.get("/deliveries/{id}/status")
def delivery_status(id:str,conn:sqlite3.Connection=Depends(get_db)):
    row=conn.execute("""SELECT status ,
                        FROM deliveries WHERE id= ?""",(id,),).fetchone()
    if row is None : 
        raise HTTPException(status_code=404,ddetail="Delivery not found")
    
    return dict(row)