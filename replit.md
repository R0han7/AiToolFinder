# AI Tools Directory

## Overview

This is a Flask-based web application that provides a searchable directory of AI tools. The application allows users to browse, search, and filter AI tools by department and category. It features a clean, responsive interface built with Bootstrap and includes functionality for importing tool data from CSV files.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Backend Framework
- **Flask**: Python web framework chosen for its simplicity and rapid development capabilities
- **SQLAlchemy**: ORM for database operations with PostgreSQL backend
- **Werkzeug ProxyFix**: Middleware for handling proxy headers in deployment

### Frontend Architecture
- **Server-side rendering**: Uses Flask's Jinja2 templating engine
- **Bootstrap 5**: CSS framework for responsive design
- **Font Awesome**: Icon library for UI elements
- **Google Fonts**: Inter font family for modern typography

### Database Design
- **Single Entity Model**: AITool model with fields for name, department, category, overview, and reference URL
- **Indexing Strategy**: Multiple indexes for search performance on name, department, category, and full-text search
- **Comma-separated Values**: Departments and categories stored as comma-separated strings for multi-value support

## Key Components

### Models (`models.py`)
- **AITool**: Core entity representing an AI tool with search-optimized indexes
- **Helper Methods**: `get_departments_list()` and `get_categories_list()` for parsing comma-separated values

### Routes (`routes.py`)
- **Home Route** (`/`): Displays featured tools and filter options
- **Search Route** (`/search`): Handles tool search with pagination and filtering
- **Tool Detail Route** (`/tool/<int:id>`): Shows individual tool details

### Templates
- **Base Template**: Common layout with navigation and Bootstrap integration
- **Index Template**: Hero section with search form and featured tools
- **Search Results**: Paginated tool listings with filter controls
- **Tool Detail**: Individual tool information page

### Data Import (`import_data.py`)
- **CSV Processing**: Imports tool data from CSV files with data cleaning
- **Text Normalization**: Cleans and validates input data
- **URL Validation**: Ensures proper URL formatting

## Data Flow

1. **User Request**: User visits homepage or searches for tools
2. **Route Processing**: Flask routes handle requests and query database
3. **Database Query**: SQLAlchemy performs filtered queries with pagination
4. **Template Rendering**: Jinja2 templates render HTML with tool data
5. **Response**: Server returns rendered HTML to browser

### Search Flow
1. User enters search query and/or selects filters
2. Search route processes parameters and builds database query
3. Results are paginated and returned with filter metadata
4. Template displays results with pagination controls

## External Dependencies

### Python Packages
- **Flask**: Web framework
- **Flask-SQLAlchemy**: Database ORM
- **Werkzeug**: WSGI utilities
- **psycopg2**: PostgreSQL adapter (implied by database URL)

### Frontend Libraries
- **Bootstrap 5**: CSS framework (CDN)
- **Font Awesome**: Icons (CDN)
- **Google Fonts**: Typography (CDN)

### Database
- **PostgreSQL**: Primary database hosted on Neon (cloud PostgreSQL service)
- **Connection Pooling**: Configured with pool recycling and pre-ping for reliability

## Deployment Strategy

### Configuration
- **Environment Variables**: Database URL and session secret from environment
- **Development Mode**: Debug mode enabled for development
- **Production Readiness**: ProxyFix middleware for reverse proxy deployment

### Database Management
- **Auto-migration**: `db.create_all()` creates tables on startup
- **Connection Pooling**: Configured for production reliability with 300-second pool recycle

### Static Assets
- **CSS/JS**: Served from `static/` directory
- **External CDNs**: Bootstrap, Font Awesome, and Google Fonts loaded from CDNs

### Server Configuration
- **Host**: Configured to run on `0.0.0.0:5000`
- **WSGI**: Compatible with production WSGI servers
- **Logging**: Debug-level logging enabled for development

## Key Features

### Search Functionality
- Full-text search across tool names and descriptions
- Department and category filtering
- Pagination for large result sets
- Auto-submit filters for better UX

### User Interface
- Responsive design with Bootstrap
- Hover effects on tool cards
- Hero section with prominent search
- Filter chips for quick navigation

### Data Management
- CSV import functionality for bulk data loading
- Data validation and cleaning
- Efficient database indexing for search performance