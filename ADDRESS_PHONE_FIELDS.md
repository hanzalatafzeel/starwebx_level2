# User Address & Phone Fields - Implementation Summary

## Changes Made

### 1. **Backend Model Updates** (`models.py`)

Added two optional fields to the `User` model:
```python
address = db.Column(db.Text)  # optional address field
phone = db.Column(db.String(20))  # optional phone field
```

Updated `to_dict()` method to include new fields:
```python
'company_logo': self.company_logo,
'address': self.address,
'phone': self.phone
```

### 2. **Backend Controllers Updates** (`controllers.py`)

#### Signup Endpoint (`/auth/signup`)
- Added extraction of `address` and `phone` from both multipart form data and JSON
- Updated User creation to include these fields
- Both fields are optional

#### Profile Edit Endpoint (`/auth/profile`)
- Added extraction of `address` and `phone` from both multipart form data and JSON
- Added update logic for both fields
- Fields can be updated independently

### 3. **Frontend - Edit Profile Component** (`EditProfile.vue`)

Added form fields:
- **Address** - Text area for multi-line address (optional)
- **Phone** - Text input for phone number (optional)

Updated:
- Form data object to include `address` and `phone`
- FormData append to send these fields to backend
- `onMounted()` hook to load these fields from user data

### 4. **Frontend - Signup Form** (`Signup.vue`)

Added form fields:
- **Address** - Text area for address input (optional)
- **Phone** - Text input for phone number (optional)

Updated:
- Form data refs for `address` and `phone`
- FormData append to include these fields
- Return statement to expose these refs

## Database Schema Update

If you already have users in the database, run a migration:

```sql
ALTER TABLE users ADD COLUMN address TEXT;
ALTER TABLE users ADD COLUMN phone VARCHAR(20);
```

Or using Flask-Migrate:
```bash
flask db migrate -m "Add address and phone to users"
flask db upgrade
```

## API Endpoints

### Signup
**POST** `/auth/signup`

New optional fields in FormData or JSON:
```json
{
  "address": "123 Business St, City, State ZIP",
  "phone": "+1 (555) 123-4567"
}
```

### Profile Update
**PUT** `/auth/profile`

Can now update address and phone:
```json
{
  "address": "456 New St, City, State ZIP",
  "phone": "+1 (555) 987-6543"
}
```

## Frontend Forms

### Signup Form
- Full Name
- Company Name (optional)
- Address (optional) - Textarea
- Phone (optional) - Tel input
- Email (required)
- Password (required)
- Company Logo (optional) - File upload

### Edit Profile Form
- Full Name
- Company Name (optional)
- Email
- Address (optional) - Textarea
- Phone (optional) - Tel input
- Password (optional) - Leave blank to keep current
- Company Logo (optional) - File upload with preview

## User Object Response

Updated user object now includes:
```json
{
  "id": 1,
  "email": "user@example.com",
  "full_name": "John Doe",
  "company_name": "ACME Corp",
  "company_logo": "uploads/logos/user_1_logo.png",
  "address": "123 Business St, City, State ZIP",
  "phone": "+1 (555) 123-4567"
}
```

## Styling Notes

- Address field: 2-row textarea with dashed border placeholder
- Phone field: Standard tel input with placeholder format
- Both fields have `text-muted` labels and small descriptive text
- Dark theme fully supported with proper contrast
- Responsive design with Bootstrap grid system
