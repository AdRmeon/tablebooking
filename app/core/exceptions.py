from fastapi import HTTPException


TABLE_ALREADY_BOOKED_400 = HTTPException(
    status_code=400,
    detail="This time slot is already booked for the selected table.",
)
