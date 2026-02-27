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
    

@app.get("/users/{user_id}")
def get_user(user_id:str,conn:sqlite3.Connection=Depends(get_db)):
    row=conn.execute("""SELECT id,username,created_at 
    FROM users WHERE id= ?""",(user_id,),).fetchone()
    if row is None : 
        raise HTTPException(status_code=404,ddetail="User not found")
    
    return dict(row)

@app.put("/users/{user_id}/password")
def update_password(user_id: str,new_password_hash,conn:sqlite3.Connection=Depends(get_db)):
    now=datetime.now(timezone.utc).isoformat()
    result=conn.execute("""UPDATE users SET 
                        password_hash=?,updated_at=?
                        WHERE id= ?""",(new_password_hash,now))
    conn.commit()

    if result.rowcount == 0:
        raise HTTPException(status_code=404,detail="User not found")
    return {"status": "password updated"}

@app.post("/users")
def add_user(user_id: str,username:str,email:str,password_hash:str,conn:sqlite3.Connection=Depends(get_db)):
            
            current_time=datetime.now(timezone.utc).isoformat()
            try: 
                conn.execute("""INSERT INTO users (id, username, email,
                                 password_hash,
                                 created_at, updated_at)
                                 VALUES (?,?,?,?,?.?)""",
                   (user_id,email,password_hash,
                   current_time,current_time))
                conn.commit()
            except sqlite3.IntegrityError as e : 
                raise HTTPException(status_code=409,detail=str(e))

            return {"id": user_id, "username": username, "email": email, "created_at": current_time}

@app.delete("/users/{user_id}")
def del_user(user_id: str,conn:sqlite3.Connection=Depends(get_db)) :
    result=conn.execute ("""DELETE FROM users WHERE id=?""",(user_id,),)
    conn.commit()

    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {"status":"user deleted"}




    

