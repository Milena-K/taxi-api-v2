from channels.generic.websocket import (
    WebsocketConsumer,
)
from django.core.serializers.json import (
    DjangoJSONEncoder,
)
from asgiref.sync import (
    async_to_sync,
)

import json


class DriverConsumer(
    WebsocketConsumer
):
    def __init__(
        self, *args, **kwargs
    ):
        super().__init__(
            args, kwargs
        )
        self.group_name = None

    def connect(self):
        self.driver_id = (
            self.scope[
                "url_route"
            ]["kwargs"][
                "driver_id"
            ]
        )
        self.group_name = f"driver_{self.driver_id}"
        self.groups.append(
            self.group_name
        )  # important otherwise some cleanup does not happened on disconnect.
        async_to_sync(
            self.channel_layer.group_add
        )(
            self.group_name,
            self.channel_name,
        )
        self.accept()

    def receive(
        self, text_data
    ):
        data = json.loads(
            text_data
        )
        async_to_sync(
            self.channel_layer.group_send
        )(
            self.group_name,
            {
                "type": "ride_accepted",
                "ride_uuid": data[
                    "ride_uuid"
                ],
                "passenger": data[
                    "passenger"
                ],
                "price": data[
                    "price"
                ],
                "room_uuid": data[
                    "room_uuid"
                ],
            },
        )

    def disconnect(
        self, close_code
    ):
        async_to_sync(
            self.channel_layer.group_discard
        )(
            self.group_name,
            self.channel_name,
        )

    def ride_accepted(
        self, event
    ):
        self.send(
            text_data=json.dumps(
                {
                    "message": event[
                        "message"
                    ],
                    "passenger": event[
                        "passenger"
                    ],
                    "starting_location": event[
                        "starting_location"
                    ],
                    "destination": event[
                        "destination"
                    ],
                    "price": event[
                        "price"
                    ],
                    "dropoff_time": event[
                        "dropoff_time"
                    ],
                    "ride_duration": event[
                        "ride_duration"
                    ],
                    "ride_uuid": event[
                        "ride_uuid"
                    ],
                }
            )
        )

    def ride_canceled_by_passenger(
        self, event
    ):
        self.send(
            text_data=json.dumps(
                {
                    "message": event[
                        "message"
                    ],
                    "passenger": event[
                        "passenger"
                    ],
                    "ride_uuid": event[
                        "ride_uuid"
                    ],
                }
            )
        )

    def send_location_data(
        self, event
    ):
        """
        the driver sends constant location messages to user
        """
        self.send(
            text_data=json.dumps(
                {
                    "current_location": event[
                        "current_location"
                    ],
                    "driver": event[
                        "driver"
                    ],
                },
                cls=DjangoJSONEncoder,
            )
        )


class PassengerConsumer(
    WebsocketConsumer
):
    def __init__(
        self, *args, **kwargs
    ):
        super().__init__(
            args, kwargs
        )
        self.group_name = None

    def connect(self):
        self.passenger_id = (
            self.scope[
                "url_route"
            ]["kwargs"][
                "passenger_id"
            ]
        )
        self.group_name = f"passenger_{self.passenger_id}"
        self.groups.append(
            self.group_name
        )  # important otherwise some cleanup does not happened on disconnect.
        async_to_sync(
            self.channel_layer.group_add
        )(
            self.group_name,
            self.channel_name,
        )
        self.accept()

    def disconnect(
        self, close_code
    ):
        async_to_sync(
            self.channel_layer.group_discard
        )(
            self.group_name,
            self.channel_name,
        )

    def new_driver_offer(
        self, event
    ):
        self.send(
            text_data=json.dumps(
                {
                    "driver": event[
                        "driver"
                    ],
                    "price": event[
                        "price"
                    ],
                    "dropoff_time": event[
                        "dropoff_time"
                    ],
                    "ride_duration": event[
                        "ride_duration"
                    ],
                    "ride_uuid": event[
                        "ride_uuid"
                    ],
                },
                cls=DjangoJSONEncoder,
            )
        )

    def start_ride(
        self, event
    ):
        self.send(
            text_data=json.dumps(
                {
                    "message": event[
                        "message"
                    ],
                    "passenger": event[
                        "passenger"
                    ],
                    "driver": event[
                        "driver"
                    ],
                    "ride_uuid": event[
                        "ride_uuid"
                    ],
                }
            )
        )

    def cancel_ride(
        self, event
    ):
        self.send(
            text_data=json.dumps(
                {
                    "message": event[
                        "message"
                    ],
                    "passenger": event[
                        "passenger"
                    ],
                    "driver": event[
                        "driver"
                    ],
                    "price": event[
                        "price"
                    ],
                    "ride_uuid": event[
                        "ride_uuid"
                    ],
                }
            )
        )
