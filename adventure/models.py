from django.db import models
from math import ceil
import numpy as np
import re
# Create your models here.


class VehicleType(models.Model):
    name = models.CharField(max_length=32)
    max_capacity = models.PositiveIntegerField()

    def __str__(self) -> str:
        return self.name


class Vehicle(models.Model):
    name = models.CharField(max_length=32)
    passengers = models.PositiveIntegerField()
    vehicle_type = models.ForeignKey(VehicleType, null=True, on_delete=models.SET_NULL)
    number_plate = models.CharField(max_length=10)

    def __str__(self) -> str:
        return self.name

    def can_start(self) -> bool:
        return self.vehicle_type.max_capacity >= self.passengers

    def get_distribution(self) -> []:
        seat_distribution = [
            True
            for _ in range(self.vehicle_type.max_capacity)
        ]
        _empty_seats = self.vehicle_type.max_capacity - self.passengers
        for index in range(_empty_seats):
            seat_distribution[index] = False

        seat_distribution = np.array_split(
            list(reversed(seat_distribution))
            ,ceil(self.vehicle_type.max_capacity/2)
        )

        return [
            list(pair)
            for pair in seat_distribution
        ]

    def validate_number_plate(self) -> bool:
        return re.search("[A-Z]{2}-[0-9]{2}-[0-9]{2}",self.number_plate)

class Journey(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.PROTECT)
    start = models.DateField()
    end = models.DateField(null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.vehicle.name} ({self.start} - {self.end})"

    def is_finished(self) -> bool:
        return self.end != None

