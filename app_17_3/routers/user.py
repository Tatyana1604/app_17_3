from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from backend.db_inst import get_db
from typing import Annotated
from models.user import User
from schemas import CreateUser, UpdateUser
from sqlalchemy import insert, select, update, delete
from slugify import slugify


router = APIRouter(prefix='/user', tags=['user'])


@router.get('/')
async def all_users(db: Annotated[Session, Depends(get_db)]):
    res = db.execute(select(User))
    users = res.scalars().all()
    return users


@router.get('/user_id')
async def user_by_id(db: Annotated[Session, Depends(get_db)],
                     user_id: int):
    query = select(User).where(User.id == user_id)
    user = db.scalar(query)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not found"
        )
    else:
        return user


@router.post('/create')
async def create_user(db: Annotated[Session, Depends(get_db)],
                      user: CreateUser):
    query = insert(User).values(username=user.username,
                                firstname=user.firstname,
                                lastname=user.lastname,
                                age=user.age,
                                slug=slugify(user.username))
    db.execute(query)
    db.commit()
    return {
        'status_code': status.HTTP_201_CREATED,
        'transaction': 'Successful'
    }


@router.put('/update')
async def update_user(db: Annotated[Session, Depends(get_db)],
                      up_user: UpdateUser, user_id: int):
    query = select(User).where(User.id == user_id)
    user = db.scalar(query)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not found"
        )

    stmt = update(User).where(User.id == user_id).values(
        firstname=up_user.firstname,
        lastname=up_user.lastname,
        age=up_user.age,
    )
    db.execute(stmt)
    db.commit()
    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'User update is successful!'
    }


@router.delete('/delete')
async def delete_user(db: Annotated[Session, Depends(get_db)], user_id: int):
    query = select(User).where(User.id == user_id)
    user = db.scalar(query)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not found"
        )
    stmt = delete(User).where(User.id == user_id)
    db.execute(stmt)
    db.commit()
    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'User deleted!'
    }