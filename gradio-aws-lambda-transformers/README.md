# Serverless Machine Learning Applications with AWS Lambda and Hugging Face 

This is an example of how to deploy a serverless machine learning application with Hugging Face Gradio and AWS Lambda.


## Local Development

1. Install dependencies

```bash
pip install -r requirements/requirements.txt
```

3. Download Hugging Face model into `model/`
```bash
python get_transfomers.py
```

4. Run the application

```bash
python app.py
```

## Deploying to AWS Lambda

1. install the AWS CDK CLI

```bash
npm install -g aws-cdk
```

2. Install dependencies

```bash
pip install -r requirements/cdk_requirements.txt
```

3. Bootstrap the CDK

_[optional]: export aws profile_
```
export AWS_PROFILE=hf-sm
```

Boostrap project in the cloud
```
cdk bootstrap
```

4. Deploy Gradio application to AWS Lambda

_Note: make sure you ran `utils/get_transformers.py` to have your model in `model/` directory available._

```bash
cdk deploy 
```

1. Delete AWS Lambda again

```bash
cdk destroy
```

## Integrate as web component

[documentation](https://github.com/gradio-app/gradio/blob/f346118133866a4186b46ce9d3c7e3aab844577a/ui/packages/app/src/main.ts)

```html
<!DOCTYPE html>
<html lang="en">

<head>
  <script type="module" src="https://gradio.s3-us-west-2.amazonaws.com/3.4/gradio.js">
  </script>
</head>

<body>
  <gradio-app src="https://vk3lxhamsu45sdy6ne3kkyitiy0scbdm.lambda-url.eu-west-1.on.aws/"></gradio-app>
</body>

</html>
```