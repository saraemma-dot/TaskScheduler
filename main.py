from fastapi import FastAPI
import users, events, accounts, payments, deliveries

app = FastAPI()

app.include_router(users.router)
app.include_router(events.router)
app.include_router(accounts.router)
app.include_router(payments.router)
app.include_router(deliveries.router)
