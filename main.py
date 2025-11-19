from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import Base, engine, SessionLocal
from models import Student
from face_utils import get_face_embedding, compare_faces
from utils import save_uploaded_image
import numpy as np

app = FastAPI()

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

# ----------- ENROLL STUDENT -----------
@app.post("/enroll")
async def enroll_student(
    name: str = Form(...),
    regno: str = Form(...),
    photo: UploadFile = File(...)
):
    db = next(get_db())
    filename = f"{regno}.jpg"
    content = await photo.read()
    file_path = save_uploaded_image(content, filename)

    embedding = get_face_embedding(file_path)
    if embedding is None:
        return {"message": "No face detected in student photo!"}

    existing = db.query(Student).filter(Student.regno == regno).first()
    if existing:
        existing.name = name
        existing.photo = filename
        existing.embedding = embedding
        db.commit()
        return {"message": "Student updated successfully!"}

    student = Student(
        name=name,
        regno=regno,
        photo=filename,
        embedding=embedding
    )
    db.add(student)
    db.commit()
    return {"message": "Student enrolled successfully!"}

# ----------- ATTENDANCE -----------
@app.post("/attendance")
async def take_attendance(photo: UploadFile = File(...)):
    db = next(get_db())
    students = db.query(Student).all()

    classroom_file = save_uploaded_image(await photo.read(), "class_photo.jpg")
    unknown_image_array = face_recognition.load_image_file(classroom_file)
    unknown_encodings = face_recognition.face_encodings(unknown_image_array, face_recognition.face_locations(unknown_image_array))

    present = []
    absent = []

    if not unknown_encodings:
        absent = [s.name for s in students]
        return {"present": present, "absent": absent, "message": "No faces detected!"}

    for student in students:
        matched = False
        for u_enc in unknown_encodings:
            if compare_faces(student.embedding, u_enc):
                matched = True
                break
        if matched:
            present.append(student.name)
        else:
            absent.append(student.name)

    return {"present": present, "absent": absent, "message": "Attendance Processed"}
