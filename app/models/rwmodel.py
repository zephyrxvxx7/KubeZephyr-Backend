from datetime import datetime, timezone
from bson.objectid import ObjectId
from bson.errors import InvalidId
from typing import Any, Generator, Union, Dict

from pydantic import BaseConfig, BaseModel


# class MongoModel(BaseModel):
#     class Config(BaseConfig):
#         allow_population_by_alias = True
#         json_encoders = {
#             datetime: lambda dt: dt.replace(tzinfo=timezone.utc)
#             .isoformat()
#             .replace("+00:00", "Z")
#         }

# Validation ObjectId for pydantic
class OID(str):
  @classmethod
  def __get_validators__(cls) -> Generator:
      yield cls.validate

  @classmethod
  def validate(cls, v: Any) -> ObjectId:
      try:
          return ObjectId(str(v))
      except InvalidId:
          raise ValueError("Not a valid ObjectId")


class MongoModel(BaseModel):
  class Config(BaseConfig):
      allow_population_by_field_name = True
      json_encoders = {
          datetime: lambda dt: dt.isoformat(),
          ObjectId: lambda oid: str(oid),
      }

  @classmethod
  def from_mongo(cls, data: dict) -> Union["MongoModel", Dict]:
      """convert _id into "id". """
      if not data:
          return data
      id = data.pop('_id', None)
      return cls(**dict(data, id=id))

  def mongo(self, **kwargs) -> Dict[Any, Any]:
      exclude_unset = kwargs.pop('exclude_unset', True)
      by_alias = kwargs.pop('by_alias', True)

      parsed = self.dict(
          exclude_unset=exclude_unset,
          by_alias=by_alias,
          **kwargs,
      )

      # Mongo uses `_id` as default key. We should stick to that as well.
      if '_id' not in parsed and 'id' in parsed:
          parsed['_id'] = parsed.pop('id')

      return parsed


# class User(_MongoModel):
#   id: OID = Field()
#   name: str = Field()


# @app.post('/me', response_model=User)
# def save_me(body: User):
#   assert isinstance(body.id, ObjectId)
#   res = db.insert_one(body.mongo())
#   assert res.inserted_id == body.id

#   found = col.find_one({'_id': res.inserted_id})
#   return User.from_mongo(found)