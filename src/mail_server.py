import smtplib as smtp
from getpass import getpass
import random
import string
import data_base

from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
import aiohttp

import uvicorn
from uuid import uuid4, UUID

def send_mail(to_address: str) -> str:
    email = "workspacemanagertelebot@yandex.ru"
    password = "wwjitkohdkflgpzx" # need hide
    dest_email = to_address
    subject = "Authorization"
    secret_code = generate_code(6)
    email_text = "Your authorization code: " + secret_code

    message = 'From: {}\nTo: {}\nSubject: {}\n\n{}'.format(email,
                                                        dest_email, 
                                                        subject, 
                                                        email_text)

    server = smtp.SMTP_SSL('smtp.yandex.com', 465)
    server.login(email, password)
    server.sendmail(email, dest_email, message)
    server.quit()
    return secret_code

 
def generate_code(length):
    all_symbols = string.ascii_uppercase + string.digits
    result = ''.join(random.choice(all_symbols) for _ in range(length))
    return result

app = FastAPI()
tasks = []

class check_id_task(BaseModel):
    id: UUID
    status: str
    result: bool

@app.post("/check_id", response_model=check_id_task)
async def create_task(user_id: dict, background_tasks: BackgroundTasks):
    task = check_id_task(id=uuid4(), status="running", result={})
    tasks.append(task)
    background_tasks.add_task(check_user(), task, session, user_id['user'])
    return task


@app.get("/check_id/{task_id}", response_model=check_id_task)
async def get_task(task_id: UUID):
    for task in tasks:
        if task.id == task_id:
            return task

def check_user(task, session, user_id):
    user = session.query(data_base.UserRole).filter(data_base.UserRole.user_id == user_id).first()
    task.status = "ready"
    if user:
        return True
    else:
        return False

if __name__ == "__main__":
    # send_mail("rosmertt@student.21-school.ru")
    data_base.connect_to_db()
    engine = data_base.create_engine('postgresql://postgres:@localhost:5430/user_auth_db')
    data_base.Base.metadata.create_all(engine)
    Session = data_base.sessionmaker(bind=engine)
    session = Session()

    # Insert a new user role
    # new_user_role = UserRole(user_id='321', role='admin')
    # session.add(new_user_role)
    session.commit()
    uvicorn.run(app, port=8888)

# wwjitkohdkflgpzx