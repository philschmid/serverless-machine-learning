import os
import json
import time
import pandas as pd
import collections


def flatten(d, parent_key="", sep="_"):
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, collections.MutableMapping):
            items.extend(flatten(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


# set aws profile and default region
os.environ["AWS_DEFAULT_REGION"] = "us-east-1"

ssm_parameter = "/benchmark/lambda/name"
lambda_memory_sizes = [1024, 2048, 4096, 8192]


result_list = []
for memory_size in lambda_memory_sizes:

    os.environ["MEMORY_SIZE"] = str(memory_size)

    # # deploy cdk stack
    os.system("cdk deploy --require-approval never")

    # get lambda function from deployment
    import boto3

    ssm_client = boto3.client("ssm")
    lambda_name = ssm_client.get_parameter(Name=ssm_parameter)["Parameter"]["Value"]
    print(f"Lambda Name: {lambda_name}")
    # invoke lambda function with empty payload and boto3
    lambda_client = boto3.client("lambda")

    start_invoke = time.time()
    response = lambda_client.invoke(
        FunctionName="BenchmarkLambda-AssetFunctionA633A7D1-JLDRVikAatDf",
    )

    response = json.loads(response["Payload"].read())["body"]
    body = json.loads(response)
    result_list.append(
        {
            **flatten(body),
            **{
                "memory_size": memory_size,
                "function_invoke_time": start_invoke,
                "runtime_cold_start": body["function_start_time"] - start_invoke,
            },
        }
    )

df = pd.DataFrame(result_list)
df.to_csv("benchmark.csv", index=False)
df.to_json("benchmark.json", orient="records", indent=2)
