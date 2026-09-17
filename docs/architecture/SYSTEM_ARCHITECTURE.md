# Wasteworx Platform — System Architecture

## 1. Purpose

Wasteworx Platform is a centralized digital waste management, operations,
finance, maintenance, compliance, and AI-assisted management platform.

The system is designed around:

> One system → One database → One source of truth → One management view

---

## 2. Technology Stack

### Frontend
- React
- Vite
- JavaScript
- REST API integration

### Backend
- Python
- Flask
- Flask-CORS
- REST APIs

### Database
- PostgreSQL

### Authentication
- JWT-based authentication
- Role-Based Access Control (RBAC)
- Password security
- Future MFA support where required

### AI
- AI management assistant
- AI equipment diagnostics
- Human authorization required for consequential decisions

### Integrations
Future integrations may include:
- M-PESA/payment services
- GPS/location services
- Weighing systems
- Vehicle/telematics systems
- Notifications
- Document/report generation
- External AI services

Third-party integrations will remain separated from the core business logic.

---

## 3. High-Level Architecture

```text
                    ┌─────────────────────────┐
                    │         USERS           │
                    │ Staff / Customers /     │
                    │ Managers / Consultants  │
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │    React Frontend       │
                    │    Web / Mobile UI      │
                    └────────────┬────────────┘
                                 │
                            REST / JSON
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │       Flask API         │
                    │ Authentication / RBAC   │
                    │ Business Logic          │
                    │ Validation / Workflows  │
                    └────────────┬────────────┘
                                 │
              ┌──────────────────┼──────────────────┐
              │                  │                  │
              ▼                  ▼                  ▼
       ┌────────────┐    ┌──────────────┐   ┌──────────────┐
       │ PostgreSQL │    │ AI Services  │   │ Integrations │
       │ Database   │    │ Assistant /  │   │ Payments /   │
       │            │    │ Diagnostics  │   │ GPS / Weighing│
       └────────────┘    └──────────────┘   └──────────────┘                                                                                                                                4. Core Principles
Single Source of Truth

Operational records should be stored centrally and linked through
stable identifiers.

Traceability

Important records must be traceable from creation through completion.

Human Authorization

AI provides recommendations and analysis.

AI must not independently:

approve hazardous waste treatment
approve financial transactions
modify safety controls
declare equipment safe
close critical incidents
make regulatory declarations
Auditability

Important changes must retain:

user
date/time
action
affected record
previous value
new value
approval information where applicable
Security

The platform must use:

authentication
authorization
secure APIs
protected credentials
access controls
backups
audit logging
account deactivation
5. Main Data Flow
Customer
   ↓
Contract
   ↓
Waste / Service Request
   ↓
Collection
   ↓
Vehicle + Driver
   ↓
Consignment
   ↓
Weighing
   ↓
Waste Acceptance / Classification
   ↓
Treatment / Recovery
   ↓
Residuals
   ↓
Cost
   ↓
Invoice
   ↓
Payment
   ↓
Profitability
6. Equipment Data Flow
Asset
   ↓
Operating Data
   ↓
Fault / Alarm / Observation
   ↓
AI Diagnostic
   ↓
Human Review
   ↓
Consultancy Escalation (if required)
   ↓
Work Order
   ↓
Repair
   ↓
Testing
   ↓
Verification
   ↓
Maintenance History
7. Backend Organization

The backend will be organized by responsibility:

app/
├── api/
│   ├── auth/
│   ├── customers/
│   ├── contracts/
│   ├── collections/
│   ├── waste/
│   ├── weighing/
│   ├── treatment/
│   ├── residuals/
│   ├── billing/
│   ├── finance/
│   ├── procurement/
│   ├── stores/
│   ├── assets/
│   ├── maintenance/
│   ├── compliance/
│   ├── documents/
│   ├── notifications/
│   └── ai/
│
├── models/
├── schemas/
├── services/
├── core/
└── utils/

This structure may evolve as implementation progresses.

8. Frontend Organization

The React application will eventually be organized around:

src/
├── components/
├── pages/
├── layouts/
├── services/
├── hooks/
├── context/
├── utils/
├── assets/
└── App.jsx

The frontend will consume the Flask REST API rather than accessing
the database directly.

9. Deployment Direction

Development:

React/Vite
    ↓
Flask API
    ↓
PostgreSQL

Production deployment will separate:

frontend
backend/API
database
external services

Deployment infrastructure will be finalized after the core application
architecture and integrations are established.
