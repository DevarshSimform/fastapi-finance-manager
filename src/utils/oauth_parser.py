from fastapi import HTTPException, status

from src.schemas.auth_schema import OAuthProvider, OAuthUser


def parse_google_userinfo(user_info: dict) -> OAuthUser:
    """
    Parse Google OAuth userinfo response into an OAuthUser schema.

    Args:
        user_info (dict): The userinfo dictionary from Google OAuth token.

    Returns:
        OAuthUser: Validated Pydantic object for DB handling.
    """
    email = user_info.get("email")
    oauth_id = user_info.get("sub")
    name = user_info.get("name", "")

    if not email or not oauth_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Google account did not return required user info",
        )

    firstname, lastname = (name.split(" ", 1) + [""])[:2]

    return OAuthUser(
        email=email,
        firstname=firstname,
        lastname=lastname,
        oauth_provider=OAuthProvider.GOOGLE,
        oauth_id=oauth_id,
    )
