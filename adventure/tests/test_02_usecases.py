import pytest
from django.utils import timezone

from adventure import models, notifiers, repositories, usecases

#########
# Mocks #
#########


class MockJourneyRepository(repositories.JourneyRepository):
    def get_or_create_car(self) -> models.VehicleType:
        return models.VehicleType(name="car", max_capacity=4)

    def create_vehicle(
        self, name: str, passengers: int, vehicle_type: models.VehicleType
    ) -> models.Vehicle:
        return models.Vehicle(
            name=name, passengers=passengers, vehicle_type=vehicle_type
        )

    def create_journey(self, vehicle) -> models.Journey:
        return models.Journey(vehicle=vehicle, start=timezone.now().date())

    def end_journey(self, journey: models.Journey) -> models.Journey:
        journey.end = timezone.now().date()
        journey.save()
        return journey

class MockNotifier(notifiers.Notifier):
    def send_notifications(self, journey: models.Journey) -> None:
        pass


#########
# Tests #
#########


class TestStartJourney:
    def test_start(self):
        repo = MockJourneyRepository()
        notifier = MockNotifier()
        data = {"name": "Kitt", "passengers": 2}
        usecase = usecases.StartJourney(repo, notifier).set_params(data)
        journey = usecase.execute()

        assert journey.vehicle.name == "Kitt"

    def test_cant_start(self):
        repo = MockJourneyRepository()
        notifier = MockNotifier()
        data = {"name": "Kitt", "passengers": 6}
        usecase = usecases.StartJourney(repo, notifier).set_params(data)
        with pytest.raises(usecases.StartJourney.CantStart):
            journey = usecase.execute()


class TestStopJourney:
    def test_stop(self):
        # TODO: Implement a StopJourney Usecase
        # it takes a started journey as a parameter and sets an "end" value
        # then saves it to the database
        repo = MockJourneyRepository()
        notifier = MockNotifier()
        data = {"name": "Ardyn", "passengers": 2}
        #usecase = usecases.StopJourney(repo, notifier).set_params(data)
        #stopped_journey = usecase.execute()

        #assert stopped_journey.end != None
