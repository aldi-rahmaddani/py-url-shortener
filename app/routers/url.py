from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse, HTMLResponse
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import Optional
import random, string

from app.config.db import get_db
from app.models.url import URL
from app.models.user import User
from app.schemas.url import URLRequest, URLResponse

from app.utils.authentication import get_current_user, hash_password, verify_password

router = APIRouter()


def generate_short_url():
    return "".join(random.choices(string.ascii_letters + string.digits, k=6))


@router.get("/list", response_model=list[URLResponse])
def get_list_url(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    """Mengambil semua URL milik user yang sedang login"""
    urls = db.query(URL).filter(URL.user_id == current_user.id).all()
    print(urls)

    if not urls:
        raise HTTPException(status_code=404, detail="No URLs found for this user")

    return urls


@router.get("/{short_url}")
def redirect_to_original(
    short_url: str, password: Optional[str] = None, db: Session = Depends(get_db)
):
    url_entry = db.query(URL).filter(URL.short_url == short_url).first()

    if not url_entry:
        raise HTTPException(status_code=404, detail="Short URL not found")

    if url_entry.expires_at and datetime.utcnow() > url_entry.expires_at:
        raise HTTPException(status_code=410, detail="Short URL has expired")

    # Jika URL memiliki password tetapi user belum memasukkan password, tampilkan prompt
    if url_entry.password_hash and not password:
        return HTMLResponse(
            f"""
            <script>
                var password = prompt("This URL is protected. Please enter the password:");
                if (password) {{
                    window.location.href = "/short/{short_url}?password=" + encodeURIComponent(password);
                }} else {{
                    alert("Password is required!");
                    window.history.back();
                }}
            </script>
        """
        )

        # Jika password dikirim melalui query, verifikasi
    if url_entry.password_hash and not verify_password(
        password, url_entry.password_hash
    ):
        raise HTTPException(status_code=403, detail="Invalid password")

    url_entry.click_count += 1
    db.commit()

    return RedirectResponse(url_entry.original_url)


@router.post("/", response_model=URLResponse)
def shorten_url(
    request: URLRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    short_url = ""

    # Check if the total user URLs have reached the limit
    limit_urls = current_user.url_limit
    total_urls = db.query(URL).filter(URL.user_id == current_user.id).count()

    if total_urls >= limit_urls:
        raise HTTPException(
            status_code=400,
            detail="User URL limit reached, please delete some to be able to add more",
        )

    # Ensure uniqueness
    if request.custom_slug:
        existing_url = (
            db.query(URL).filter(URL.short_url == request.custom_slug).first()
        )

        if existing_url:
            raise HTTPException(status_code=400, detail="Custom slug already in use")

        short_url = request.custom_slug
    else:
        short_url = generate_short_url()

        while db.query(URL).filter(URL.short_url == short_url).first():
            short_url = generate_short_url()

    password_hash = hash_password(request.password) if request.password else None

    expires_at = datetime.utcnow() + timedelta(days=request.expire_in_days)
    new_url = URL(
        original_url=request.original_url,
        short_url=short_url,
        expires_at=expires_at,
        user_id=current_user.id,
        password_hash=password_hash,
    )

    db.add(new_url)
    db.commit()
    db.refresh(new_url)

    return new_url


@router.delete("/{id_url}", response_model=dict)
def delete_url(
    id_url: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    url_entry = db.query(URL).filter(URL.id == id_url).first()

    if not url_entry:
        raise HTTPException(status_code=404, detail="URL not found")

    if url_entry.user_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="You are not authorized to delete this URL"
        )

    db.delete(url_entry)
    db.commit()

    return {"status": "OK", "message": "URL deleted successfully"}
