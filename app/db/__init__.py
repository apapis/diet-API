from app.db.session import engine, Base
from app.db.models import Meal

def init_db():
    print("🔹 Tworzenie tabel w bazie danych...")
    Base.metadata.create_all(bind=engine)
    print("✅ Baza danych gotowa!")
