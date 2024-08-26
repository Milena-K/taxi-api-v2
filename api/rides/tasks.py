from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from celery import shared_task
import uuid


@shared_task
def find_driver_for_ride(passenger: int, starting_location: str, destination: str, ride_uuid: uuid.UUID):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "requests_group",
        {
            "type": "new_passenger_request",
            "passenger": passenger,
            "starting_location": starting_location,
            "destination": destination,
            "ride_uuid": str(ride_uuid)
        }
    )

@shared_task
def send_ride_offer(driver: int, vehicle: str, price: int, ride_uuid: uuid.UUID):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"offers_group_{ride_uuid}",
        {
            "type": "new_driver_offer",
            "driver": driver,
            "vehicle": vehicle,
            "price": price,
            "ride_uuid": str(ride_uuid)
        }
    )


# send direct driver message
@shared_task
def accept_ride_offer(driver_id: int, passenger_id: int, vehicle: str, \
                price: int, ride_uuid: uuid.UUID, room_uuid: uuid.UUID):
    # TODO: also send message to offers_group_[room_uuid] that the ride is now accepted
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"driver_{driver_id}",
        {
            "type": "ride_accepted",
            "passenger": passenger_id,
            "vehicle": vehicle,
            "price": price,
            "ride_uuid": str(ride_uuid),
            "room_uuid": str(room_uuid)
        }
    )

# create a private room
@shared_task
def start_ride(driver_id: int, passenger_id: int, vehicle: str, \
                price: int, ride_uuid: uuid.UUID, room_uuid: uuid.UUID):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"active_ride_{room_uuid}",
        {
            "type": "create_private_room",
            "passenger": passenger_id,
            "vehicle": vehicle,
            "price": price,
            "ride_uuid": str(ride_uuid),
            "room_uuid": str(room_uuid)
        }
    )
