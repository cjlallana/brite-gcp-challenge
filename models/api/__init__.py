""" This module contains the base class for all API models, which will be
read-only and have limited fields, so we don't expose private or sensitive
fields to the client.
"""

from pydantic import BaseModel, ConfigDict


class ApiBaseModel(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    # we could also add some json_encoders here
