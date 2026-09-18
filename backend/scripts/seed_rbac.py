from app import create_app
from app.extensions import db
from app.models import Role, Permission

ROLES = [
    ("Director", "Executive oversight"),
    ("General Manager", "General management"),
    ("Operations Manager", "Operations management"),
    ("Technical Manager", "Technical management"),
    ("HSE / Environmental", "Health, safety and environmental"),
    ("Finance Manager", "Financial management"),
    ("Accountant", "Accounting"),
    ("Procurement", "Procurement"),
    ("Stores", "Stores and inventory"),
    ("Sales", "Sales"),
    ("Customer Service", "Customer support"),
    ("Supervisor", "Operations supervision"),
    ("Technician", "Technical work"),
    ("Driver", "Vehicle and collection operations"),
    ("Waste Handler", "Waste handling"),
    ("Admin", "System administration"),
]

PERMISSIONS = [
    ("users.view", "View users"),
    ("users.create", "Create users"),
    ("users.update", "Update users"),
    ("users.deactivate", "Deactivate users"),
    ("customers.view", "View customers"),
    ("customers.create", "Create customers"),
    ("customers.update", "Update customers"),
    ("contracts.view", "View contracts"),
    ("contracts.create", "Create contracts"),
    ("contracts.approve", "Approve contracts"),
    ("collections.view", "View collections"),
    ("collections.create", "Create collection records"),
    ("collections.update", "Update collections"),
    ("waste.view", "View waste"),
    ("waste.create", "Create waste records"),
    ("waste.accept", "Accept waste"),
    ("waste.quarantine", "Quarantine waste"),
    ("weighing.view", "View weighing"),
    ("weighing.create", "Create weighing records"),
    ("treatment.view", "View treatment"),
    ("treatment.create", "Create treatment records"),
    ("residuals.view", "View residuals"),
    ("residuals.create", "Create residual records"),
    ("invoices.view", "View invoices"),
    ("invoices.create", "Create invoices"),
    ("invoices.approve", "Approve invoices"),
    ("payments.view", "View payments"),
    ("payments.create", "Record payments"),
    ("payments.approve", "Approve payments"),
    ("costs.view", "View costs"),
    ("costs.create", "Create costs"),
    ("procurement.view", "View procurement"),
    ("procurement.create", "Create procurement"),
    ("procurement.approve", "Approve procurement"),
    ("stores.view", "View stores"),
    ("stores.create", "Create inventory transactions"),
    ("stores.update", "Update inventory"),
    ("assets.view", "View assets"),
    ("assets.create", "Create assets"),
    ("assets.update", "Update assets"),
    ("maintenance.view", "View maintenance"),
    ("maintenance.create", "Create maintenance"),
    ("maintenance.approve", "Approve maintenance"),
    ("reports.view", "View reports"),
    ("reports.export", "Export reports"),
    ("compliance.view", "View compliance"),
    ("compliance.create", "Create compliance records"),
    ("documents.view", "View documents"),
    ("documents.upload", "Upload documents"),
    ("audit.view", "View audit trail"),
    ("ai.use", "Use AI assistance"),
    ("ai.review", "Review AI recommendations"),
    ("settings.manage", "Manage system settings"),
]

def seed():
    app = create_app()

    with app.app_context():
        permissions = {}

        for name, description in PERMISSIONS:
            permission = Permission.query.filter_by(name=name).first()

            if not permission:
                permission = Permission(
                    name=name,
                    description=description
                )
                db.session.add(permission)

            permissions[name] = permission

        for name, description in ROLES:
            role = Role.query.filter_by(name=name).first()

            if not role:
                role = Role(
                    name=name,
                    description=description
                )
                db.session.add(role)

        db.session.commit()

        director = Role.query.filter_by(name="Director").first()
        director.permissions = list(permissions.values())

        admin = Role.query.filter_by(name="Admin").first()

        admin_names = [
            "users.view",
            "users.create",
            "users.update",
            "users.deactivate",
            "reports.view",
            "reports.export",
            "documents.view",
            "documents.upload",
            "audit.view",
            "settings.manage",
        ]

        admin.permissions = [
            permissions[name] for name in admin_names
        ]

        db.session.commit()

        print("RBAC seed completed.")
        print("Roles:", Role.query.count())
        print("Permissions:", Permission.query.count())
        print("Director permissions:", len(director.permissions))
        print("Admin permissions:", len(admin.permissions))

if __name__ == "__main__":
    seed()
