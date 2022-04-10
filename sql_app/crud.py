from sqlalchemy.orm import Session

from . import models, schemas


def create_url(db: Session, url: schemas.ShortUrlCreate, short: str):
    db_url = models.ShortUrl(url=url.url, short=short)
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    return db_url


def get_url_by_short_url(db: Session, short_url: str):
    return db.query(models.ShortUrl).filter(models.ShortUrl.short == short_url).first()
