from fastapi import APIRouter, HTTPException

from app.schemas.user import UserCreate, UserUpdate, UserResponse
import app.services.user_service as user_service


router = APIRouter()


@router.post("/users", response_model=UserResponse)
def create_user(user: UserCreate):

    try:
        return user_service.create_user(user)

    except ValueError as error:
        if str(error) == "User already exists":
            raise HTTPException(
                status_code=409,
                detail=str(error)
            )

        raise


@router.get("/users", response_model=list[UserResponse])
def get_users():

    return user_service.get_users()


@router.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: str):

    try:
        user = user_service.get_user(user_id)

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user


@router.put("/users/{user_id}", response_model=UserResponse)
def update_user(user_id: str, user: UserUpdate):

    try:
        updated_user = user_service.update_user(
            user_id,
            user
        )

    except ValueError as error:

        if str(error) == "User already exists":
            raise HTTPException(
                status_code=409,
                detail=str(error)
            )

        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    if updated_user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return updated_user



@router.delete("/users/{user_id}")
def delete_user(user_id: str):

    try:
        deleted = user_service.delete_user(user_id)

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return {
        "message": "User deleted successfully"
    }