
from sdks.novavision.src.helper.package import PackageHelper
from components.BAmine.src.models.PackageModel import PackageModel, PackageConfigs, ConfigExecutor, BAmineExecutorOutputs, BAmineExecutorResponse, BAmineExecutor, CAmineExecutorOutputs, CAmineExecutorResponse, CAmineExecutor, OutputImageOne, OutputImageTwo


def build_response_b(context):
    outputImageOne = OutputImageOne(value=context.image_one)
    b_outputs = BAmineExecutorOutputs(outputImageOne=outputImageOne)
    b_response = BAmineExecutorResponse(outputs=b_outputs)
    b_executor = BAmineExecutor(value=b_response)
    configexecutor = ConfigExecutor(value=b_executor)
    packageConfigs = PackageConfigs(executor=configexecutor)
    package = PackageHelper(packageModel=PackageModel, packageConfigs=packageConfigs)
    return package.build_model(context)


def build_response_c(context):
    outputImageOne = OutputImageOne(value=context.image_one)
    outputImageTwo = OutputImageTwo(value=context.image_two)
    c_outputs = CAmineExecutorOutputs(outputImageOne=outputImageOne, outputImageTwo=outputImageTwo)
    c_response = CAmineExecutorResponse(outputs=c_outputs)
    c_executor = CAmineExecutor(value=c_response)
    configexecutor = ConfigExecutor(value=c_executor)
    packageConfigs = PackageConfigs(executor=configexecutor)
    package = PackageHelper(packageModel=PackageModel, packageConfigs=packageConfigs)
    return package.build_model(context)
