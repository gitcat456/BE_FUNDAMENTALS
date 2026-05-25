from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from django.conf import settings


# [x] User clicks frontend → Google button
# [x] Google authenticates user → gives Google JWT to frontend
# [x] Frontend sends Google JWT to your /api/google_login/
# [x] Your backend verifies Google JWT with Google
# [x] Extract name, email, picture, google_id
# [x] Find existing user or create new User + UserProfile
# [x] Create your JWT with user_id, username, exp
# [x] Return your JWT to frontend
# [x] Frontend stores your JWT and uses it for all future requests
# [x] Your backend verifies your JWT locally on every protected endpoint

def verify_google_token(token: str) -> dict | None:
    """
    Verify the ID token Google gave the frontend.
    Returns user info dict or None if invalid.
    """
    try:
        # this call hits Google's servers to verify the token
        id_info = id_token.verify_oauth2_token(
            token,
            google_requests.Request(),
            settings.GOOGLE_CLIENT_ID
        )

        # ensure token was issued for YOUR app
        if id_info['aud'] != settings.GOOGLE_CLIENT_ID:
            return None

        return {
            'google_id': id_info['sub'],        # unique Google user ID
            'email': id_info['email'],
            'name': id_info.get('name', ''),
            'picture': id_info.get('picture', ''),
            'email_verified': id_info.get('email_verified', False)
        }

    except Exception:
        return None