from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr, Field
from typing import Optional

app = FastAPI()

class ContactForm(BaseModel):
    name: str = Field(..., min_length = 2)
    email: EmailStr
    subject: str = Field(..., min_length = 3, max_length = 100)
    message: str = Field(..., min_length = 10)


class ContactResponse(BaseModel):
    status: str
    message: str


@app.post("/contact", response_model=ContactResponse)
def submit_contact_form(form: ContactForm):
    # Imagine we store or send this data
    print(f"📩 New message from {form.name} ({form.email}): {form.subject}")
    print(f"Message: {form.message}")

    return ContactResponse(
        status="success",
        message="Thanks for reaching out! We'll get back to you soon."
    )