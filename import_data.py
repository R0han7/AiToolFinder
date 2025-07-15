import csv
import os
from app import app, db
from models import AITool

def clean_text(text):
    """Clean and normalize text data"""
    if not text or text.strip() == '':
        return None
    # Remove extra whitespace and newlines
    cleaned = ' '.join(text.strip().split())
    return cleaned if cleaned else None

def clean_url(url):
    """Clean and validate URL"""
    if not url or url.strip() == '':
        return None
    url = url.strip()
    if not url.startswith('http'):
        url = 'https://' + url
    return url

def import_csv_data():
    """Import AI tools data from CSV file"""
    csv_file_path = 'attached_assets/Guide to AI Tools 230a5ed5fb8d80678183c5fdf6fafa09_1752588089851.csv'
    
    if not os.path.exists(csv_file_path):
        print(f"CSV file not found: {csv_file_path}")
        return
    
    with app.app_context():
        # Clear existing data
        AITool.query.delete()
        db.session.commit()
        
        with open(csv_file_path, 'r', encoding='utf-8') as file:
            # Skip the BOM if present
            content = file.read()
            if content.startswith('\ufeff'):
                content = content[1:]
            
            csv_reader = csv.DictReader(content.splitlines())
            
            imported_count = 0
            for row in csv_reader:
                try:
                    # Skip empty rows or rows without tool name
                    if not row.get('AI Tool') or row['AI Tool'].strip() == '':
                        continue
                    
                    # Clean the data
                    name = clean_text(row.get('AI Tool'))
                    department = clean_text(row.get('Department'))
                    category = clean_text(row.get('Category'))
                    overview = clean_text(row.get('Overview'))
                    reference_url = clean_url(row.get('Reference'))
                    
                    # Skip if no name
                    if not name:
                        continue
                    
                    # Create new tool
                    tool = AITool(
                        name=name,
                        department=department,
                        category=category,
                        overview=overview,
                        reference_url=reference_url
                    )
                    
                    db.session.add(tool)
                    imported_count += 1
                    
                except Exception as e:
                    print(f"Error processing row: {row}")
                    print(f"Error: {e}")
                    continue
            
            db.session.commit()
            print(f"Successfully imported {imported_count} AI tools")

if __name__ == '__main__':
    import_csv_data()
