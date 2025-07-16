
from pydantic import Field, validator
from typing import List, Optional, Union, Literal
from sdks.novavision.src.base.model import Package, Image, Inputs, Configs, Outputs, Response, Request, Output, Input, Config


class InputImageOne(Input):
    name: Literal["inputImageOne"] = "inputImageOne"
    value: Union[List[Image], Image]
    type: str = "object"

    @validator("type", pre=True, always=True)
    def set_type_based_on_value(cls, value, values):
        value = values.get('value')
        if isinstance(value, Image):
            return "object"
        elif isinstance(value, list):
            return "list"

    class Config:
        title = "Image"

class InputImageTwo(Input):
    name: Literal["inputImageTwo"] = "inputImageTwo"
    value: Union[List[Image], Image]
    type: str = "object"

    @validator("type", pre=True, always=True)
    def set_type_based_on_value(cls, value, values):
        value = values.get('value')
        if isinstance(value, Image):
            return "object"
        elif isinstance(value, list):
            return "list"

    class Config:
        title = "Image"


class OutputImageOne(Output):
    name: Literal["outputImageOne"] = "outputImageOne"
    value: Union[List[Image],Image]
    type: str = "object"

    @validator("type", pre=True, always=True)
    def set_type_based_on_value(cls, value, values):
        value = values.get('value')
        if isinstance(value, Image):
            return "object"
        elif isinstance(value, list):
            return "list"

    class Config:
        title = "Image"

class OutputImageTwo(Output):
    name: Literal["outputImageTwo"] = "outputImageTwo"
    value: Union[List[Image],Image]
    type: str = "object"

    @validator("type", pre=True, always=True)
    def set_type_based_on_value(cls, value, values):
        value = values.get('value')
        if isinstance(value, Image):
            return "object"
        elif isinstance(value, list):
            return "list"

    class Config:
        title = "Image"


class KeepSideFalse(Config):
    name: Literal["False"] = "False"
    value: Literal[False] = False
    type: Literal["bool"] = "bool"
    field: Literal["option"] = "option"

    class Config:
        title = "Disable"


class KeepSideTrue(Config):
    name: Literal["True"] = "True"
    value: Literal[True] = True
    type: Literal["bool"] = "bool"
    field: Literal["option"] = "option"

    class Config:
        title = "Enable"


class KeepSideBBox(Config):
    """
        Rotate image without catting off sides.
    """
    name: Literal["KeepSide"] = "KeepSide"
    value: Union[KeepSideTrue, KeepSideFalse]
    type: Literal["object"] = "object"
    field: Literal["dropdownlist"] = "dropdownlist"

    class Config:
        title = "Keep Sides"


class Degree(Config):
    """
        Positive angles specify counterclockwise rotation while negative angles indicate clockwise rotation.
    """
    name: Literal["Degree"] = "Degree"
    value: int = Field(ge=-359.0, le=359.0,default=0)
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"
    placeHolder: Literal["[-359, 359]"] = "[-359, 359]"

    class Config:
        title = "Anglee"




class CropBoxSize(Config):
    name: Literal["CropBoxSize"] = "CropBoxSize"
    value: int = Field(default=100, ge=10, le=500)
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"

    class Config:
        title = "Crop Box Size"

class CropRatio(Config):
    name: Literal["CropRatio"] = "CropRatio"
    value: float = Field(default=0.5, ge=0.1, le=1.0)
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"

    class Config:
        title = "Crop Ratio"

class CropType(Config):
    name: Literal["CropType"] = "CropType"
    value: Union[CropBoxSize, CropRatio]
    type: Literal["object"] = "object"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"

    class Config:
        title = "Crop Type Selection"




class BAmineExecutorInputs(Inputs):
    inputImageOne: InputImageOne


class BAmineExecutorConfigs(Configs):
    degree: Degree
    drawBBox: KeepSideBBox

class BAmineExecutorRequest(Request):
    inputs: Optional[BAmineExecutorInputs]
    configs: BAmineExecutorConfigs

    class Config:
        json_schema_extra = {
            "target": "configs"
        }

class BAmineExecutorOutputs(Outputs):
    outputImageOne: OutputImageOne

class BAmineExecutorResponse(Response):
    outputs: BAmineExecutorOutputs

class BAmineExecutor(Config):
    name: Literal["BAmine"] = "BAmine"
    value: Union[BAmineExecutorRequest, BAmineExecutorResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"

    class Config:
        title = "Blurring"
        json_schema_extra = {
            "target": {
                "value": 0
            }
        }








class CAmineExecutorInputs(Inputs):
    inputImageOne: InputImageOne
    inputImageTwo: InputImageTwo


class CAmineExecutorConfigs(Configs):
    cropType: CropType

class CAmineExecutorRequest(Request):
    inputs: Optional[CAmineExecutorInputs]
    configs: CAmineExecutorConfigs

    class Config:
        json_schema_extra = {
            "target": "configs"
        }

class CAmineExecutorOutputs(Outputs):
    outputImageOne: OutputImageOne
    outputImageTwo: OutputImageTwo

class CAmineExecutorResponse(Response):
    outputs: CAmineExecutorOutputs

class CAmineExecutor(Config):
    name: Literal["CAmine"] = "CAmine"
    value: Union[CAmineExecutorRequest, CAmineExecutorResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"

    class Config:
        title = "Crop"
        json_schema_extra = {
            "target": {
                "value": 0
            }
        }






class ConfigExecutor(Config):
    name: Literal["ConfigExecutor"] = "ConfigExecutor"
    value: Union[BAmineExecutor, CAmineExecutor]
    type: Literal["executor"] = "executor"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"
    restart: Literal[True] = True

    class Config:
        title = "Type"

class PackageConfigs(Configs):
    executor: ConfigExecutor

class PackageModel(Package):
    configs: PackageConfigs
    type: Literal["component"] = "component"
    name: Literal["BAmine"] = "BAmine"
