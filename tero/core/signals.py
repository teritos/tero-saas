import django.dispatch


motion_detected = django.dispatch.Signal(
    providing_args=[
        "alarm", 
        "active", 
        "filepath"
    ]
)
userprofile_created = django.dispatch.Signal(
    providing_args=[
        "username",
        "password",
        "alarm",
        "ftpd",
    ]
)
