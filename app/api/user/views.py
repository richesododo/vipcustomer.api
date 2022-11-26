from fastapi import APIRouter, Depends, HTTPException, status, Request
import jwt
from db.db import db_session
from api.user.schemas import Signup, Login, APIKey
from sqlalchemy.ext.asyncio import AsyncSession
from db.models.user import User
from api.user.authentication import config_credentials, authorized_exception
from fastapi.security import OAuth2PasswordBearer
from api.user.services import UserService

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


@router.post('/signup')
async def create_user(user:Signup,session: AsyncSession = Depends(db_session)):
    user_service = UserService(session=session)
    new_user = await user_service.create_user(user)
    new_user = User(**user.dict())
    return new_user

@router.post('/login')
async def login(form_data: Login, session: AsyncSession = Depends(db_session)):
    user_service = UserService(session=session)
    res = await user_service.token_generator(form_data.email, form_data.password)
    user, token = res['user'], res['access_token']
    try:
        payload = jwt.decode(token, config_credentials['SECRET_KEY'], config_credentials['ALGORITHM'])
        return  {
            'user': {
                'id' : user.id,
                'email' : user.email,
                'first_name' : user.first_name,
                'last_name' : user.last_name
            },
            'access_token' : token,'token_type' : 'bearer'
        }
    except:
        raise authorized_exception

@router.post("/get_api_key")
async def get_user_api_key(form_data : Login, session: AsyncSession = Depends(db_session)):
    user_service = UserService(session=session)
    key = await user_service.get_api_key(form_data.email, form_data.password)
    return key

@router.post('/verify/')
async def verify_api_key(key: APIKey, session: AsyncSession = Depends(db_session)):
    user_service = UserService(session=session)
    key = await user_service.verify_api_key(key)
    return key

# async def get_current_user(token : str = Depends(oauth2_scheme)):
#     try:
#         payload = jwt.decode(token, config_credentials['SECRET_KEY'], config_credentials['ALGORITHM'])
#         user = await User.get(id=payload.get('id'))
#     except:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail = 'Invalid Username or Password',
#             headers={"WWW-Authenticate":'Bearer'}
#         )
#     return await user




# @router.get("/my_details/")
# def get_current_user(current_user: User):
#     return current_user


