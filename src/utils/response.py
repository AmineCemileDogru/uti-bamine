
from sdks.novavision.src.helper.package import PackageHelper
from components.BAmine.src.models.PackageModel import PackageModel, PackageConfigs, ConfigExecutor, BAmineExecutorOutputs, BAmineExecutorResponse, BAmineExecutor, OutputImage


def build_response(context):
    outputImage = OutputImage(value=context.image)
    bAmineExecutorOutputs = BAmineExecutorOutputs(outputImage=outputImage)
    bAmineExecutorResponse = BAmineExecutorResponse(outputs=bAmineExecutorOutputs)
    bAmineExecutor = BAmineExecutor(value=bAmineExecutorResponse)
    configexecutor = ConfigExecutor(value=bAmineExecutor)
    packageConfigs = PackageConfigs(executor=configexecutor)
    package = PackageHelper(packageModel=PackageModel, packageConfigs=packageConfigs)
    packageModel = package.build_model(context)
    return packageModel