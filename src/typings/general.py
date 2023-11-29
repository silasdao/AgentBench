import builtins
from typing import List, Dict, Union, Any, Literal

from pydantic import BaseModel, validator

JSONSerializable = Union[None, bool, int, float, str, List[Any], Dict[str, Any]]
SampleIndex = Union[int, str]


class InstanceFactory(BaseModel):
    module: str
    parameters: Dict[str, Any] = {}

    @validator("parameters", pre=True)
    def _ensure_dict(cls, v):
        return {} if v is None else v

    def create(self):
        # print('>>>>>>>> ', self.module, self.parameters)
        splits = self.module.split(".")
        if len(splits) == 0:
            raise Exception(f"Invalid module name: {self.module}")
        if len(splits) == 1:
            g = globals()
            class_type = g.get(self.module, getattr(builtins, self.module))
            return class_type(**self.parameters)
        else:
            path = ".".join(self.module.split(".")[:-1])
            mod = __import__(path, fromlist=[self.module.split(".")[-1]])
            return getattr(mod, self.module.split(".")[-1])(**self.parameters)


class Assignment(BaseModel):
    agent: str
    task: str


class ChatHistoryItem(BaseModel):
    role: Literal["user", "agent"]
    content: str
