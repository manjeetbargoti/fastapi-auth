from app.db.models.user import User

def get_user_permissions(user:User) -> set[str]:
    permissions: set[str] = set()

    for role in user.roles:
        print(role)
        for perm in role.permissions:
            print(perm)
            permissions.add(perm.code)

    return permissions