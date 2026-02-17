"""Seed default roles and permissions into the database."""

import asyncio

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.auth.models import Permission, Role
from app.core.database import async_session

# All permissions in the system
PERMISSIONS = [
    {"name": "create_article", "resource": "article", "action": "create"},
    {"name": "read_article", "resource": "article", "action": "read"},
    {"name": "update_article", "resource": "article", "action": "update"},
    {"name": "delete_article", "resource": "article", "action": "delete"},
    {"name": "read_user", "resource": "user", "action": "read"},
    {"name": "update_user", "resource": "user", "action": "update"},
    {"name": "delete_user", "resource": "user", "action": "delete"},
]

# Roles and which permissions they get
ROLES = {
    "viewer": ["read_article", "read_user"],
    "editor": ["read_article", "read_user", "create_article", "update_article"],
    "admin": [p["name"] for p in PERMISSIONS],  # all permissions
}


async def seed():
    async with async_session() as session:
        # Create permissions (skip if they already exist)
        for perm_data in PERMISSIONS:
            exists = await session.execute(
                select(Permission).where(Permission.name == perm_data["name"])
            )
            if not exists.scalar_one_or_none():
                session.add(Permission(**perm_data))

        await session.commit()

        # Load all permissions into a lookup dict
        result = await session.execute(select(Permission))
        all_perms = {p.name: p for p in result.scalars().all()}

        # Create roles and assign permissions
        for role_name, perm_names in ROLES.items():
            existing = await session.execute(
                select(Role).options(selectinload(Role.permissions)).where(Role.name == role_name)
            )
            role = existing.scalar_one_or_none()

            if not role:
                role = Role(name=role_name, permissions=[all_perms[name] for name in perm_names])
                session.add(role)
            else:
                role.permissions = [all_perms[name] for name in perm_names]

        await session.commit()
        print("Seeded roles and permissions.")


if __name__ == "__main__":
    asyncio.run(seed())
