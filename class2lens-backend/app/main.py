from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from .database import Base, engine, SessionLocal
from .models import Student
from .face_utils import generate_fake_embedding, compare_embeddings
from .utils import save_uploaded_image
import os
import shutil

app = FastAPI()

# allow frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/enroll")
async def enroll_student(
    name: str = Form(...),
    regno: str = Form(...),
    photo: UploadFile = File(...)
):
    db = next(get_db())

    # Save photo
    filename = f"{regno}.jpg"
    content = await photo.read()
    save_uploaded_image(content, filename)

    # Generate fake embedding
    embedding = generate_fake_embedding()

    student = Student(
        name=name,
        regno=regno,
        photo=filename,
        fake_embedding=embedding
    )

    db.add(student)
    db.commit()
    return {"message": "Student enrolled"}


@app.post("/attendance")
async def take_attendance(photo: UploadFile = File(...)):
    db = next(get_db())
    students = db.query(Student).all()

    # Save classroom photo
    class_photo_name = "class_photo.jpg"
    file_path = os.path.join("uploads", class_photo_name)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(photo.file, buffer)

    # Fake recognition:
    present = []
    absent = []

    for s in students:
        # randomly mark present or absent (fake logic)
        if int(s.regno[-1]) % 2 == 0:
            present.append(s.name)
        else:
            absent.append(s.name)

    return {"present": present, "absent": absent}
