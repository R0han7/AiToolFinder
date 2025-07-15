from app import db
from sqlalchemy import Index

class AITool(db.Model):
    __tablename__ = 'ai_tools'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    department = db.Column(db.String(200), nullable=True)
    category = db.Column(db.String(200), nullable=True)
    overview = db.Column(db.Text, nullable=True)
    reference_url = db.Column(db.String(500), nullable=True)
    
    # Add indexes for better search performance
    __table_args__ = (
        Index('idx_name', 'name'),
        Index('idx_department', 'department'),
        Index('idx_category', 'category'),
        Index('idx_search', 'name', 'overview', 'department', 'category'),
    )
    
    def __repr__(self):
        return f'<AITool {self.name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'department': self.department,
            'category': self.category,
            'overview': self.overview,
            'reference_url': self.reference_url
        }
    
    def get_departments_list(self):
        """Parse department string and return list of departments"""
        if not self.department:
            return []
        return [dept.strip() for dept in self.department.split(',')]
    
    def get_categories_list(self):
        """Parse category string and return list of categories"""
        if not self.category:
            return []
        return [cat.strip() for cat in self.category.split(',')]
