import cloudinary
import cloudinary.uploader
from dotenv import load_dotenv
import os

load_dotenv()

cloudinary.config(
    cloudinary_url=os.getenv("CLOUDINARY_URL"),
    secure=True
)

result = cloudinary.uploader.upload(
    "static/default_img_rf.png",
    folder="doughfinder/test"
)

print("UPLOAD OK:", result["secure_url"])
