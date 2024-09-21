from channels.layers import (
    get_channel_layer,
)
from asgiref.sync import (
    async_to_sync,
)
from celery import shared_task
import uuid

channel_layer = (
    get_channel_layer()
)


@shared_task
def find_driver_for_ride(
    passenger: int,
    starting_location: str,
    destination: str,
    ride_uuid: uuid.UUID,
):
    """
    Find a driver for a ride by sending a ride request message.
    """
    dropoff_time = "2024-09-19T00:00:00"  # TODO: calculate
    ride_duration = (
        0  # TODO: calculate
    )
    # TODO should i calculate the price here as well
    async_to_sync(
        channel_layer.group_send
    )(
        "requests_group",
        {
            "type": "new_passenger_request",
            "passenger": passenger,
            "starting_location": starting_location,
            "destination": destination,
            "dropoff_time": dropoff_time,
            "ride_duration": ride_duration,
            "ride_uuid": str(
                ride_uuid
            ),
        },
    )


@shared_task
def send_ride_offer(
    driver: int,
    price: int,
    ride_duration: int,
    dropoff_time: int,
    ride_uuid: uuid.UUID,
    passenger_id: int,
):
    async_to_sync(
        channel_layer.group_send
    )(
        f"passenger_{passenger_id}",
        {
            "type": "new_driver_offer",
            "driver": driver,
            "price": price,
            "dropoff_time": dropoff_time,
            "ride_duration": ride_duration,
            "ride_uuid": str(
                ride_uuid
            ),
        },
    )


@shared_task
def accept_ride_offer(
    driver_id: int,
    passenger_id: int,
    starting_location: str,
    destination: str,
    ride_duration: int,
    dropoff_time: int,
    price: int,
    ride_uuid: uuid.UUID,
):
    """
    Send direct message to the chosen driver that the ride is accepted
    """
    async_to_sync(
        channel_layer.group_send
    )(
        f"driver_{driver_id}",
        {
            "type": "ride_accepted",
            "message": "Ride accepted!",
            "passenger": passenger_id,
            "starting_location": starting_location,
            "destination": destination,
            "price": price,
            "dropoff_time": dropoff_time,
            "ride_duration": ride_duration,
            "ride_uuid": str(
                ride_uuid
            ),
        },
    )


@shared_task
def start_ride_task(
    passenger: int,
    driver: int,
    ride_uuid: uuid.UUID,
):
    """
    Send a message as a passenger or driver that a ride was canceled
    """
    async_to_sync(
        channel_layer.group_send
    )(
        f"passenger_{passenger}",
        {
            "type": "start_ride",
            "message": "Ride started!",
            "passenger": passenger,
            "driver": driver,
            "ride_uuid": str(
                ride_uuid
            ),
        },
    )


@shared_task
def cancel_ride_task(
    passenger: int,
    driver_id: int,
    ride_uuid: uuid.UUID,
):
    async_to_sync(
        channel_layer.group_send
    )(
        f"driver_{driver_id}",
        {
            "type": "ride_canceled_by_passenger",
            "message": "Ride canceled!",
            "passenger": passenger,
            "ride_uuid": ride_uuid,
        },
    )


@shared_task
def cancel_active_ride_task(
    passenger: int,
    driver: int,
    price: int,
    ride_uuid: uuid.UUID,
):
    """
    Send a message as a passenger or driver that a ride was canceled
    """
    async_to_sync(
        channel_layer.group_send
    )(
        f"passenger_{passenger}",
        {
            "type": "cancel_ride",
            "message": "Ride has finished!",
            "passenger": passenger,
            "driver": driver,
            "price": price,
            "ride_uuid": str(
                ride_uuid
            ),
        },
    )
