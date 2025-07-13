
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
        string email
        string phone
        date birth_date
        string gender
        string city
        string address
        date last_donation_date
        int total_donations
        datetime created_at
        datetime updated_at
    }
    BLOOD_BANK {
        int id PK
        string name
        string city
        string address
        string phone
        string operating_hours
        datetime created_at
    }
    DONATION {
        int id PK
        int donor_id FK
        int blood_bank_id FK
        date donation_date
        boolean virus_test_result
        string blood_type
        int quantity_ml
        string status
        date expiration_date
        string rejection_reason
        datetime created_at
        datetime updated_at
    }
    STOCK {
        int id PK
        int donation_id FK
        string status
        datetime created_at
        datetime updated_at
    }
    HOSPITAL {
        int id PK
        string name
        string city
        string address
        string phone
        string contact_person
        datetime created_at
    }
    REQUEST {
        int id PK
        int hospital_id FK
        string blood_type
        int quantity
        string status
        string priority
        datetime requested_date
        datetime required_by_date
        string notes
        datetime created_at
        datetime updated_at
    }
    MATCHER {
        int id PK
        int request_id FK
        int stock_id FK
        decimal distance_km
        decimal match_score
        datetime created_at
    }
    NOTIFICATION {
        int id PK
        int donor_id FK
        int donation_id FK
        string message
        string status
        datetime sent_at
        boolean via_email
        boolean seen
        datetime created_at
    }
    DONOR ||--o{ DONATION : "makes"
    BLOOD_BANK ||--o{ DONATION : "collects"
    DONATION ||--|| STOCK : "becomes"
    HOSPITAL ||--o{ REQUEST : "makes"
    REQUEST ||--o{ MATCHER : "matched_by"
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
    "email": "donor1@example.com",
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

