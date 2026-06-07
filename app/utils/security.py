from passlib.context import CryptContext
#创建加密上下文，指定加密方式为bcrypt
pwd_content = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 对密码进行加密
def hash_password(password:str)-> str:
    raw = password.encode("utf-8")[:72]
    return pwd_content.hash(raw)

# 验证密码
def verify_password(plain:str,hashed:str)-> bool:
    return pwd_content.verify(plain,hashed)
