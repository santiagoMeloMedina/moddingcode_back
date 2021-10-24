from typing import Any, Dict
from aws_cdk import aws_lambda as _lambda
from src import common


class LocalLambda(_lambda.Function):
    def __init__(self, scope: Any, id: str, source: str, env: Dict[str, str]):
        super().__init__(
            scope=scope,
            id=id,
            code=_lambda.Code.from_asset(common.LOGIC_PROJECT_FOLDER_SRC_PATH_STR),
            handler=".".join([source, "handler"]),
            runtime=_lambda.Runtime.PYTHON_3_8,
            environment=env,
            layers=[LocalLayer(scope=scope)],
        )


class LocalLayer(_lambda.LayerVersion):
    def __init__(self, scope: Any):
        super().__init__(
            scope=scope,
            id="CommonLayer",
            code=_lambda.Code.from_asset(common.LOGIC_PROJECT_FOLDER_ASSETS_PATH_STR),
            compatible_runtimes=[_lambda.Runtime.PYTHON_3_8],
        )
