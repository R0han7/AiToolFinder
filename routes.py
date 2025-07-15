from flask import render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import or_, func
from app import app, db
from models import AITool
import logging

@app.route('/')
def index():
    """Home page with featured tools and search"""
    # Get some featured tools
    featured_tools = AITool.query.limit(6).all()
    
    # Get unique departments and categories for filters
    departments = db.session.query(AITool.department).distinct().filter(
        AITool.department.isnot(None)
    ).all()
    categories = db.session.query(AITool.category).distinct().filter(
        AITool.category.isnot(None)
    ).all()
    
    # Process departments and categories to handle comma-separated values
    dept_set = set()
    cat_set = set()
    
    for dept in departments:
        if dept[0]:
            for d in dept[0].split(','):
                dept_set.add(d.strip())
    
    for cat in categories:
        if cat[0]:
            for c in cat[0].split(','):
                cat_set.add(c.strip())
    
    departments_list = sorted(list(dept_set))
    categories_list = sorted(list(cat_set))
    
    return render_template('index.html', 
                         featured_tools=featured_tools,
                         departments=departments_list,
                         categories=categories_list)

@app.route('/search')
def search():
    """Search and filter tools"""
    query = request.args.get('q', '').strip()
    department = request.args.get('department', '').strip()
    category = request.args.get('category', '').strip()
    page = request.args.get('page', 1, type=int)
    per_page = 12
    
    # Start with base query
    tools_query = AITool.query
    
    # Apply search filter
    if query:
        search_filter = or_(
            AITool.name.ilike(f'%{query}%'),
            AITool.overview.ilike(f'%{query}%'),
            AITool.department.ilike(f'%{query}%'),
            AITool.category.ilike(f'%{query}%')
        )
        tools_query = tools_query.filter(search_filter)
    
    # Apply department filter
    if department:
        tools_query = tools_query.filter(AITool.department.ilike(f'%{department}%'))
    
    # Apply category filter
    if category:
        tools_query = tools_query.filter(AITool.category.ilike(f'%{category}%'))
    
    # Paginate results
    tools = tools_query.paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    # Get filter options
    departments = db.session.query(AITool.department).distinct().filter(
        AITool.department.isnot(None)
    ).all()
    categories = db.session.query(AITool.category).distinct().filter(
        AITool.category.isnot(None)
    ).all()
    
    # Process departments and categories
    dept_set = set()
    cat_set = set()
    
    for dept in departments:
        if dept[0]:
            for d in dept[0].split(','):
                dept_set.add(d.strip())
    
    for cat in categories:
        if cat[0]:
            for c in cat[0].split(','):
                cat_set.add(c.strip())
    
    departments_list = sorted(list(dept_set))
    categories_list = sorted(list(cat_set))
    
    return render_template('search_results.html',
                         tools=tools,
                         query=query,
                         selected_department=department,
                         selected_category=category,
                         departments=departments_list,
                         categories=categories_list)

@app.route('/tool/<int:tool_id>')
def tool_detail(tool_id):
    """Show detailed information about a specific tool"""
    tool = AITool.query.get_or_404(tool_id)
    
    # Get related tools (same category or department)
    related_tools = AITool.query.filter(
        AITool.id != tool_id,
        or_(
            AITool.category.ilike(f'%{tool.category}%') if tool.category else False,
            AITool.department.ilike(f'%{tool.department}%') if tool.department else False
        )
    ).limit(4).all()
    
    return render_template('tool_detail.html', tool=tool, related_tools=related_tools)

@app.route('/api/tools/count')
def tools_count():
    """API endpoint to get total number of tools"""
    count = AITool.query.count()
    return jsonify({'count': count})

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    db.session.rollback()
    return render_template('500.html'), 500
