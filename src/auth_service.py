import smtplib as smtp
import random
import string
from fastapi import FastAPI, BackgroundTasks, HTTPException
from pydantic import BaseModel
import uvicorn
from uuid import uuid4, UUID
import json
from sqlalchemy import Column, Integer, String, literal_column, select, create_engine, delete
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv
import os

app = FastAPI()
tasks = []
Base = declarative_base()

class Task_bool(BaseModel):
    id: UUID
    status: str
    result: bool

class Task_str(BaseModel):
    id: UUID
    status: str
    result: str

class UserRole(Base):
    __tablename__ = 'user_roles'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer)
    nickname = Column(String)
    role = Column(String)

class NicknameCode(Base):
    __tablename__ = 'nickname_codes'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nickname = Column(String)
    code = Column(String)

@app.post("/check_id", response_model=Task_str)
async def create_task(user_id: dict, background_tasks: BackgroundTasks):
    task = Task_str(id=uuid4(), status="running", result="None")
    tasks.append(task)
    background_tasks.add_task(check_user, task, user_id['user_id'])
    return task


@app.get("/{task_id}")
async def get_task(task_id: UUID):
    for task in tasks:
        if task.id == task_id:
            return task

async def check_user(task, user_id):
    user = session.query(UserRole).filter(UserRole.user_id == user_id).first()
    task.status = "ready"
    if user:
        task.result = True

@app.post("/check_mail", response_model=Task_str)
async def create_task(nickname: dict, background_tasks: BackgroundTasks):
    code = generate_code(6)
    new_nicname_code = NicknameCode(nickname=nickname['nickname'], code=code)
    session.add(new_nicname_code)
    session.commit()

    task = Task_str(id=uuid4(), status="running", result=code)
    tasks.append(task)
    background_tasks.add_task(send_mail, task, nickname['nickname'])
    return task

def send_mail(task: Task_str, nickname: str) -> str:
    email = "workspacemanagertelebot@yandex.ru"
    # load_dotenv('.env')
    # password = os.getenv("MAIL_PASSWORD")
    password = "wwjitkohdkflgpzx" # need hide
    dest_email = nickname + "@student.21-school.ru"
    subject = "Authorization"
    secret_code = task.result
    email_text = "Your authorization code: " + secret_code

    message = 'From: {}\nTo: {}\nSubject: {}\n\n{}'.format(email,
                                                        dest_email, 
                                                        subject, 
                                                        email_text)

    server = smtp.SMTP_SSL('smtp.yandex.com', 465)
    server.login(email, password)
    server.sendmail(email, dest_email, message)
    server.quit()

    task.status = "ready"

def generate_code(length):
    all_symbols = string.ascii_uppercase + string.digits
    result = ''.join(random.choice(all_symbols) for _ in range(length))
    return result

@app.post("/check_code", response_model=Task_bool)
async def create_task(code: dict, background_tasks: BackgroundTasks):
    task = Task_bool(id=uuid4(), status="running", result=False)
    tasks.append(task)
    background_tasks.add_task(check_code, task, code)
    return task

async def check_code(task: Task_bool, code:dict):
    user = session.query(NicknameCode).filter(
        NicknameCode.code == code['code'] and 
        NicknameCode.nickname == code['nickname']).first()

    new_user = UserRole(
        user_id=code['user_id'], nickname=code['nickname'], role='COMMON') #autoincrement doesn't work, i dont know why
    session.add(new_user)
    session.commit()

    task.status = "ready"
    if user:
        task.result = True

    # delete_statement = delete(NicknameCode).where(NicknameCode.id == user.id)
    # session.execute(delete_statement)
    # session.commit()

class UserRequest(BaseModel):
    user: dict

@app.get("/user/id={user_id}")
def get_user_role(user_id: str):
    user_role = session.query(UserRole).filter(UserRole.user_id == int(user_id)).first()
    if user_role:
        role = user_role.role
    else:
        raise HTTPException(status_code=404, detail="Item not found")
    result = json.dumps({"user_id": int(user_id), "role": role})
    return result
    

if __name__ == "__main__":
    engine = create_engine('sqlite:///user_auth.db')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    # for testing
    #===================================================================
    user_role1 = UserRole(user_id=666, nickname='chelovek_admin', role='ADM')
    user_role2 = UserRole(user_id=333, nickname='user-man', role='COMMON')
    user_role3 = UserRole(user_id=999, nickname='user-woman', role='COMMON')
    session.add_all([user_role1, user_role2, user_role3])
    #===================================================================

    session.commit()

    uvicorn.run(app, port=8888)

# wwjitkohdkflgpzx