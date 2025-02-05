""" This module contains the base class for all API models, which will be
read-only and have limited fields, so we don't expose private or sensitive
fields to the client.
"""

from pydantic import BaseModel


class ApiBaseModel(BaseModel):
    class Config:
        populate_by_name = True
        # we could add some json_encoders here
