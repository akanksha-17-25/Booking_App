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

