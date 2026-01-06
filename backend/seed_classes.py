from sqlmodel import Session, select
from app.db import engine
from app.models import CreatureClass

# Define specific colors for the requested classes
# Using the app's purple/dark theme palette where possible
REQUIRED_CLASSES = [
    {"name": "Other", "color": "#9ca3af"},          # Gray
    {"name": "Chimeric", "color": "#fcd34d"},       # Amber
    {"name": "Fae", "color": "#f472b6"},            # Pink
    {"name": "Titanic", "color": "#60a5fa"},        # Blue
    {"name": "Abyssal", "color": "#1e40af"},        # Dark Blue
    {"name": "Ethereal", "color": "#a78bfa"},       # Light Purple
    {"name": "Mythic Beasts", "color": "#f87171"},  # Red
    {"name": "Draconic", "color": "#dc2626"},       # Dark Red
]

def seed_classes():
    results = {"added": [], "skipped": []}
    
    with Session(engine) as session:
        for cls_data in REQUIRED_CLASSES:
            # Check if class exists
            statement = select(CreatureClass).where(CreatureClass.name == cls_data["name"])
            existing = session.exec(statement).first()
            
            if not existing:
                # Create new class
                new_class = CreatureClass(
                    name=cls_data["name"],
                    color=f"rgba(0,0,0,0.1)", # Default bg, replaced below usually but needed for model
                    text_color=cls_data["color"],
                    border_color=cls_data["color"] # Use same for border
                )
                session.add(new_class)
                results["added"].append(cls_data["name"])
            else:
                results["skipped"].append(cls_data["name"])
        
        session.commit()
    
    return results

if __name__ == "__main__":
    r = seed_classes()
    print(f"Seeding complete. Added: {r['added']}, Skipped: {r['skipped']}")
