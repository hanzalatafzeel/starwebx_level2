# Profile Edit & Logo Upload Feature - Implementation Summary

## Features Added

### 1. **Edit Profile Page** (`EditProfile.vue`)
- Located at: `/profile/edit`
- Users can edit:
  - Full Name
  - Company Name
  - Email
  - Password (optional, leave blank to keep current)
  - Company Logo (optional upload)
- Features:
  - Logo preview before saving
  - Display current logo if already uploaded
  - Dark theme support
  - Form validation
  - Success/error messages
  - Auto-redirect to dashboard on success

### 2. **Enhanced Signup Form** (`Signup.vue`)
- Added optional company logo upload field
- Logo preview display
- FormData support for file uploads
- Direct API integration for multipart form data
- Accepted formats: PNG, JPG, JPEG, GIF

### 3. **Updated Navbar** (`Navbar.vue`)
- Added "Profile" button for authenticated users
- Links to `/profile/edit` page
- Displayed between Dashboard and Logout buttons

### 4. **API Service Updates** (`api.js`)
- Added `updateProfile()` method
- Supports multipart/form-data for file uploads
- Integrates with backend `/auth/profile` endpoint

### 5. **Router Configuration** (`router/index.js`)
- Added new route: `/profile/edit`
- Protected route (requires authentication)
- Imports EditProfile component

## Backend Integration

All features align with the backend controllers:

### **Signup Endpoint** (`/auth/signup`)
- Accepts:
  - email (required)
  - password (required)
  - full_name (optional)
  - company_name (optional)
  - logo file (optional, multipart/form-data)
- Returns: user object with company_logo path

### **Profile Update Endpoint** (`/auth/profile`)
- PUT request to `/auth/profile`
- Accepts FormData with:
  - full_name
  - company_name
  - email
  - password (optional)
  - logo file (optional)
- Handles logo file validation and storage
- Deletes old logo before saving new one
- Returns: updated user object

## File Structure

```
frontend/src/
├── components/
│   ├── Profile/
│   │   └── EditProfile.vue (NEW)
│   ├── Auth/
│   │   ├── Signup.vue (UPDATED)
│   │   └── Login.vue
│   ├── Layout/
│   │   └── Navbar.vue (UPDATED)
│   └── ...
├── services/
│   └── api.js (UPDATED)
├── router/
│   └── index.js (UPDATED)
└── ...
```

## Styling Features

- Full dark theme support
- Logo upload with drag-and-drop style UI
- Responsive design (Bootstrap grid)
- Logo preview images with proper sizing
- Disabled state handling for form submit button
- Error and success message alerts

## Logo Upload Specifications

- **Accepted formats**: PNG, JPG, JPEG, GIF
- **Max size**: 5MB (enforced by form UI)
- **Server validation**: Handled by backend `allowed_file()` function
- **Storage**: `uploads/logos/user_{user_id}_logo.{ext}`
- **Deletion**: Old logo automatically deleted when new one uploaded

## Usage

### Edit Profile:
1. User clicks "Profile" button in navbar
2. Fills form with updated information
3. Optionally uploads new company logo
4. Clicks "Save Changes"
5. Profile updates and redirects to dashboard

### Signup with Logo:
1. User fills signup form
2. Optionally selects company logo file
3. Logo preview appears
4. Clicks "Sign Up"
5. Account created with logo if provided

## Error Handling

- Invalid file types are rejected with error message
- Email uniqueness validation
- Password minimum length (6 characters)
- Network errors display user-friendly messages
- Form submission is disabled while loading

## Security

- JWT token required for profile updates
- Backend validates user ownership
- File extension validation on both frontend and backend
- Secure filename handling via werkzeug
