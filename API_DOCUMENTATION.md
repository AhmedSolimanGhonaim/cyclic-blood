# Cyclic Blood Donation System - Comprehensive API Documentation

## 1. Introduction

This document provides a comprehensive guide to the Cyclic Blood Donation System's backend API. It is intended for frontend developers to understand user roles, authentication, data models, and how to interact with every API endpoint.

The system is built with Django and Django REST Framework, using JWT for authentication. It manages the lifecycle of blood donations, from the donor to the blood bank, and fulfills requests from hospitals.

---

## 2. User Roles & Permissions

The system defines four primary user roles, each with specific capabilities:

-   **Donor**: Can register, manage their profile, create donation records, and view their donation history.
-   **Hospital**: Can register, manage their profile, register patients under their care, and create blood requests for those patients.
-   **Bank Employee**: An employee of a blood bank. They manage incoming donations at their assigned bank, including updating lab test results, which moves valid donations into the main blood stock.
-   **Admin**: Has superuser privileges and can access all data. They are responsible for managing users, blood banks, and triggering system-wide processes like batch matching.

---

## 3. Authentication

Authentication is handled via JSON Web Tokens (JWT). All protected endpoints require an `Authorization` header with a bearer token.

**Header Format**: `Authorization: Bearer <access_token>`

### User Login

-   **Endpoint**: `/api/login/`
-   **Method**: `POST`
-   **Description**: Authenticates a user and returns access and refresh tokens.

-   **Request Body**:
    ```json
    {
        "username": "your_username",
        "password": "your_password"
    }
    ```

-   **Success Response (200 OK)**:
    ```json
    {
        "refresh": "<long_refresh_token>",
        "access": "<long_access_token>"
    }
    ```

### User Registration

-   **Endpoint**: `/api/register/`
-   **Method**: `POST`
-   **Description**: Registers a new user and their associated profile (`Donor`, `Hospital`, or `Bank Employee`). The request must contain a `user` object and one of the profile objects matching the `role`.

-   **Donor Registration Request**:
    ```json
    {
        "user": {
            "username": "new_donor",
            "password": "Password123",
            "email": "donor@example.com",
            "role": "donor",
            "city": "Cairo"
        },
        "donor_profile": {
            "national_id": "12345678901234",
            "name": "John Doe",
            "phone": "01012345678"
        }
    }
    ```

-   **Hospital Registration Request**:
    ```json
    {
        "user": {
            "username": "new_hospital",
            "password": "Password123",
            "email": "hospital@example.com",
            "role": "hospital",
            "city": "Giza"
        },
        "hospital_profile": {
            "name": "City General Hospital",
            "address": "123 Health St, Giza",
            "phone": "01098765432"
        }
    }
    ```

-   **Bank Employee Registration Request**:
    ```json
    {
        "user": {
            "username": "new_bank_employee",
            "password": "Password123",
            "email": "employee@bank.com",
            "role": "bank_employee",
            "city": "Alexandria"
        },
        "bank_employee_profile": {
            "blood_bank": 1
        }
    }
    ```

-   **Success Response (201 Created)**:
    *The response will be the created user object.*
    ```json
    {
        "id": 1,
        "username": "new_donor",
        "email": "donor@example.com",
        "role": "donor",
        "city": "Cairo"
    }
    ```

---

## 4. API Endpoints by Application

### Users App

-   **List/Create Users**
    -   **Endpoint**: `/api/users/`
    -   **Methods**: `GET`, `POST`
    -   **Permissions**: `Admin Only`
    -   **Description**: `GET` lists all users. `POST` creates a new user (admin-level creation).

### Donor App

-   **List/Create Donors**
    -   **Endpoint**: `/api/donor/`
    -   **Methods**: `GET`, `POST`
    -   **Permissions**: `Admin Only`

-   **Retrieve/Update/Delete Donor Profile**
    -   **Endpoint**: `/api/donor/profile/`
    -   **Methods**: `GET`, `PUT`, `PATCH`, `DELETE`
    -   **Permissions**: `IsDonorUser`
    -   **Description**: Manage the logged-in donor's profile.
    -   **Success Response (200 OK)**:
        ```json
        {
            "id": 1,
            "email": "donor@example.com",
            "city": "Cairo",
            "national_id": "12345678901234",
            "name": "John Doe",
            "phone": "01012345678",
            "blood_type": "A+",
            "last_donation_date": null
        }
        ```

### Hospital App

-   **List/Create Hospitals**
    -   **Endpoint**: `/api/hospital/`
    -   **Methods**: `GET`, `POST`
    -   **Permissions**: `Admin Only`

-   **Retrieve/Update/Delete Hospital Profile**
    -   **Endpoint**: `/api/hospital/profile/`
    -   **Methods**: `GET`, `PUT`, `PATCH`, `DELETE`
    -   **Permissions**: `IsHospitalUser`

### Patient App (for Hospitals)

-   **List/Create Patients**
    -   **Endpoint**: `/api/patient/`
    -   **Methods**: `GET`, `POST`
    -   **Permissions**: `IsHospitalUser`
    -   **Description**: `GET` lists all patients registered by the hospital. `POST` creates a new patient record associated with the hospital.
    -   **POST Request Body**:
        ```json
        {
            "name": "Jane Patient",
            "age": 45,
            "blood_type": "A+",
            "status": "high"
        }
        ```
    -   **Success Response (201 Created)**:
        ```json
        {
            "id": 1,
            "name": "Jane Patient",
            "age": 45,
            "blood_type": "A+",
            "status": "high",
            "hospital": 1
        }
        ```

### Blood Requests App (for Hospitals)

-   **List/Create Blood Requests**
    -   **Endpoint**: `/api/bloodrequests/do/`
    -   **Methods**: `GET`, `POST`
    -   **Permissions**: `IsHospitalUser`
    -   **Description**: `GET` lists all blood requests from the hospital. `POST` creates a new request. The `patient` ID is required to infer blood type and priority.
    -   **POST Request Body**:
        ```json
        {
            "patient": 1, 
            "quantity": 2
        }
        ```
    -   **Success Response (201 Created)**:
        ```json
        {
            "id": 1,
            "quantity": 2,
            "blood_type": "A+",
            "priority": "high",
            "status": "pending",
            "quantity_allocated": 0
        }
        ```

### Donation App

-   **Create Donation Record**
    -   **Endpoint**: `/api/donation/create/`
    -   **Method**: `POST`
    -   **Permissions**: `IsDonorUser`
    -   **Description**: Allows a donor to create a record of their donation.
    -   **POST Request Body**:
        ```json
        {
            "donor": 1,
            "bank": 2,
            "blood_type": "O-",
            "quantity": 1
        }
        ```

-   **List Donations (for Bank Employees)**
    -   **Endpoint**: `/api/donation/list/`
    -   **Method**: `GET`
    -   **Permissions**: `IsBankEmployee`
    -   **Description**: Lists all donations at the employee's blood bank that are pending a lab test.

-   **Update Lab Test Results**
    -   **Endpoint**: `/api/donation/test/<pk>/`
    -   **Method**: `PATCH`
    -   **Permissions**: `IsBankEmployee`
    -   **Description**: Marks a donation's lab test as complete. This is a trigger-only endpoint; the request body is empty. The backend logic evaluates the donation and creates a `Stock` record if valid.

### Matcher System App

-   **Trigger Batch Matching**
    -   **Endpoint**: `/api/bloodrequests/batch/`
    -   **Method**: `GET`
    -   **Permissions**: `Admin Only`
    -   **Description**: Manually triggers the batch matching process to fulfill pending blood requests with available stock.

-   **List Matches**
    -   **Endpoint**: `/api/matchersystem/`
    -   **Method**: `GET`
    -   **Permissions**: `Admin Only`
    -   **Description**: Lists all historical matches made by the system.
    -   **Success Response (200 OK)**:
        ```json
        [
            {
                "id": 1,
                "quantity_allocated": 1,
                "stock_info": {
                    "id": 10,
                    "blood_type": "A+",
                    "city": "Cairo",
                    "status": "available"
                },
                "request_info": {
                    "id": 5,
                    "blood_type": "A+",
                    "quantity": 2,
                    "priority": "high",
                    "city": "Cairo",
                    "hospital": "City General Hospital",
                    "patient": "Jane Patient"
                }
            }
        ]
        ```

---

## 5. Application Lifecycles

### A. Donation Lifecycle

1.  **Registration**: A user registers with the `donor` role.
2.  **Donation Event**: The donor donates blood. A `Donation` record is created (`POST /api/donation/create/`).
3.  **Lab Testing**: A `bank_employee` logs in and views pending donations (`GET /api/donation/list/`).
4.  **Update Status**: The employee updates the donation's lab results (`PATCH /api/donation/test/<pk>/`).
5.  **Stock Creation**: If the donation is valid, the system automatically creates a `Stock` record.
6.  **Notification**: The donor is notified of the result.

### B. Blood Request Lifecycle

1.  **Registration**: A user registers with the `hospital` role.
2.  **Patient Creation**: The hospital registers a patient (`POST /api/patient/`).
3.  **Request Creation**: The hospital submits a blood request (`POST /api/bloodrequests/do/`).
4.  **Matching**: The backend `Matcher` system finds available `Stock` (can be triggered by `GET /api/bloodrequests/batch/`).
5.  **Fulfillment**: The request status is updated. The hospital can monitor status via `GET /api/bloodrequests/`.

## 1. Introduction

This document provides a comprehensive overview of the Cyclic Blood Donation System's backend, including user roles, authentication, API endpoints, and application workflows. It is intended for frontend developers to understand how to interact with the API.

---

## 2. User Roles & Permissions

The system defines three primary user roles, each with specific permissions:

-   **Donor**: Can register, manage their profile, and view their donation history.
-   **Hospital**: Can register, manage their profile, register patients, and create blood requests for those patients.
-   **Bank Employee**: An employee of a blood bank. They can list all donations at their assigned bank and update the lab test results of donations.

**Frontend Note**: The UI should dynamically show/hide features based on the logged-in user's role, which is available in the user object after login.

---

## 3. Authentication & User Management

Authentication is handled via JWT. All protected endpoints require an `Authorization: Bearer <access_token>` header.

-   **Register User**: `POST /api/register/`
    -   **Permissions**: Public
    -   **Description**: Registers a new user and their associated profile (Donor, Hospital, or Bank Employee). The `role` field in the user object determines which profile to create.

-   **Login**: `POST /api/login/`
    -   **Permissions**: Public
    -   **Description**: Authenticates a user and returns `access` and `refresh` tokens.

-   **Refresh Token**: `POST /api/login/refresh/`
    -   **Permissions**: Public
    -   **Description**: Obtains a new `access` token using a valid `refresh` token.

-   **Verify Token**: `POST /api/login/verify/`
    -   **Permissions**: Public
    -   **Description**: Checks if an `access` token is valid.

-   **List/Manage Users**: `GET, POST, PUT, PATCH, DELETE /api/users/` and `/api/users/<pk>/`
    -   **Permissions**: Admin Only
    -   **Description**: Standard Django Rest Framework ViewSet for user management.

---

## 4. API Endpoints by Application

### Donor (`/api/donor/`)

-   **Get My Profile**: `GET /api/donor/me/`
    -   **Permissions**: `IsDonorUser`
    -   **Description**: Retrieves the profile details for the currently logged-in donor.

-   **Manage Donors**: `GET, PUT, PATCH, DELETE /api/donor/<pk>/`
    -   **Permissions**: Admin Only
    -   **Description**: Allows administrators to manage donor records.

### Hospital (`/api/hospital/`)

-   **Get My Profile**: `GET /api/hospital/me/`
    -   **Permissions**: `IsHospitalUser`
    -   **Description**: Retrieves the profile details for the currently logged-in hospital.

-   **Manage Hospitals**: `GET, PUT, PATCH, DELETE /api/hospital/<pk>/`
    -   **Permissions**: Admin Only
    -   **Description**: Allows administrators to manage hospital records.

### Patient (`/api/patient/`)

-   **List/Create Patients**: `GET, POST /api/patient/`
    -   **Permissions**: `IsHospitalUser`
    -   **Description**: `GET` lists all patients associated with the hospital. `POST` creates a new patient for the hospital.

-   **Manage Patient**: `GET, PUT, PATCH, DELETE /api/patient/<pk>/`
    -   **Permissions**: `IsHospitalUser` (for their own patients)
    -   **Description**: Allows a hospital to view or update a specific patient's details.

### Blood Requests (`/api/bloodrequests/`)

-   **List Blood Requests**: `GET /api/bloodrequests/`
    -   **Permissions**: `IsHospitalUser`
    -   **Description**: Lists all blood requests made by the logged-in hospital.

-   **Create Blood Request**: `POST /api/bloodrequests/do/`
    -   **Permissions**: `IsHospitalUser`
    -   **Description**: Creates a new blood request for one of the hospital's patients.

-   **Trigger Batch Matching**: `GET /api/bloodrequests/batch/`
    -   **Permissions**: Admin Only
    -   **Description**: Manually triggers the matching process between blood requests and available stock. **Frontend Note**: This is an administrative action and should not be exposed to regular users.

### Donation (`/api/donation/`)

-   **Create Donation**: `POST /api/donation/create/`
    -   **Permissions**: Admin/Staff (or potentially Bank Employee)
    -   **Description**: Creates a new donation record. **Frontend Note**: The current workflow implies this is a backend process, not a direct user action.

-   **List Donations in Bank**: `GET /api/donation/list/`
    -   **Permissions**: `IsBankEmployee`
    -   **Description**: Lists all donations associated with the logged-in employee's blood bank.

-   **Update Lab Test**: `PATCH /api/donation/test/<pk>/`
    -   **Permissions**: `IsBankEmployee`
    -   **Description**: Marks a donation's lab test as complete. This is a critical step that can trigger the creation of a `Stock` record.

### Blood Bank (`/api/bloodbank/`)

-   **List/Create Blood Banks**: `GET, POST /api/bloodbank/`
    -   **Permissions**: Admin Only
    -   **Description**: Allows administrators to manage blood bank records.

### Blood Stock (`/api/stock/`)

-   **Get Stock Summary**: `GET /api/stock/summary/`
    -   **Permissions**: Authenticated Users
    -   **Description**: Provides a summary of available blood stock, grouped by blood type.

-   **Get Stock Summary by City**: `GET /api/stock/summary/city/`
    -   **Permissions**: Authenticated Users
    -   **Description**: Provides a summary of available blood stock, grouped by city and blood type.

### Matcher System (`/api/matcher/`)

-   **List Matches**: `GET /api/matcher/`
    -   **Permissions**: Admin Only
    -   **Description**: Lists all historical matches made between blood requests and stock.

---

## 5. Application Lifecycles

### A. Donation Lifecycle

1.  **Registration**: A user registers with the `donor` role.
2.  **Donation Event**: The donor donates blood. A `Donation` record is created (`POST /api/donation/create/`).
3.  **Lab Testing**: A `bank_employee` logs in and views pending donations (`GET /api/donation/list/`).
4.  **Update Status**: The employee updates the donation's lab results (`PATCH /api/donation/test/<pk>/`).
5.  **Stock Creation**: If the donation is valid, the system automatically creates a `Stock` record.
6.  **Notification**: The donor is notified of the result.

### B. Blood Request Lifecycle

1.  **Registration**: A user registers with the `hospital` role.
2.  **Patient Creation**: The hospital registers a patient (`POST /api/patient/`).
3.  **Request Creation**: The hospital submits a blood request (`POST /api/bloodrequests/do/`).
4.  **Matching**: The backend `Matcher` system finds available `Stock` (can be triggered by `GET /api/bloodrequests/batch/`).
5.  **Fulfillment**: The request status is updated. The hospital can monitor status via `GET /api/bloodrequests/`.
