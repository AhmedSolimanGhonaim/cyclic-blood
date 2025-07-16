# Cyclic Blood Donation System

Welcome to **Cyclic Blood**, a blood donation system developed by Ahmed Soliman Ghonaim.

- **Root Directory:** `dono system`

---

## Entity Relationship Diagram

```mermaid
erDiagram
    DONOR {
        int id PK
        string national_id UK
        string name
        string phone
        date last_donation_date
        int total_donations
        date registration_date
        bool can_donate
        bool is_active
        datetime updated_at
        int user_id FK
    }
    BLOOD_BANK {
        int id PK
        string name
        string address
        string phone
        datetime created_at
    }
    DONATION {
        int id PK
        int donor_id FK
        int blood_bank_id FK
        date donation_date
        bool virus_test_result
        string blood_type
        int quantity_ml
        string status
        date expiration_date
        string rejection_reason
    }
    STOCK {
        int id PK
        int donation_id FK
        string blood_type
        string status
        datetime created_at
        datetime updated_at
    }
    HOSPITAL {
        int id PK
        string name
        string address
        string phone
        int user_id FK
        datetime created_at
    }
    PATIENT {
        int id PK
        string name
        int age
        string blood_type
        int hospital_id FK
        string status
        datetime created_at
        datetime updated_at
    }
    BLOOD_REQUESTS {
        int id PK
        int hospital_id FK
        int patient_id FK
        string blood_type
        int quantity
        string status
        string priority
        datetime requested_at
        datetime updated_at
    }
    MATCHER {
        int id PK
        int request_id FK
        int stock_id FK
        int quantity_allocated
    }
    NOTIFICATION {
        int id PK
        string message
        bool status
        datetime sent_at
        bool via_email
        int donation_id FK
        int donor_id FK
    }
    USER {
        int id PK
        string username
        string email
        string role
        string city
    }
    USER ||--o{ DONOR : "profile"
    USER ||--o{ HOSPITAL : "profile"
    DONOR ||--o{ DONATION : "makes"
    BLOOD_BANK ||--o{ DONATION : "collects"
    DONATION ||--|| STOCK : "becomes"
    HOSPITAL ||--o{ PATIENT : "has"
    HOSPITAL ||--o{ BLOOD_REQUESTS : "makes"
    PATIENT ||--o{ BLOOD_REQUESTS : "requests"
    BLOOD_REQUESTS ||--o{ MATCHER : "matched_by"
    STOCK ||--o{ MATCHER : "matched_in"
    DONOR ||--o{ NOTIFICATION : "receives"
    DONATION ||--o{ NOTIFICATION : "about"
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
