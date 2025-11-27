Keycloak Authentication Demo

A complete authentication & authorization demo using:

• Keycloak (OpenID Connect Identity Provider)
• Next.js (Frontend)
• FastAPI (Backend API)
• Role-based authorization (user and admin)
• Automatic token refresh
• Clean minimal UI

This project satisfies Phase 1–5 of the Keycloak assignment.

⸻

1. Project Structure

keycloak-auth-assignment/
│
├── keycloak/        → Docker Compose Keycloak instance
├── backend/         → FastAPI backend with JWT validation
└── frontend/        → Next.js authentication frontend

⸻

2. How to Run The Entire Project

2.1 Start Keycloak

cd keycloak
docker compose up

Access Keycloak:
http://localhost:8080

Admin credentials:
username: admin
password: admin

⸻

3. Keycloak Configuration

Realm

Name: demo-realm

Client

Client ID: demo-frontend
Client type: OpenID Connect
Access Type: Public
Root URL: http://localhost:3000
Valid redirect URIs: http://localhost:3000/*
Web origins: http://localhost:3000

User

Username: demo-user
Password: (set manually, not temporary)

Roles

user
admin

Assign user role to demo-user.

⸻

4. Backend Setup (FastAPI)

cd backend
python3 -m venv venv
source venv/bin/activate

Install dependencies:

pip install fastapi uvicorn requests python-dotenv “python-jose[cryptography]”

Environment variables file (backend/.env):

KEYCLOAK_URL=http://localhost:8080
REALM=demo-realm

Run backend:

python -m uvicorn main:app –reload –port 8000

Backend runs at:
http://127.0.0.1:8000

⸻

5. Backend Endpoints

• GET /user-info
Requires valid token
Returns username + roles

• GET /admin-only
Requires admin role
Returns 403 for non-admin users

⸻

6. Frontend Setup (Next.js)

cd frontend
npm install
npm run dev

Frontend runs at:
http://localhost:3000

⸻

7. Frontend Functionality

The UI shows:

• Logged-in username
• User roles
• Buttons to call /user-info and /admin-only
• Pretty black-and-red minimalistic theme
• Logout button

The app uses KeycloakProvider to:

• Require login
• Maintain session
• Auto-refresh tokens every 20 seconds

This implements a real refresh token flow (Phase 5 requirement).

⸻

8. Authentication Flow (Full Integration Plan)
	1.	User opens http://localhost:3000
	2.	KeycloakProvider checks login
	3.	If no token → redirects to Keycloak login
	4.	User logs in (demo-user)
	5.	Keycloak redirects back to frontend
	6.	Frontend stores JWT and refresh token
	7.	Frontend sends requests to backend with header:
Authorization: Bearer <access_token>
	8.	Backend validates token using Keycloak /userinfo
	9.	Backend decodes roles from JWT
	10.	Backend enforces role-based access
	11.	UI displays results accordingly

⸻

9. Phase 4 Deliverables

• Realm, User, Roles, Client — all configured
• Frontend integrated
• Backend integrated
• End-to-end login and authorization flow
• Documentation provided
• Screenshot instructions satisfied

⸻

10. Phase 5 Deliverables (Advanced Topics)

• Full logout support
• Auto refresh token flow implemented
• Explanation of multi-tenant options
• User migration strategies described
• Token lifecycle analysis
• Advanced integration documentation

⸻

11. How to Create a GitHub Repo for This Project
	1.	Go to GitHub → New Repository
	2.	Name: keycloak-auth-assignment
	3.	Do NOT add README / .gitignore / license
	4.	In terminal:

cd keycloak-auth-assignment
git init
git add .
git commit -m “Initial commit: Keycloak Authentication Demo”
git branch -M main
git remote add origin https://github.com/your-username/keycloak-auth-assignment.git
git push -u origin main

⸻

12. Final Notes

This project includes:

• Fully working login
• Role enforcement
• Proper backend API security
• Clean UI
• Complete documentation for all phases