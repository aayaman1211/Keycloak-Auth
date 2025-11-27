Keycloak Authentication Assignment

⸻

1. Overview

This project demonstrates a complete authentication flow using:

• Keycloak – Identity Provider (OpenID Connect)
• Next.js (React + TypeScript) – Frontend
• FastAPI (Python) – Backend API
• Keycloak Roles – Authorization (user, admin)

The system supports:

• Login using Keycloak
• Displaying logged-in user and roles
• Secure backend API calls using access tokens
• Role-based protection with admin-only endpoints

⸻

2. Phase 1 – Keycloak Setup & Initial Configuration

2.1 Running Keycloak

Inside the keycloak/ folder:

docker compose up

This starts Keycloak at:
http://localhost:8080

Admin credentials:
• Username: admin
• Password: admin

Deliverables:
• Screenshot of Docker terminal
• Screenshot of Keycloak login page

⸻

2.2 Creating Realm, Client, and User

Realm

• Name: demo-realm

Client

• Client ID: demo-frontend
• Type: OpenID Connect
• Access Type: Public
• Root URL: http://localhost:3000
• Valid redirect URIs: http://localhost:3000/*
• Web Origins: http://localhost:3000

User

• Username: demo-user
• Set a password (non-temporary)

Deliverables:
• Realm overview screenshot
• Client config screenshot
• User details screenshot

⸻

3. Phase 2 – Roles & Client Setup

3.1 Roles Created

• user
• admin

3.2 Role Assignment

• demo-user → user

3.3 Client Configuration

• Redirect URIs and origins correctly set
• Access Type = Public

Deliverables:
• Screenshot of role list
• Screenshot of demo-user role mappings
• Screenshot of redirect URIs

⸻

4. Phase 3 – Frontend + Backend Integration

4.1 Frontend (Next.js)

Folder: frontend/

Important files:

• src/keycloak.ts
Contains Keycloak client config (realm, clientId, URL).

• src/components/KeycloakProvider.tsx
Automatically logs the user in and maintains session.

• src/app/page.tsx
Shows username, roles, and provides buttons to test backend endpoints.

Run frontend:

npm install
npm run dev

Open: http://localhost:3000

⸻

4.2 Backend (FastAPI)

Folder: backend/

Install dependencies:

python -m venv venv
source venv/bin/activate
pip install fastapi uvicorn requests python-dotenv “python-jose[cryptography]”

Environment variables (backend/.env):

KEYCLOAK_URL=http://localhost:8080
REALM=demo-realm

Backend Features:

• Validates access token via Keycloak /userinfo
• Reads roles from JWT payload
• Routes:
– /user-info → returns username + roles
– /admin-only → requires admin role

Run backend:

python -m uvicorn main:app –reload –port 8000

Open: http://127.0.0.1:8000

Deliverables:
• Screenshot of FastAPI running
• Screenshot of frontend showing logged in user
• Screenshot of /user-info response
• Screenshot of 403 error on /admin-only for normal user

⸻

5. Phase 4 – Integration Plan (How It All Connects)

5.1 Authentication Flow (Step-by-Step)
	1.	User opens frontend (http://localhost:3000).
	2.	KeycloakProvider checks if user is logged in.
	3.	If not logged in → redirect to Keycloak login.
	4.	User logs in using Keycloak (demo-user).
	5.	Keycloak redirects back to frontend with an access token.
	6.	Frontend stores and manages this token via keycloak-js.
	7.	Frontend calls backend endpoints with the header:
Authorization: Bearer <access_token>
	8.	Backend verifies the token using Keycloak /userinfo.
	9.	Backend extracts user roles from JWT.
	10.	Backend returns response or 403 (Forbidden) if user lacks roles.

⸻

5.2 Component Responsibilities

Frontend (Next.js)

• UI
• Login redirection
• Keeps token refreshed
• Sends token to backend
• Shows user info and roles

Backend (FastAPI)

• Validates tokens
• Enforces role-based authorization
• Provides protected endpoints

Keycloak

• Manages users
• Issues access tokens
• Stores roles and groups
• Handles login/logout



