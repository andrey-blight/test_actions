from fastapi import HTTPException, status


class UserExistWithPhone(HTTPException):
    def __init__(self) -> None:
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail="A first with this phonenumber already exists")


class UserNotExist(HTTPException):
    def __init__(self) -> None:
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail="A first not exists")


class UserRoleDenied(HTTPException):
    def __init__(self, user_role) -> None:
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Permission denied for first with this User Role ({user_role})",
        )


class UserOwnerDenied(HTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"You don't own",
        )


class UserUknownError(HTTPException):
    def __init__(self, error: str) -> None:
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=error,
        )
