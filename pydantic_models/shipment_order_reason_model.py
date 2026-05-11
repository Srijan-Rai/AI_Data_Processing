from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field
from uuid import UUID, uuid4


class ShipmentReasonEvent(BaseModel):
    """
    A single tender/reason event for a shipment.
    One shipment can have multiple of these.
    """
    reason_id: UUID = Field(default_factory=uuid4)
    reason: str = Field(..., description="Reason for retender/rejection/etc.")
    tender_time: datetime = Field(..., description="Tender creation time")
    tender_response_time: datetime = Field(
        ..., description="Carrier/system response time"
    )


class Shipment(BaseModel):
    """
    One shipment under an order.
    A shipment can have multiple reason events.
    Pickup/Delivery/Delete are shipment-level attributes.
    """

    shipment_id: str = Field(..., alias="shipment")

    pickup_appointment: datetime
    delivery_appointment: datetime
    delete_time: Optional[datetime] = None

    reason_events: List[ShipmentReasonEvent] = Field(default_factory=list)
    invalid_reason_list: List[str] = Field(default_factory=list)

    model_config = {
        "populate_by_name": True
    }


class Order(BaseModel):
    """
    One order can contain multiple shipments.
    """

    order_number: str
    shipments: List[Shipment] = Field(default_factory=list)