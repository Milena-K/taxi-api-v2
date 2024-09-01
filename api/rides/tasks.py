from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from celery import shared_task
import uuid

channel_layer = get_channel_layer()

@shared_task
def find_driver_for_ride(passenger: int, starting_location: str, destination: str, ride_uuid: uuid.UUID):
    """
    Find a driver for a ride by sending a ride request message.
    """
    dropoff_time = 0 # TODO: calculate
    ride_duration = 0 # TODO: calculate
    async_to_sync(channel_layer.group_send)(
        "requests_group",
        {
            "type": "new_passenger_request",
            "passenger": passenger,
            "starting_location": starting_location,
            "destination": destination,
            "dropoff_time": dropoff_time,
            "ride_duration": ride_duration,
            "ride_uuid": str(ride_uuid)
        }
    )

@shared_task
def send_ride_offer(driver: int, price: int, ride_duration: int, dropoff_time: int, ride_uuid: uuid.UUID, passenger_id: int):
    async_to_sync(channel_layer.group_send)(
        f"passenger_{passenger_id}",
        {
            "type": "new_driver_offer",
            "driver": driver,
            "price": price,
            "ride_duration": ride_duration,
            "dropoff_time": dropoff_time,
            "ride_uuid": str(ride_uuid)
        }
    )


@shared_task
def accept_ride_offer(driver_id: int, passenger_id: int, starting_location: str, \
                      destination:str, ride_duration: int, dropoff_time: int, \
                      price: int, ride_uuid: uuid.UUID):
    """
    Send direct message to the chosen driver that the ride is accepted
    """
    async_to_sync(channel_layer.group_send)(
        f"driver_{driver_id}",
        {
            "type": "ride_accepted",
            "message": "Ride accepted!",
            "passenger": passenger_id,
            "starting_location": starting_location,
            "destination": destination,
            "price": price,
            "ride_duration": ride_duration,
            "dropoff_time": dropoff_time,
            "ride_uuid": str(ride_uuid),
        }
    )


@shared_task
def cancel_ride_task(passenger: int, ride_uuid: uuid.UUID):
    """
    Send a message to the drivers that a passenger has canceled a ride
    """
    async_to_sync(channel_layer.group_send)(
        "requests_group",
        {
            "type": "cancel_ride",
            "passenger": passenger,
            "ride_uuid": str(ride_uuid)
        }
    )
