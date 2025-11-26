from flask import Blueprint, request, jsonify, send_file
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import datetime
from models import db, User, Invoice, InvoiceItem
from pdf_generator import generate_invoice_pdf
import io
import os
from werkzeug.utils import secure_filename
from flask import current_app, send_from_directory

ALLOWED_LOGO_EXT = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_LOGO_EXT


def save_user_logo(user_id, file):
    """Helper function to save user logo"""
    if not file or not allowed_file(file.filename):
        return None
    
    filename = secure_filename(file.filename)
    ext = filename.rsplit('.', 1)[1].lower()
    save_dir = os.path.join(current_app.config.get('UPLOAD_FOLDER', 'uploads'), 'logos')
    os.makedirs(save_dir, exist_ok=True)
    save_name = f"user_{user_id}_logo.{ext}"
    save_path = os.path.join(save_dir, save_name)
    file.save(save_path)
    
    # Return relative path
    return os.path.join('uploads', 'logos', save_name)


# ✅ Blueprint create karo
bp = Blueprint("api", __name__)


# Serve uploaded files (if not using a dedicated static web server)
@bp.route('/uploads/<path:filename>')
def serve_uploads(filename):
    upload_root = current_app.config.get('UPLOAD_FOLDER', 'uploads')
    return send_from_directory(upload_root, filename)


# ==================== HEALTH CHECK ====================

@bp.route("/health", methods=["GET"])
def health():
    return {'status': 'healthy'}, 200


# ==================== AUTH CONTROLLERS ====================

@bp.route('/auth/signup', methods=['POST'])
def signup():
    """Register a new user with optional logo upload"""
    try:
        # Check if request has form data (with file) or JSON
        if request.content_type and 'multipart/form-data' in request.content_type:
            # Form data with potential file upload
            email = request.form.get('email')
            password = request.form.get('password')
            full_name = request.form.get('full_name', '')
            company_name = request.form.get('company_name', '')
            address = request.form.get('address', '')
            phone = request.form.get('phone', '')
            logo_file = request.files.get('logo')
        else:
            # JSON data (no file)
            data = request.get_json()
            email = data.get('email')
            password = data.get('password')
            full_name = data.get('full_name', '')
            company_name = data.get('company_name', '')
            address = data.get('address', '')
            phone = data.get('phone', '')
            logo_file = None
        
        # Validation
        if not email or not password:
            return jsonify({'error': 'Email and password are required'}), 400
        
        # Check if user exists
        if User.query.filter_by(email=email).first():
            return jsonify({'error': 'Email already registered'}), 400
        
        # Create user
        user = User(
            email=email,
            full_name=full_name,
            company_name=company_name,
            address=address,
            phone=phone
        )
        user.set_password(password)
        
        db.session.add(user)
        db.session.flush()  # Get user ID before committing
        
        # Handle logo upload if provided
        if logo_file:
            logo_path = save_user_logo(user.id, logo_file)
            if logo_path:
                user.company_logo = logo_path
        
        db.session.commit()
        
        # Create token
        access_token = create_access_token(identity=str(user.id))
        
        return jsonify({
            'message': 'User created successfully',
            'access_token': access_token,
            'user': user.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@bp.route('/auth/login', methods=['POST'])
def login():
    """Login user and return JWT token"""
    try:
        data = request.get_json()
        
        if not data.get('email') or not data.get('password'):
            return jsonify({'error': 'Email and password are required'}), 400
        
        user = User.query.filter_by(email=data['email']).first()
        
        if not user or not user.check_password(data['password']):
            return jsonify({'error': 'Invalid email or password'}), 401
        
        access_token = create_access_token(identity=str(user.id))
        
        return jsonify({
            'message': 'Login successful',
            'access_token': access_token,
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/auth/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """Get current authenticated user"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify({'user': user.to_dict()}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/auth/profile', methods=['PUT'])
@jwt_required()
def edit_profile():
    """Edit user profile with optional logo upload"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Check if request has form data (with file) or JSON
        if request.content_type and 'multipart/form-data' in request.content_type:
            # Form data with potential file upload
            full_name = request.form.get('full_name')
            company_name = request.form.get('company_name')
            email = request.form.get('email')
            password = request.form.get('password')
            address = request.form.get('address')
            phone = request.form.get('phone')
            logo_file = request.files.get('logo')
        else:
            # JSON data (no file)
            data = request.get_json()
            full_name = data.get('full_name')
            company_name = data.get('company_name')
            email = data.get('email')
            password = data.get('password')
            address = data.get('address')
            phone = data.get('phone')
            logo_file = None
        
        # Update fields if provided
        if full_name is not None:
            user.full_name = full_name
        
        if company_name is not None:
            user.company_name = company_name
        
        if address is not None:
            user.address = address
        
        if phone is not None:
            user.phone = phone
        
        if email is not None:
            # Check if email is already taken by another user
            existing_user = User.query.filter_by(email=email).first()
            if existing_user and existing_user.id != user.id:
                return jsonify({'error': 'Email already in use'}), 400
            user.email = email
        
        if password is not None and password.strip():
            user.set_password(password)
        
        # Handle logo upload if provided
        if logo_file:
            # Delete old logo if exists
            if user.company_logo:
                old_logo_path = os.path.join(os.getcwd(), user.company_logo)
                if os.path.exists(old_logo_path):
                    try:
                        os.remove(old_logo_path)
                    except Exception as e:
                        print(f"Error deleting old logo: {e}")
            
            # Save new logo
            logo_path = save_user_logo(user.id, logo_file)
            if logo_path:
                user.company_logo = logo_path
            else:
                return jsonify({'error': 'Invalid file type'}), 400
        
        db.session.commit()
        
        return jsonify({
            'message': 'Profile updated successfully',
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# ==================== INVOICE HELPERS ====================

def generate_invoice_number():
    """Generate unique invoice number"""
    last_invoice = Invoice.query.order_by(Invoice.id.desc()).first()
    if last_invoice:
        num = int(last_invoice.invoice_number.split('-')[1]) + 1
    else:
        num = 1
    return f'INV-{num:05d}'


# ==================== INVOICE ROUTES ====================

@bp.route('/invoices', methods=['GET'])
@jwt_required()
def get_invoices():
    """Get all invoices for current user"""
    try:
        user_id = get_jwt_identity()
        invoices = Invoice.query.filter_by(user_id=user_id).order_by(Invoice.created_at.desc()).all()
        
        return jsonify({
            'invoices': [invoice.to_dict() for invoice in invoices]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/invoices/<int:invoice_id>', methods=['GET'])
@jwt_required()
def get_invoice(invoice_id):
    """Get single invoice by ID"""
    try:
        user_id = get_jwt_identity()
        invoice = Invoice.query.filter_by(id=invoice_id, user_id=user_id).first()
        
        if not invoice:
            return jsonify({'error': 'Invoice not found'}), 404
        
        return jsonify({'invoice': invoice.to_dict(include_items=True)}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/invoices', methods=['POST'])
@jwt_required()
def create_invoice():
    """Create new invoice"""
    print("CREATE INVOICE CALLED")
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        print("="*50)
        print("RECEIVED DATA:", data)
        print("="*50)
        
        # Validation
        if not data.get('client_name'):
            return jsonify({'error': 'Client name is required'}), 400
        
        if not data.get('items') or len(data['items']) == 0:
            return jsonify({'error': 'At least one item is required'}), 400
        
        # Parse dates safely
        try:
            if data.get('invoice_date'):
                invoice_date_str = data['invoice_date'].split('T')[0]
                invoice_date = datetime.strptime(invoice_date_str, '%Y-%m-%d').date()
                print(f"Parsed invoice_date: {invoice_date}")
            else:
                invoice_date = datetime.utcnow().date()
                print(f"Using default invoice_date: {invoice_date}")
            
            if data.get('due_date'):
                due_date_str = data['due_date'].split('T')[0]
                due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date()
                print(f"Parsed due_date: {due_date}")
            else:
                due_date = None
                print("No due_date provided")
        except ValueError as e:
            print(f"DATE PARSING ERROR: {str(e)}")
            return jsonify({'error': f'Invalid date format: {str(e)}'}), 400
        except Exception as e:
            print(f"UNEXPECTED DATE ERROR: {str(e)}")
            return jsonify({'error': f'Date error: {str(e)}'}), 400
        
        # Create invoice
        print("Creating invoice object...")
        invoice = Invoice(
            invoice_number=generate_invoice_number(),
            user_id=user_id,
            client_name=data['client_name'],
            client_email=data.get('client_email', ''),
            client_address=data.get('client_address', ''),
            invoice_date=invoice_date,
            due_date=due_date,
            notes=data.get('notes', ''),
            tax_rate=float(data.get('tax_rate', 0.0)),
            status=data.get('status', 'draft')
        )
        
        db.session.add(invoice)
        db.session.flush()
        print(f"Invoice created with ID: {invoice.id}")
        
        # Add items
        print(f"Adding {len(data['items'])} items...")
        for idx, item_data in enumerate(data['items']):
            print(f"Item {idx}: {item_data}")
            item = InvoiceItem(
                invoice_id=invoice.id,
                description=item_data['description'],
                quantity=int(item_data['quantity']),
                unit_price=float(item_data['unit_price'])
            )
            item.calculate_total()
            db.session.add(item)
            print(f"Item {idx} added: {item.description} - ${item.total}")
        
        db.session.flush()
        invoice.calculate_totals()
        print(f"Invoice totals calculated: Subtotal=${invoice.subtotal}, Total=${invoice.total}")
        
        db.session.commit()
        print("Invoice committed successfully!")
        
        return jsonify({
            'message': 'Invoice created successfully',
            'invoice': invoice.to_dict(include_items=True)
        }), 201
        
    except Exception as e:
        db.session.rollback()
        print("="*50)
        print(f"ERROR CREATING INVOICE: {str(e)}")
        print(f"ERROR TYPE: {type(e).__name__}")
        import traceback
        print("FULL TRACEBACK:")
        traceback.print_exc()
        print("="*50)
        return jsonify({'error': str(e)}), 500


@bp.route('/invoices/<int:invoice_id>', methods=['PUT'])
@jwt_required()
def update_invoice(invoice_id):
    """Update existing invoice"""
    try:
        user_id = get_jwt_identity()
        invoice = Invoice.query.filter_by(id=invoice_id, user_id=user_id).first()
        
        if not invoice:
            return jsonify({'error': 'Invoice not found'}), 404
        
        data = request.get_json()
        
        invoice.client_name = data.get('client_name', invoice.client_name)
        invoice.client_email = data.get('client_email', invoice.client_email)
        invoice.client_address = data.get('client_address', invoice.client_address)
        invoice.notes = data.get('notes', invoice.notes)
        invoice.tax_rate = float(data.get('tax_rate', invoice.tax_rate))
        invoice.status = data.get('status', invoice.status)
        
        try:
            if data.get('invoice_date'):
                invoice_date_str = data['invoice_date'].split('T')[0]
                invoice.invoice_date = datetime.strptime(invoice_date_str, '%Y-%m-%d').date()
            
            if data.get('due_date'):
                due_date_str = data['due_date'].split('T')[0]
                invoice.due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date()
        except ValueError as e:
            return jsonify({'error': f'Invalid date format: {str(e)}'}), 400
        
        if 'items' in data:
            InvoiceItem.query.filter_by(invoice_id=invoice.id).delete()
            
            for item_data in data['items']:
                item = InvoiceItem(
                    invoice_id=invoice.id,
                    description=item_data['description'],
                    quantity=int(item_data['quantity']),
                    unit_price=float(item_data['unit_price'])
                )
                item.calculate_total()
                db.session.add(item)
        
        db.session.flush()
        invoice.calculate_totals()
        
        db.session.commit()
        
        return jsonify({
            'message': 'Invoice updated successfully',
            'invoice': invoice.to_dict(include_items=True)
        }), 200
        
    except Exception as e:
        db.session.rollback()
        print(f"Error updating invoice: {str(e)}")
        return jsonify({'error': str(e)}), 500


@bp.route('/invoices/<int:invoice_id>', methods=['DELETE'])
@jwt_required()
def delete_invoice(invoice_id):
    """Delete invoice"""
    try:
        user_id = get_jwt_identity()
        invoice = Invoice.query.filter_by(id=invoice_id, user_id=user_id).first()
        
        if not invoice:
            return jsonify({'error': 'Invoice not found'}), 404
        
        db.session.delete(invoice)
        db.session.commit()
        
        return jsonify({'message': 'Invoice deleted successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@bp.route('/invoices/<int:invoice_id>/pdf', methods=['GET'])
@jwt_required()
def download_pdf(invoice_id):
    """Download invoice as PDF"""
    try:
        user_id = get_jwt_identity()
        invoice = Invoice.query.filter_by(id=invoice_id, user_id=user_id).first()
        
        if not invoice:
            return jsonify({'error': 'Invoice not found'}), 404
        
        user = User.query.get(user_id)
        
        logo_path = None
        if getattr(user, 'company_logo', None):
            # convert relative path to absolute server path
            logo_path = os.path.join(os.getcwd(), user.company_logo)
        
        pdf_bytes = generate_invoice_pdf(invoice, user, logo_path=logo_path,
                                        theme_color="#0ea5a4",
                                        currency_symbol="$")
        
        return send_file(io.BytesIO(pdf_bytes), mimetype='application/pdf',
                        as_attachment=True, download_name=f"{invoice.invoice_number}.pdf")
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500