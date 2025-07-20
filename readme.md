# Cyclic Blood Donation System

Welcome to **Cyclic Blood**, a blood donation system developed by Ahmed Soliman Ghonaim.

## Project Overview

The Cyclic Blood Donation System is a comprehensive web application designed to manage the complete blood donation lifecycle in Egypt. It connects donors, hospitals, blood banks, and patients through an intelligent platform that optimizes blood collection, storage, and distribution based on location, priority, and medical requirements.


- **Root Directory:** `dono system`

---

## Entity Relationship Diagram

```mermaid
erDiagram
    CITY {
        int id PK
        string name
        point location "Geographic coordinates"
        datetime created_at
        datetime updated_at
    }
    
    CUSTOM_USER {
        int id PK
        string username UK
        string email UK
        string password
        string role "donor, hospital, bank_employee"
        int city_id FK
        point location "Auto-set from city"
        datetime date_joined
        bool is_active
        bool is_staff
        bool is_superuser
    }
    
    DONOR {
        int id PK
        string national_id UK
        string name
        string phone
        date last_donation_date
        int total_donations
        date registration_date
        bool can_donate "Auto-calculated"
        bool is_active
        datetime updated_at
        int user_id FK "OneToOne"
    }
    
    HOSPITAL {
        int id PK
        string name
        string address
        string phone
        int user_id FK "OneToOne"
        datetime created_at
        datetime updated_at
    }
    
    BLOOD_BANK {
        int id PK
        string name
        string address
        string phone
        int city_id FK
        point location
        datetime created_at
        datetime updated_at
    }
    
    BANK_EMPLOYEE {
        int id PK
        int user_id FK "OneToOne"
        int blood_bank_id FK
        datetime created_at
        datetime updated_at
    }
    
    PATIENT {
        int id PK
        string name
        int age
        string blood_type "A+, A-, B+, B-, AB+, AB-, O+, O-"
        int hospital_id FK
        datetime created_at
        datetime updated_at
    }
    
    DONATION {
        int id PK
        int donor_id FK
        int bank_id FK
        date donation_date "Auto-set"
        bool virus_test_result "null=pending"
        string blood_type "A+, A-, B+, B-, AB+, AB-, O+, O-"
        int quantity_ml
        string status "pending, accepted, rejected_virus, rejected_time"
        date expiration_date "Auto-calculated (42 days)"
        text rejection_reason
        datetime created_at
        datetime updated_at
    }
    
    BLOOD_STOCK {
        int id PK
        int donation_id FK "OneToOne"
        string blood_type
        string status "available, reserved, used, expired"
        int quantity "From donation"
        int bank_id FK "From donation.bank"
        datetime created_at
        datetime updated_at
    }
    
    BLOOD_REQUESTS {
        int id PK
        int hospital_id FK
        int patient_id FK
        string blood_type "A+, A-, B+, B-, AB+, AB-, O+, O-"
        int quantity
        string status "pending, fulfilled, cancelled"
        string priority "immediate, urgent, normal"
        datetime requested_at "Auto-set"
        datetime updated_at
    }
    
    MATCHER {
        int id PK
        int request_id FK "BloodRequests"
        int stock_id FK "BloodStock"
        int quantity_allocated
        datetime matched_at "Auto-set"
        datetime created_at
        datetime updated_at
    }
    
    NOTIFICATION {
        int id PK
        int user_id FK
        string title
        text message
        string type "donation_status, request_update, system"
        bool is_read
        datetime created_at
        datetime updated_at
    }
        int quantity_allocated
    }
    
    %% Relationships
    CITY ||--o{ CUSTOM_USER : "located_in"
    CITY ||--o{ BLOOD_BANK : "located_in"
    
    CUSTOM_USER ||--o| DONOR : "profile"
    CUSTOM_USER ||--o| HOSPITAL : "profile"
    CUSTOM_USER ||--o| BANK_EMPLOYEE : "profile"
    CUSTOM_USER ||--o{ NOTIFICATION : "receives"
    
    BLOOD_BANK ||--o{ BANK_EMPLOYEE : "employs"
    BLOOD_BANK ||--o{ DONATION : "collects"
    BLOOD_BANK ||--o{ BLOOD_STOCK : "stores"
    
    DONOR ||--o{ DONATION : "makes"
    
    HOSPITAL ||--o{ PATIENT : "treats"
    HOSPITAL ||--o{ BLOOD_REQUESTS : "requests"
    
    PATIENT ||--o{ BLOOD_REQUESTS : "needs"
    
    DONATION ||--o| BLOOD_STOCK : "becomes"
    
    BLOOD_REQUESTS ||--o{ MATCHER : "matched_by"
    BLOOD_STOCK ||--o{ MATCHER : "allocated_from"
```

---

http://127.0.0.1:8080/api/register/

for testing register donor
{
"user": {
"username": "donor_user1",
"email": "donor1@example.com",
"password": "donorpass123",
"role": "donor",
"city": "Cairo"
},
"donor_profile": {
"national_id": "12345678901234",
"name": "Ahmed Donor",
"city": "Cairo",
"phone": "01012345678"
}
}

for testing register hospital

{
"user": {
"username": "hospital_user1",
"email": "hospital1@example.com",
"password": "hospitalpass123",
"role": "hospital",
"city": "Alexandria"
},
"hospital_profile": {
"name": "Alex General Hospital",
"address": "123 Street, Alexandria",
"phone": "01098765432"
}
}


<!-- adding a patient example-->
register as hospital and then /api/patient/ method post 
{
    "name": "mo7sens",
    "age":30,
    "blood_type": "O-"
    
}

<!-- view bloodrequests  -->
/bloodrequests/ method get 

<!-- add  blood requests -->
/bloodrequests/ method post



<!-- ordering is by  fifo created_at-->




## Business Logic & Core Rules

### Critical Business Rules

1. **Blood Type Immutability**: Once a donor donates with a specific blood type, it cannot be changed for future donations
2. **90-Day Donation Interval**: Donors cannot donate again within 90 days of their last donation
3. **Blood Bank Selection**: Donors must select a blood bank when donating, which appears in their donation history
4. **Bank Employee Restrictions**: Bank employees can only manage donations for their assigned blood bank
5. **Location-Based Optimization**: System uses distance and priority algorithms for optimal blood request matching

### User Roles & Permissions

- **Donor**: Register, donate blood, view donation history
- **Hospital**: Register patients, create blood requests, manage patient records
- **Bank Employee**: Manage donations at their blood bank, accept/reject lab tests, monitor stock

## Technical Architecture

### Backend Stack
- **Framework**: Django 5.2 with Django REST Framework
- **Database**: SQLite (development) / PostgreSQL (production)
- **Authentication**: JWT (JSON Web Tokens)
- **Task Queue**: Celery with Redis/RabbitMQ
- **API Documentation**: Comprehensive REST API with detailed endpoints

### Frontend Stack
- **Framework**: React 18 with Create React App
- **UI Library**: Bootstrap 5 for responsive design
- **HTTP Client**: Axios with interceptors for token management
- **Notifications**: React Toastify for user feedback
- **Routing**: React Router DOM for navigation

### Key Features

#### 1. Intelligent Donation Management


#### 2. Location-Based Optimization
```python
# Find nearby blood banks within 50km
nearby_banks = LocationService.find_nearby_blood_banks('Cairo', max_distance_km=50)

# Optimize blood request matching (70% priority, 30% distance)
optimized_matches = LocationService.optimize_blood_request_matching(
    blood_requests, priority_weight=0.7, distance_weight=0.3
)
```

#### 3. Bank Employee Workflow
- **Accept Donation**: Creates stock entry and notifies donor
- **Reject Donation**: Records reason and notifies donor
- **Bank-Specific Access**: Only see donations for their assigned blood bank

## System Lifecycle

### 1. Donor Journey
1. **Registration**: Create account with city and personal details
2. **First Donation**: Select blood type (permanently stored) and blood bank
3. **Lab Testing**: Bank employee accepts/rejects donation
4. **Notification**: Donor receives acceptance/rejection notification
5. **Future Donations**: Blood type locked, 90-day interval enforced

### 2. Hospital Journey
1. **Registration**: Create hospital account with location
2. **Patient Management**: Register patients with blood type and medical details
3. **Blood Requests**: Create requests with priority levels (immediate/urgent/normal)
4. **Matching**: System finds optimal blood banks based on distance and stock
5. **Fulfillment**: Receive blood allocation notifications

### 3. Blood Bank Journey
1. **Employee Registration**: Assign employees to specific blood banks
2. **Donation Processing**: Review incoming donations from donors
3. **Lab Testing**: Accept (create stock) or reject (with reason) donations
4. **Stock Management**: Monitor inventory, expiration dates, and alerts
5. **Request Fulfillment**: Process hospital blood requests


### 2. Priority Scoring System

### 3. Automated Notifications
- **Stock Expiry**: Alerts 7 days before expiration
- **Donation Status**: Immediate notifications on accept/reject
- **System Alerts**: Power outages, storage failures, equipment issues

## API Endpoints

### Core Endpoints
```
POST /api/register/          # User registration
POST /api/login/             # Authentication
GET  /api/profile/           # User profile

POST /api/donation/create/   # Create donation
GET  /api/donation/history/  # Donor history
GET  /api/donation/list/     # Bank employee list
POST /api/donation/accept/<id>/  # Accept donation
POST /api/donation/reject/<id>/  # Reject donation

GET  /api/bloodbanks/        # List blood banks
GET  /api/cities/            # List cities
POST /api/bloodrequests/     # Create blood request
```

## Database Schema

### Key Models
- **User**: Authentication and role management
- **Donor**: Blood type, donation history, 90-day tracking
- **Hospital**: Location, patient management
- **BloodBank**: Location, stock management
- **Donation**: Links donor, bank, status, lab results
- **Stock**: Available blood inventory with expiration
- **BloodRequest**: Hospital requests with priority
- **Notification**: System alerts and user notifications

## Security Implementation

### Authentication & Authorization
- **JWT Tokens**: Secure access and refresh token system
- **Role-Based Access**: Strict permission enforcement
- **API Security**: Protected endpoints with proper validation

### Data Protection
- **Input Validation**: Comprehensive data sanitization
- **SQL Injection Prevention**: Django ORM protection
- **CORS Configuration**: Secure cross-origin requests

## Performance Optimizations

### Backend Optimizations
- **Database Indexing**: Optimized queries for location and user data
- **Caching**: Redis caching for frequently accessed data
- **Async Processing**: Celery for background tasks



## Deployment Architecture

### Production Setup
- **Database**: PostgreSQL 
- **Task Queue**: Celery with rabbitmq broker



