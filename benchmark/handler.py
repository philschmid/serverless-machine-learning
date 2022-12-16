import time

function_start = time.time()
import cpufeature
import json
import os


def import_onnxruntime():
    import onnxruntime


def load_onnx_model(path):
    import onnxruntime

    return onnxruntime.InferenceSession(path)


def import_torch():
    import torch


def load_torch_model(path):
    import torch

    return torch.load(path)


def measure_execution_of_method(method, *args, **kwargs):
    start = time.time()
    method(*args, **kwargs)
    end = time.time()
    return end - start


def handler(event, context):
    # measure pytorch
    import_torch_time = measure_execution_of_method(import_torch)
    load_torch_model_time = measure_execution_of_method(load_torch_model, "model/pytorch_model.bin")
    # measure onnxruntime
    import_onnxruntime_time = measure_execution_of_method(import_onnxruntime)
    load_onnx_model_time = measure_execution_of_method(load_onnx_model, "model/model.onnx")

    # get CPU Features
    cpu_features = cpufeature.CPUFeature
    file_size = os.stat("model/pytorch_model.bin").st_size / (1024 * 1024)
    # return results
    result = {
        "pytroch": {"import": import_torch_time, "load_model": load_torch_model_time},
        "onnxruntime": {"import": import_onnxruntime_time, "load_model": load_onnx_model_time},
        "cpu_features": cpu_features,
        "file_size": file_size,
        "function_start_time": function_start,
    }
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Credentials": True,
        },
        "body": json.dumps(result),
    }


if __name__ == "__main__":
    res = handler(None, None)
    print(
        json.loads(
            res["body"],
        )
    )
