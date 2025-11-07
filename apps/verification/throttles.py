from rest_framework.throttling import ScopedRateThrottle
from rest_framework.exceptions import Throttled

class RequstVerifyThrottle(ScopedRateThrottle):
    scope = 'request_verify'

    def throttle_failure(self):
        wait = self.wait()
        detail = {"detail": f"Too many OTP requests. Try again in {int(wait)} seconds."}
        raise Throttled(detail=detail)
