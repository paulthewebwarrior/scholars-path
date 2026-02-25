## Context

The platform currently lacks any user authentication or profile system. The dashboard is accessible to everyone without identification. To enable personalized productivity tracking and recommendations, we need to establish user identity, secure authentication, and persistent user profiles.

Current state:
- Frontend: Angular app with public access, no auth guards
- Backend: FastAPI app with no user models or auth endpoints
- Database: Only contains productivity dataset, no user data
- No session/token management in place

## Goals / Non-Goals

**Goals:**
- Enable secure user registration with email validation
- Implement session-based authentication (or JWT tokens)
- Store encrypted user credentials securely
- Provide user profile management (name, course, year level, career goal)
- Protect dashboard routes with authentication guards
- Set foundation for personalized features in future iterations

**Non-Goals:**
- Social login (Google, GitHub, etc.) - phase 2
- Advanced permissions/roles system - phase 2
- Email verification/password recovery - phase 2
- Multi-factor authentication - future
- Data export/migration tools - future

## Decisions

### 1. Authentication Method
**Decision:** Use JWT (JSON Web Tokens) with refresh tokens for stateless authentication

**Rationale:** JWT allows easy scaling across services, enables both web and mobile clients, and is simpler to implement than session-based auth with databases. Refresh tokens provide security without frequent re-authentication.

**Alternatives considered:**
- Session-based auth with server-side storage: More secure but less scalable
- Basic auth with each request: Simple but exposes credentials
- OAuth 2.0: Overkill for phase 1

### 2. Password Storage
**Decision:** Hash passwords with bcrypt (salt + hash), never store plaintext

**Rationale:** Industry standard, includes salt generation, resistant to rainbow tables and brute force

### 3. Database Schema
**Decision:** Add users table with: id, email (unique), hashed_password, name, course, year_level, career_goal, created_at, updated_at

**Rationale:** Normalizes user data, allows flexible profile updates, maintains audit trail

### 4. API Structure
**Decision:** REST endpoints under `/api/auth/` and `/api/profile/`

Endpoints:
- POST `/api/auth/register` - Create account
- POST `/api/auth/login` - Generate tokens
- POST `/api/auth/refresh` - Get new access token
- GET `/api/profile/me` - Get current user profile
- PUT `/api/profile/me` - Update profile
- POST `/api/auth/logout` - Invalidate tokens (optional with JWT)

### 5. Frontend Auth Guards
**Decision:** Implement route guards in Angular to prevent unauthenticated access to dashboard

**Rationale:** Improves UX by preventing page loads that require auth, works with API-level auth

### 6. Token Storage
**Decision:** Store access token in memory, refresh token in secure HTTP-only cookie

**Rationale:** Access token in memory prevents XSS token theft. HTTP-only cookie prevents access via JavaScript malicious code. CSRF protection via SameSite flag.

## Risks / Trade-offs

| Risk | Mitigation |
|------|-----------|
| Token expiration breaks user mid-session | Automatic refresh handling in HTTP interceptors |
| Password breach if database compromised | Use bcrypt with appropriate work factor; regular security audits |
| CSRF attacks on login/logout | SameSite cookies, CSRF tokens for state-changing requests |
| Scaling auth service | JWT's stateless nature allows horizontal scaling |
| User lockout if cookies lost | Clear documentation for clearing cookies; implement "remember me" later |

## Migration Plan

**Phase 1 - Backend Setup:**
1. Create users table in database
2. Implement auth endpoints (register, login, profile CRUD)
3. Add JWT generation/validation middleware
4. Create password hashing utilities

**Phase 2 - Frontend Setup:**
1. Build register and login pages
2. Implement HTTP interceptor for token injection
3. Add auth route guards to dashboard
4. Add logout button and user menu

**Phase 3 - Integration:**
1. Connect frontend forms to backend endpoints
2. Test full auth flow
3. Deploy with database migrations

**Rollback Strategy:**
- Auth is additive; removing it requires deleting user data and removing route guards
- API versioning allows maintaining legacy endpoints if needed

## Open Questions

- Should we implement "remember me" / auto-login on page refresh?
- What's the appropriate JWT token expiration time (15m access, 7d refresh)?
- Should user email be changeable post-registration?
- Do we need a "delete account" feature in phase 1 or defer to phase 2?
