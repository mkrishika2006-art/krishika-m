 from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import Base, engine, SessionLocal
from models import Student
from face_utils import generate_fake_embedding, compare_embeddings
from utils import save_uploaded_image
import os
import shutil

app = FastAPI()

# Allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# create DB tables
Base.metadata.create_all(bind=engine)

# Database session generator
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -------------------------------
# 🔹 ENROLL STUDENT
# -------------------------------
@app.post("/enroll")
async def enroll_student(
    name: str = Form(...),
    regno: str = Form(...),
    photo: UploadFile = File(...)
):
    db = next(get_db())

    # Save uploaded image
    filename = f"{regno}.jpg"
    content = await photo.read()
    save_uploaded_image(content, filename)

    # Fake embedding
    embedding = generate_fake_embedding()

    # Insert student
    student = Student(
        name=name,
        regno=regno,
        photo=filename,
        fake_embedding=embedding
    )

    db.add(student)
    db.commit()

    return {"message": "Student enrolled successfully!"}


# -------------------------------
# 🔹 ATTENDANCE
# -------------------------------
@app.post("/attendance")
async def take_attendance(photo: UploadFile = File(...)):
    db = next(get_db())
    students = db.query(Student).all()

    # Save classroom image
    class_photo_name = "class_photo.jpg"
    save_path = os.path.join("uploads", class_photo_name)

    with open(save_path, "wb") as buffer:
        shutil.copyfileobj(photo.file, buffer)

    # FAKE attendance logic
    present = []
    absent = []

    for student in students:
        # fake random match
        matched = compare_embeddings(student.fake_embedding, "dummy")

        if matched:
            present.append(student.name)
        else:
            absent.append(student.name)

    return {
        "message": "Attendance Processed",
        "present": present,
        "absent": absent
    }
