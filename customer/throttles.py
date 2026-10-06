from rest_framework.throttling import UserRateThrottle

class CustomerRateThrottle(UserRateThrottle):
    scope='customer'