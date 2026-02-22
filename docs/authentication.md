# Authentication

## Traditional sessions

- When you log in, the server creates a session record (in memory/Redis/DB) that says who you are.
- The server puts a session ID cookie in the HTTP response header.

```
Set-Cookie: session_id=abc123; HttpOnly; Secure; Path=/
```

- Then on every request, the browser sends that cookie back.

```
Cookie: session_id=abc123 # The cookie doesn’t store user info.
```

- The server looks up the session ID in the cookie, looks up the session record, and identifies the user.

```
# example of a session record
{
  "id": "abc123",
  "user_id": 42,
  "expires": "2026-02-22T12:00:00Z"
}
```

Pros

- Easy to revoke or invalidate sessions instantly.
- Server fully controls authentication state.

Cons

- The server must store state for every user.
- Multiple servers need a shared session store, which adds complexity.
- Cookies don’t fit well for mobile apps or third-party clients.

### How caching fits into session-based auth

1. In-memory cache (fastest, but only single server)

Example: server keeps sessions in RAM.

- super fast
- but doesn’t work if you have multiple servers (each would have different RAM)

2. Distributed cache (most common)

Example: Redis.

- all servers share the same session store
- lookup is very fast (microseconds–milliseconds)
- scales across many servers
- can evict expired sessions automatically

This is what most scalable systems use.

3. Database (slowest, last resort)
   Systems can store sessions in a database, but it’s slow compared to Redis, so it’s usually avoided for each-request lookups.

## JWT tokens (stateless approach)

A JWT (JSON Web Token) is a small, signed package of data that the server gives the client after login.
It contains user info inside the token itself — no session lookup required.

With a JWT, the server authenticates the user by simply:

1. Receiving the token
2. Verifying the signature using its secret/public key
3. Reading the claims inside (user_id, roles, expiry, etc.)

### How JWT authentication works

1. Client sends credentials

```
POST /login
```

2. Server creates a JWT

It encodes:
• user ID
• expiry
• maybe permissions/roles

```
{
  "user_id": 42,
  "role": "admin",
  "exp": 1730000000
}
```

The server signs it with a secret key so the client can’t modify it.

3. Server gives JWT to the client

Usually in the response body or a header.
(Optionally in an HttpOnly cookie.)

4. Client sends the JWT on every request

Typically in:

```
Authorization: Bearer <token>
```

5. Server verifies the JWT signature
   • If valid → trust the data inside
   • No DB lookup needed
   • If expired or invalid → deny access

Advantages

- Stateless → server doesn’t store sessions - no cache, no lookup
- Scales easily across many servers
- Works great for:
- mobile apps
- SPAs (React/Vue)
- third-party APIs
- microservices

## Two-token system: Access + Refresh

This is the trade-off that gives you the **best of both worlds**: stateless speed for normal requests (access token, no DB lookup), with the ability to revoke sessions (refresh token, stored in DB).

|               | Access Token                                | Refresh Token                           |
| ------------- | ------------------------------------------- | --------------------------------------- |
| **Format**    | JWT (signed, stateless)                     | JWT (stored in DB)                      |
| **Lifetime**  | ~30 minutes                                 | ~7 days                                 |
| **Sent with** | Every API request (`Authorization: Bearer`) | Only to `/auth/refresh`                 |
| **Revocable** | No (expires naturally)                      | Yes (marked as revoked in DB on logout) |

**Why two tokens?** A single long-lived token is dangerous if stolen (can't revoke a JWT). A single short-lived token forces constant re-login. The pair gives you short exposure + long sessions + revocability.

The flow:

```
1. Login → get access_token (30min) + refresh_token (7 days)
2. Use access_token for API calls
3. Access token expires → send refresh_token to POST /auth/refresh
4. Server checks refresh token in DB (not revoked? not expired?) → issues new access_token
5. Logout → server marks refresh_token as revoked in DB
```

## Library choices

- **PyJWT** over python-jose — python-jose is abandoned (~3 years unmaintained). FastAPI docs switched to PyJWT in 2024.
- **pwdlib[argon2]** over passlib — passlib is unmaintained and breaks on Python 3.13+. pwdlib uses Argon2id (winner of the Password Hashing Competition).

## Auth flow in this project

```
POST /auth/register  → hash password, save user, assign default "viewer" role, return tokens
POST /auth/login     → verify password → return { access_token, refresh_token, user }
POST /auth/refresh   → verify refresh token → return new access_token
GET  /users/me       → decode JWT → return user profile + roles + permissions
POST /auth/logout    → revoke refresh token in DB
```
