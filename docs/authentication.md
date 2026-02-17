# Authentication

## Two-token system: Access + Refresh

| | Access Token | Refresh Token |
|---|---|---|
| **Format** | JWT (signed, stateless) | Opaque string (stored in DB) |
| **Lifetime** | ~30 minutes | ~7 days |
| **Sent with** | Every API request (`Authorization: Bearer`) | Only to `/auth/refresh` |
| **Revocable** | No (expires naturally) | Yes (deleted from DB on logout) |

**Why two tokens?** A single long-lived token is dangerous if stolen (can't revoke a JWT). A single short-lived token forces constant re-login. The pair gives you short exposure + long sessions + revocability.

## Why JWT over sessions?

- **Stateless** — any server can verify the token without shared storage (Redis, DB). Scales horizontally.
- **FastAPI native** — built-in `OAuth2PasswordBearer` support. Sessions need third-party libraries.
- **API-first** — JWTs are the standard for SPAs, mobile apps, and microservices. Sessions are for server-rendered HTML.

## Library choices

- **PyJWT** over python-jose — python-jose is abandoned (~3 years unmaintained). FastAPI docs switched to PyJWT in 2024.
- **pwdlib[argon2]** over passlib — passlib is unmaintained and breaks on Python 3.13+. pwdlib uses Argon2id (winner of the Password Hashing Competition).

## Auth flow

```
POST /auth/register  → hash password, save user, assign default "viewer" role
POST /auth/login     → verify password → return { access_token, refresh_token, user }
POST /auth/refresh   → verify refresh token → return new access_token
GET  /users/me       → decode JWT → return user profile + roles + permissions
POST /auth/logout    → revoke refresh token in DB
```

## JWT payload (minimal by design)

```json
{ "sub": "user_id", "exp": 1234567890 }
```

Identity only. No permissions in the token — they live in the database so they can be changed/revoked instantly without reissuing tokens.

## Frontend integration

- Store access token in memory, refresh token in httpOnly cookie
- On 401: silently call `/auth/refresh` for a new access token
- Use permissions from `/users/me` for UI rendering (show/hide elements)
- Never trust frontend permission checks — backend always re-validates
