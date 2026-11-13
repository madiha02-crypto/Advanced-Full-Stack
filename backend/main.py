from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import function

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=[ "http://localhost:5173","http://127.0.0.1:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# PYDANTIC MODELS - python library used for checking and data validation.
class Package(BaseModel):
    name: str
    destination: str
    weight: int


class UpdatePackage(BaseModel):
    name: str
    destination: str
    weight: int


class DispatchBatch(BaseModel):
    destination: str
    vehicle_number: int
    dispatch_date: str


class Login(BaseModel):
    username: str
    password: str


class RegisterUser(BaseModel):
    user_name: str
    password: str



# E1 - REGISTER PACKAGE
@app.post("/packages")
def register_package(package: Package,token=Header(None)):
    username = function.verify_token(token=token)

    if not username:
        raise HTTPException(status_code=401,detail="Invalid or Expired token")

    return function.register_package(
        name=package.name,
        destination=package.destination,
        weight=package.weight
    )


# E2 - GET PACKAGE
@app.get("/packages/{package_id}")
def get_package_details(package_id: int,token=Header(None)):
    username = function.verify_token(token=token)

    if not username:
        raise HTTPException(status_code=401,detail="Invalid or Expired token")

    return function.get_package_by_id(package_id)


# E3 - UPDATE PACKAGE
@app.patch("/packages/{package_id}")
def update_package_details(package_id: int,package: UpdatePackage,token=Header(None)):
    username = function.verify_token(token=token)

    if not username:
        raise HTTPException(status_code=401,detail="Invalid or Expired token")

    return function.update_package_details(
        package_id=package_id,
        name=package.name,
        destination=package.destination,
        weight=package.weight
    )


# E4 - DELETE PACKAGE
@app.delete("/packages/{package_id}")
def delete_package(package_id: int,token=Header(None)):
    username = function.verify_token(token=token)

    if not username:
        raise HTTPException(status_code=401,detail="Invalid or Expired token")

    return function.delete_package(package_id=package_id)


# E5 - SEARCH PACKAGE
@app.get("/packages")
def search_package(destination: str = None,status: str = None,arrival_date: str = None,token=Header(None)):
    username = function.verify_token(token=token)

    if not username:
        raise HTTPException(status_code=401,detail="Invalid or Expired token")

    return function.search_package(
        destination=destination,
        status=status,
        arrival_date=arrival_date
    )

# E6 - VIEW DISPATCH BATCHES
@app.get("/dispatch-batches")
def view_dispatchBatches(destination: str = None,vehicle_number: int = None,dispatch_status: str = None,token=Header(None)):
    username = function.verify_token(token=token)

    if not username:
        raise HTTPException(status_code=401,detail="Invalid or Expired token")

    return function.view_dispatchBatches(
        destination=destination,
        vehicle_number=vehicle_number,
        dispatch_status=dispatch_status
    )

# E7 - WAREHOUSE SUMMARY
@app.get("/warehouse/summary")
def warehouse_summary(token=Header(None)):
    username = function.verify_token(token=token)

    if not username:
        raise HTTPException(status_code=401,detail="Invalid or Expired token")

    return function.get_warehouse_summary()


# E8 - CREATE DISPATCH BATCH
@app.post("/dispatch-batches")
def add_dispatch(dispatch: DispatchBatch,token=Header(None)):
    username = function.verify_token(token=token)

    if not username:
        raise HTTPException(status_code=401,detail="Invalid or Expired token")

    return function.create_dispatchBatches(
        destination=dispatch.destination,
        vehicle_number=dispatch.vehicle_number,
        dispatch_date=dispatch.dispatch_date
    )


# LOGIN
@app.post("/login")
def login(data: Login):

    token = function.verify_login(username=data.username,password=data.password)

    if not token:
        raise HTTPException(status_code=401,detail="Invalid credentials")

    return token


# REFRESH TOKEN
@app.post("/refresh")
def refresh(refresh_token=Header(None)):

    username = function.verify_token(token=refresh_token,token_type="refresh")

    if not username:
        raise HTTPException(status_code=401,detail="Invalid or Expired refresh token")

    access_token = function.create_token(
        username=username,
        token_type="access"
    )

    return {"access_token": access_token}


# REGISTER USER
@app.post("/register")
def register_user(data: RegisterUser):

    if function.register_user(user_name=data.user_name,password=data.password):
        return {"message": "user registered successfully"}

    raise HTTPException(status_code=400,detail="User already exists")