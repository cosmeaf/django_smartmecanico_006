# fleet_management/admin.py

from django.contrib import admin
from .models import FleetVehicle, MaintenanceRecord, ExpenseRecord, TripLog, Driver

admin.site.register(FleetVehicle)
admin.site.register(MaintenanceRecord)
admin.site.register(ExpenseRecord)
admin.site.register(Driver)
admin.site.register(TripLog)