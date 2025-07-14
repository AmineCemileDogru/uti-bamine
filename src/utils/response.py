
from sdks.novavision.src.helper.package import PackageHelper
from components.BAmine.src.models.PackageModel import PackageModel, PackageConfigs, ConfigExecutor, BAmineExecutorOutputs, BAmineExecutorResponse, BAmineExecutor, CAmineExecutorOutputs, CAmineExecutorResponse, CAmineExecutor, OutputImageOne, OutputImageTwo


def build_response_b(context):
    outputImageOne = OutputImageOne(value=context.image)
    bAmineExecutorOutputs = BAmineExecutorOutputs(outputImage=outputImageOne)
    bAmineExecutorResponse = BAmineExecutorResponse(outputs=bAmineExecutorOutputs)
    bAmineExecutor = BAmineExecutor(value=bAmineExecutorResponse)
    configexecutor = ConfigExecutor(value=bAmineExecutor)
    packageConfigs = PackageConfigs(executor=configexecutor)
    package = PackageHelper(packageModel=PackageModel, packageConfigs=packageConfigs)
    packageModel = package.build_model(context)
    return packageModel

def build_response_c(context):
    outputImageOne = OutputImageOne(value=context.image_one)
    outputImageTwo = OutputImageTwo(value=context.image_two)
    cAmineExecutorOutputs = CAmineExecutorOutputs(
        outputImageOne=outputImageOne,
        outputImageTwo=outputImageTwo
    )
    cAmineExecutorResponse = CAmineExecutorResponse(outputs=cAmineExecutorOutputs)
    cAmineExecutor = CAmineExecutor(value=cAmineExecutorResponse)
    configexecutor = ConfigExecutor(value=cAmineExecutor)
    packageConfigs = PackageConfigs(executor=configexecutor)
    package = PackageHelper(packageModel=PackageModel, packageConfigs=packageConfigs)
    packageModel = package.build_model(context)
    return packageModel