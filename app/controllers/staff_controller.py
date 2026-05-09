# =========================================================
# FILE: app/controllers/staff_controller.py
# =========================================================

from flask import Blueprint
from flask import render_template
from flask import session
from flask import redirect

from app.models.document_model import DocumentModel


staff_bp = Blueprint(
    'staff',
    __name__
)


# =========================================================
# CHECK STAFF
# =========================================================
def check_staff():

    if 'user_id' not in session:
        return False

    if session.get('role') != 'staff':
        return False

    return True


# =========================================================
# STAFF DASHBOARD
# =========================================================
@staff_bp.route('/staff')
def staff_dashboard():

    if not check_staff():
        return redirect('/')

    assigned_documents = (
        DocumentModel.get_documents_by_assignee(
            session['user_id']
        )
    )

    processing_documents = len(
        DocumentModel.get_documents_by_status(
            "processing"
        )
    )

    approved_documents = len(
        DocumentModel.get_documents_by_status(
            'approved'
        )
    )

    return render_template(
        'staff/dashboard.html',

        assigned_documents=assigned_documents,

        processing_documents=processing_documents,

        approved_documents=approved_documents
    )


# =========================================================
# ASSIGNED DOCUMENTS
# =========================================================
@staff_bp.route('/staff/assigned-documents')
def assigned_documents():

    if not check_staff():
        return redirect('/')

    documents = (
        DocumentModel.get_documents_by_assignee(
            session['user_id']
        )
    )

    return render_template(
        'staff/assigned_documents.html',
        documents=documents
    )


# =========================================================
# PROCESSING DOCUMENTS
# =========================================================
@staff_bp.route('/staff/processing-documents')
def processing_documents():

    if not check_staff():
        return redirect('/')

    documents = (
        DocumentModel.get_documents_by_status(
            'processing'
        )
    )

    return render_template(
        'staff/processing_documents.html',
        documents=documents
    )


# =========================================================
# APPROVED DOCUMENTS
# =========================================================
@staff_bp.route('/staff/approved-documents')
def approved_documents():

    if not check_staff():
        return redirect('/')

    documents = (
        DocumentModel.get_documents_by_status(
            'approved'
        )
    )

    return render_template(
        'staff/approved_documents.html',
        documents=documents
    )