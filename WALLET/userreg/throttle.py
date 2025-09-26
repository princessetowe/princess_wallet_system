from rest_framework.throttling import AnonRateThrottle

class SignUpThrottle(AnonRateThrottle):
    scope = "signup"

class LoginThrottle(AnonRateThrottle):
    scope = "login"