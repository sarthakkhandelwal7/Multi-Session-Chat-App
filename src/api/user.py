from fastapi import APIRouter, Depends, HTTPException
from src.dependency import get_user_service
from src.service import UserService
from src.schema import (
    CreateUserRequest,
    UpdateUserRequest,
    UserResponse,
    CreateUserResponse,
)
from typing import List
from uuid import UUID

user_router = APIRouter(prefix="/user", tags=["user"])


@user_router.post(path="", response_model=CreateUserResponse)
async def create_user(
    request: CreateUserRequest,
    user_service: UserService = Depends(get_user_service),
) -> CreateUserResponse:
    """Create a new user"""
    response = await user_service.create_user(
        first_name=request.first_name,
        last_name=request.last_name,
        email=request.email,
    )
    return CreateUserResponse(user_id=str(response["user_id"]))


@user_router.get(path="/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: UUID, user_service: UserService = Depends(get_user_service)
) -> UserResponse:
    """Get a specific user by ID"""
    user = await user_service.get_user_by_id(str(user_id))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserResponse(**user)


@user_router.get(path="", response_model=List[UserResponse])
async def get_all_users(
    user_service: UserService = Depends(get_user_service),
) -> List[UserResponse]:
    """Get all users"""
    users = await user_service.get_all_users()
    return [UserResponse(**user) for user in users]


@user_router.put(path="/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: UUID,
    request: UpdateUserRequest,
    user_service: UserService = Depends(get_user_service),
) -> UserResponse:
    """Update user information"""
    # Check if user exists
    existing_user = await user_service.get_user_by_id(str(user_id))
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")

    updated_user = await user_service.update_user(
        user_id=str(user_id),
        first_name=request.first_name,
        last_name=request.last_name,
        email=request.email,
    )
    return UserResponse(**updated_user)


@user_router.delete(path="/{user_id}")
async def delete_user(
    user_id: UUID, user_service: UserService = Depends(get_user_service)
):
    """Delete a user"""
    # Check if user exists
    user = await user_service.get_user_by_id(str(user_id))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    await user_service.delete_user(str(user_id))
    return {"message": "User deleted successfully"}
