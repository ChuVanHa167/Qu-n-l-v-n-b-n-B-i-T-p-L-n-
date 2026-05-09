# =========================================================
# FILE: app/controllers/employee_controller.py
# =========================================================

from flask import Blueprint
from flask import render_template
from flask import session
from flask import redirect

from app.models.document_model import DocumentModel


employee_bp = Blueprint(
    'employee',
    __name__
)


# =========================================================
# CHECK EMPLOYEE
# =========================================================
def check_employee():

    if 'user_id' not in session:
        return False

    return session.get('role') == 'employee'


# =========================================================
# EMPLOYEE DASHBOARD
# =========================================================
@employee_bp.route('/employee')
def employee_dashboard():

    if not check_employee():
        return redirect('/')

    total_documents = DocumentModel.count_documents()

    pending_documents = DocumentModel.count_by_status(
        'pending'
    )

    approved_documents = DocumentModel.count_by_status(
        'approved'
    )

    rejected_documents = DocumentModel.count_by_status(
        'rejected'
    )

    recent_documents = (
        DocumentModel.get_documents_by_creator(
            session['user_id']
        )
    )

    return render_template(
        'employee/dashboard.html',
        processing_documents=0,
        total_documents=total_documents,

        pending_documents=pending_documents,

        approved_documents=approved_documents,

        rejected_documents=rejected_documents,

        recent_documents=recent_documents
    )


# =========================================================
# MY DOCUMENTS
# =========================================================
@employee_bp.route('/employee/my-documents')
def my_documents():

    if not check_employee():
        return redirect('/')

    documents = (
        DocumentModel.get_documents_by_creator(
            session['user_id']
        )
    )

    return render_template(
        'employee/my_documents.html',
        documents=documents
    )