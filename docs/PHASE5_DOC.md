PHASE 5 – Advanced Topics & Demo Enhancements

1. Overview

Phase 5 explores advanced authentication topics using Keycloak:

• Logout behavior
• Refresh tokens & automatic token renewal
• Multi-tenant architecture
• User migration approaches
• A small working demo of an advanced feature

All changes are implemented on top of the working Phase 1–4 app.

⸻

2. Logout Functionality

Frontend Behavior

The “Logout” button calls:

keycloak.logout()

This redirects the user to Keycloak’s logout endpoint.
Keycloak then:

• Invalidates the user’s session
• Invalidates refresh tokens
• Removes active access tokens
• Redirects back to the frontend

After logout, any attempt to re-enter the app triggers a fresh login.

Why this matters

Logout must terminate the session at Keycloak, not just wipe tokens locally.

⸻

3. Refresh Tokens / Session Renewal

Concept

Keycloak issues:

• Access Token → short lifetime
• Refresh Token → longer lifetime

In SPAs (React/Next.js), access tokens expire while the user is still active.
To avoid breaking the UX, tokens must be refreshed automatically.

Implementation in the app

The KeycloakProvider includes:

• Automatic token refresh every 20 seconds
• Uses keycloak.updateToken(30)
• If refresh fails → user is logged out

This ensures:

• Long-lived sessions
• No silent failures
• Smooth workflow for users

This counts as the “small demo” required for Phase 5.

⸻

4. Multi-Tenant Setup (Concept)

Keycloak supports multiple approaches to multi-tenancy.

Model 1 — Multi-Realm (strong isolation)

Each tenant has:

• Its own realm
• Its own users, roles, clients
• Fully isolated security boundaries

Best for: SaaS platforms requiring hard isolation.

Model 2 — Single Realm + Groups / Attributes

Each user receives a tenant identifier inside their token.

Example:

realm_access.roles → [“user”]
attributes.tenant → “tenantA”

Backend enforces:

• User may only access resources belonging to their tenant
• Tenant-based routing or database filters

Best for: Apps with many tenants but shared infra.

Model 3 — Single Realm + Client-per-Tenant

Each tenant has their own client.
User logs into the client belonging to their tenant.

⸻

5. User Migration Approaches

Case 1 — Import users into Keycloak

Steps:
	1.	Export users from old system
	2.	Map attributes → username, email, roles
	3.	Import into Keycloak (Admin console or Admin REST API)
	4.	Assign realm roles

Case 2 — User Federation

Keycloak connects directly to:

• LDAP
• Active Directory
• Custom DB

Users stay in original system; Keycloak acts as auth proxy.

Case 3 — Identity Brokering

Keycloak delegates login to an external provider:

• OAuth
• Google
• Auth0
• SAML

Runs smooth transitions without migrating passwords.

⸻

6. Role-Based Authorization Review

The backend enforces:

• Token must be valid (\userinfo)
• User must have required role

/user-info → requires valid token
/admin-only → requires admin role

This demonstrates:

• Authentication (identity verification)
• Authorization (permissions)

⸻

7. Final Summary

Phase 5 introduces advanced capabilities:

• Fully implemented logout
• Auto-refresh tokens (real demo)
• Understanding of multi-tenancy
• Strategies to migrate existing users
• Token lifecycle & security considerations
• Clear separation between authentication and authorization
