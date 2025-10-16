from rest_framework.throttling import AnonRateThrottle
from rest_framework.exceptions import Throttled

class BaseThrottle(AnonRateThrottle):
    def throttle_failure(self):
        exc = Throttled(wait=self.wait())
        exc.scope_name = self.scope
        raise exc
class SignUpThrottle(BaseThrottle):
    scope = "signup"

class LoginThrottle(BaseThrottle):
    scope = "login"