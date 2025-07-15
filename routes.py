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

@app.route('/admin')
def admin_dashboard():
    """Admin dashboard"""
    total_tools = AITool.query.count()
    
    # Get department and category counts
    departments = db.session.query(AITool.department).distinct().filter(
        AITool.department.isnot(None)
    ).all()
    categories = db.session.query(AITool.category).distinct().filter(
        AITool.category.isnot(None)
    ).all()
    
    # Process to get unique count
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
    
    return render_template('admin/dashboard.html', 
                         total_tools=total_tools,
                         total_departments=len(dept_set),
                         total_categories=len(cat_set))

@app.route('/admin/tools')
def admin_tools():
    """Admin page to manage tools"""
    page = request.args.get('page', 1, type=int)
    per_page = 20
    
    tools = AITool.query.paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return render_template('admin/tools.html', tools=tools)

@app.route('/admin/tools/add', methods=['GET', 'POST'])
def add_tool():
    """Add a new AI tool"""
    if request.method == 'POST':
        try:
            # Get form data
            name = request.form.get('name', '').strip()
            department = request.form.get('department', '').strip()
            category = request.form.get('category', '').strip()
            overview = request.form.get('overview', '').strip()
            reference_url = request.form.get('reference_url', '').strip()
            
            # Validate required fields
            if not name:
                flash('Tool name is required', 'error')
                return render_template('admin/add_tool.html')
            
            # Check if tool already exists
            existing_tool = AITool.query.filter_by(name=name).first()
            if existing_tool:
                flash('A tool with this name already exists', 'error')
                return render_template('admin/add_tool.html')
            
            # Clean URL
            if reference_url and not reference_url.startswith('http'):
                reference_url = 'https://' + reference_url
            
            # Create new tool
            new_tool = AITool(
                name=name,
                department=department if department else None,
                category=category if category else None,
                overview=overview if overview else None,
                reference_url=reference_url if reference_url else None
            )
            
            db.session.add(new_tool)
            db.session.commit()
            
            flash('Tool added successfully!', 'success')
            return redirect(url_for('admin_tools'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding tool: {str(e)}', 'error')
            return render_template('admin/add_tool.html')
    
    return render_template('admin/add_tool.html')

@app.route('/admin/tools/edit/<int:tool_id>', methods=['GET', 'POST'])
def edit_tool(tool_id):
    """Edit an existing AI tool"""
    tool = AITool.query.get_or_404(tool_id)
    
    if request.method == 'POST':
        try:
            # Get form data
            name = request.form.get('name', '').strip()
            department = request.form.get('department', '').strip()
            category = request.form.get('category', '').strip()
            overview = request.form.get('overview', '').strip()
            reference_url = request.form.get('reference_url', '').strip()
            
            # Validate required fields
            if not name:
                flash('Tool name is required', 'error')
                return render_template('admin/edit_tool.html', tool=tool)
            
            # Check if another tool with the same name exists
            existing_tool = AITool.query.filter(
                AITool.name == name,
                AITool.id != tool_id
            ).first()
            if existing_tool:
                flash('A tool with this name already exists', 'error')
                return render_template('admin/edit_tool.html', tool=tool)
            
            # Clean URL
            if reference_url and not reference_url.startswith('http'):
                reference_url = 'https://' + reference_url
            
            # Update tool
            tool.name = name
            tool.department = department if department else None
            tool.category = category if category else None
            tool.overview = overview if overview else None
            tool.reference_url = reference_url if reference_url else None
            
            db.session.commit()
            
            flash('Tool updated successfully!', 'success')
            return redirect(url_for('admin_tools'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating tool: {str(e)}', 'error')
            return render_template('admin/edit_tool.html', tool=tool)
    
    return render_template('admin/edit_tool.html', tool=tool)

@app.route('/admin/tools/delete/<int:tool_id>', methods=['POST'])
def delete_tool(tool_id):
    """Delete an AI tool"""
    tool = AITool.query.get_or_404(tool_id)
    
    try:
        db.session.delete(tool)
        db.session.commit()
        flash('Tool deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting tool: {str(e)}', 'error')
    
    return redirect(url_for('admin_tools'))

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    db.session.rollback()
    return render_template('500.html'), 500
