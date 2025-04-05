"""
Constants used throughout the application.
"""

# Headers we want to extract from Booking.com
TARGET_HEADERS = [
    "user-agent",
    "x-booking-context-action-name",
    "x-booking-context-aid",
    "x-booking-csrf-token",
    "x-booking-et-serialized-state",
    "x-booking-pageview-id",
    "x-booking-site-type-id",
    "x-booking-topic",
]

# Map from header name to environment variable name
HEADER_TO_ENV = {
    "user-agent": "USER_AGENT",
    "x-booking-context-action-name": "X_BOOKING_CONTEXT_ACTION_NAME",
    "x-booking-context-aid": "X_BOOKING_CONTEXT_AID",
    "x-booking-csrf-token": "X_BOOKING_CSRF_TOKEN",
    "x-booking-et-serialized-state": "X_BOOKING_ET_SERIALIZED_STATE",
    "x-booking-pageview-id": "X_BOOKING_PAGEVIEW_ID",
    "x-booking-site-type-id": "X_BOOKING_SITE_TYPE_ID",
    "x-booking-topic": "X_BOOKING_TOPIC",
}