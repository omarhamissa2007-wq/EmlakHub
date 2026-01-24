# EmlakHub Project Index

This document outlines the project structure and key components of the EmlakHub application.

## Directory Structure

### Root

- **`app.py`**: The entry point of the Streamlit application. Handles initial routing (Login/Home).
- **`utils.py`**: Helper functions for the project (e.g., path management).
- **`.gitignore`**: Specifies files to be ignored by Git (e.g., `__pycache__`).

### Assets (`assets/`)

Contains resources for the application.

- **`documents/`**: PDF contracts (e.g., `ownership_contract.pdf`).
- **`images/`**: Property images.

### Data (`data/`)

- **`properties_data.py`**: Contains the dictionary database of properties.
- **`uploads/`**: Directory where user-uploaded files (contracts, property images) are stored.

### Notifications (`notifications/`)

Module for sending external notifications.

- **`__init__.py`**: Exports `send_message` function.
- **`email_sender.py`**: Logic for sending emails via SMTP.
- **`whatsapp_sender.py`**: Logic for sending WhatsApp messages via `pywhatkit`.

### Pages (`pages/`)

Streamlit pages for the multi-page application.

- **`home.py`**: Main dashboard displaying property gallery.
- **`property_details.py`**: Shows details for a selected property.
- **`contract.py`**: Handles contract generation and signing.
- **`add_property.py`**: Admin form to add new properties.
- **`login.py`/`signup.py`**: Authentication pages.
- **`about.py`**: Information page.

## Key Workflows

1. **Authentication**: User logs in -> Session state updated -> Redirect to Home.
2. **Browsing**: Home page lists properties from `properties_data.py`. User clicks "View Details" -> `property_details.py`.
3. **contracting**: User selects "View Contract" -> `contract.py`. Fills form -> System generates contract -> Sends email/whatsapp via `notifications` module.
4. **Admin**: Admin uses `add_property.py` to append new properties to `properties_data.py` and upload images to `data/uploads`.
