- venv create
- started a new project
- started a new app
- adding config for rest_framework and our custom app
- created function and class endpoints
- added models
- created migration
- ran migration
- populated admin.py and created super user, 'python manage.py createsuperuser'
- created serializer 
- created serializer for FK
- created serializerMethodField
- created query for future slots

# Technical edge cases handled
- Race-condition in bookings endpoint, by using translational update
- N+1 queries problem, by doing proper join
- Unique together/composite key to avoid double booking for same user

# Non-Technical Edge cases handled
- 



# transaction.atomic
# F (field based query)
# __ for nested queries
# select_related for joins
# python manage.py shell to run commands
    # from api.models import *


# Home Work
- Add description field in class, show it in all the APIs
- Add date range filter in /classes endpoint
- Add pagination in /classes endpoint

# Feature
- Users will have coins
- Each class will cost some coin
- Booking will decrement user's coins