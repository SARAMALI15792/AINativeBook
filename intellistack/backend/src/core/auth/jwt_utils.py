"""
Shared JWT validation helper.

Single source of truth for EdDSA JWT decoding used by both the JWKS middleware
(perimeter validation) and the get_current_user dependency (inner validation).

Responsibilities
----------------
- Parse the unverified JWT header to extract `kid` and `alg`.
- Reject any token whose `alg` header is not "EdDSA" — **before** any network call.
- Fetch the JWKS and locate the key by `kid`.
- Reject any JWKS key whose algorithm is not "EdDSA".
- Verify the signature and return the decoded payload dict.

Return contract
---------------
- Returns a ``dict`` of JWT claims on success.
- Returns ``None`` if the token is structurally not a JWT (no ``kid``, or
  cannot be parsed as a JWT header) — callers should try a session-token
  fallback in that case.
- Raises ``fastapi.HTTPException(401)`` for every *intentional* rejection
  (bad algorithm, key not found after a valid JWT header, decode failure).
"""

import logging
from typing import Any, Dict, Optional

import jwt
from fastapi import HTTPException, status
from jwt import PyJWK, PyJWTError

logger = logging.getLogger(__name__)


async def decode_bearer_jwt(
    token: str,
    jwks_manager,   # JWKSManager — typed loosely to avoid circular imports
    settings,       # Settings
) -> Optional[Dict[str, Any]]:
    """
    Validate a Bearer JWT against the shared JWKS manager.

    Parameters
    ----------
    token:
        Raw Bearer token string (no "Bearer " prefix).
    jwks_manager:
        A ``JWKSManager`` instance — obtain via ``get_shared_jwks_manager()``.
    settings:
        Application ``Settings`` — used for optional audience/issuer validation.

    Returns
    -------
    dict
        Decoded JWT claims on success.
    None
        Token is not a recognisable JWT (no parseable header / no ``kid``).

    Raises
    ------
    HTTPException(401)
        * Token header specifies a non-EdDSA algorithm.
        * ``kid`` present but not found in JWKS.
        * JWKS returned a key with a non-EdDSA algorithm.
        * JWT signature/expiry verification failed.
    """
    # --- Step 1: parse the unverified header --------------------------------
    try:
        unverified_header = jwt.get_unverified_header(token)
    except jwt.DecodeError:
        # Not a JWT at all — caller should try a session-token fallback.
        return None

    kid: Optional[str] = unverified_header.get("kid")
    algorithm: str = unverified_header.get("alg", "EdDSA")

    # --- Step 2: enforce EdDSA algorithm BEFORE any network call -----------
    # Rejecting here closes the algorithm-confusion attack window early and
    # avoids paying the JWKS fetch cost for obviously invalid tokens.
    if algorithm != "EdDSA":
        logger.warning(
            "JWT rejected: header claims alg=%r; only EdDSA tokens are accepted. "
            "Possible algorithm-confusion attack.",
            algorithm,
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token: unsupported signing algorithm",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not kid:
        # Structurally not a JWT we can validate (no key ID).
        return None

    # --- Step 3: fetch JWKS and locate the key -----------------------------
    jwks = await jwks_manager.fetch_jwks()
    key_data: Optional[Dict[str, Any]] = None
    for key in jwks.get("keys", []):
        if key.get("kid") == kid:
            key_data = key
            break

    if key_data is None:
        logger.warning("JWT rejected: kid=%r not found in JWKS", kid)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token: signing key not found",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # --- Step 4: enforce EdDSA on the key itself ---------------------------
    jwk = PyJWK.from_dict(key_data)
    key_algorithm: str = jwk.algorithm_name
    if key_algorithm != "EdDSA":
        logger.error(
            "JWKS key kid=%r has algorithm=%r; only EdDSA keys are trusted. "
            "Check Better-Auth server configuration.",
            kid,
            key_algorithm,
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token: unsupported key algorithm",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # --- Step 5: verify signature -------------------------------------------
    aud = settings.better_auth_audience or None
    iss = settings.better_auth_issuer or None

    try:
        payload: Dict[str, Any] = jwt.decode(
            token,
            jwk.key,
            algorithms=["EdDSA"],
            audience=aud,
            issuer=iss,
            options={
                "verify_aud": aud is not None,
                "verify_iss": iss is not None,
            },
        )
    except jwt.ExpiredSignatureError:
        logger.debug("JWT rejected: token has expired")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except PyJWTError as exc:
        logger.warning("JWT signature verification failed: %s", exc)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token: signature verification failed",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return payload
