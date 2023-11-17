# Use Generative AI to Build a DevSecOps Chatbot

## Introduction
----
This repository provides guidance and assets to build a DevSecOps Chatbot. This chatbot is built with the context of a scenario of a fictional company that has DevSecOps challenges. 

This repository is the companion to the AWS Workshop: Use Generative AI to build a DevSecOps Chatbot. 

The AWS Workshop Use Generative AI to build a DevSecOps Chatbot is available [here.](https://studio.us-east-1.prod.workshops.aws/preview/75a20314-5e15-4246-9352-3643d9dafc43/builds/8db6ec08-b64e-48c0-ba11-6f571975ecde/en-US)

In this workshop, we will demonstrate how you can create a chatbot using AI-powered AWS services that will help engineers solve common challenges like how to securely store your application’s secrets or how to create a new Disaster Recovery environment. At the end of this Workshop you will understand how to build a Chatbot that can help you with DevSecOps queries as well as other use cases. You will understand how you can use several AWS services and easily integrate them in order to build this Chatbot and use Retrieval Augmented Generation (RAG) to make the Chatbot specific to different use cases.

### What is the required level of knowledge?
----
You don't need to be an expert to take this workshop. If you want to figure out how to build the Chatbot without using the step-by-step guide, it will help if you have an understanding of the AWS Console, experience with the Linux Operating System as well as coding with Python. You'll also need know how to use some AWS Services that are used. However, there is a Step-By-Step guide (under Modules) that assumes little to no knowledge of AWS - so you can follow that to build a Chatbot even if you have little to no prior experience.

### Will this cost me anything?
----
This repository is licensed under the MIT-0 License and is available at no cost. The Workshop Studio environment varies in cost depending on circumstance. If you are at an AWS event and using a Sandbox environment, you will incur no cost. If you use your own AWS Account, there will be some charges depending on how long the services are operational. Make sure you clean up your resources at the end to avoid unnecessary charges.

## Abstract
----
Welcome to the Repository for the AWS workshop for Using Generative AI to Build a DevSecOps Chatbot! Here you will find the assets that pair with the hands-on content in Workshop Studio aimed at helping you gain an understanding of GenAI services that will help you build a Chatbot. Although you can use the same (or similar) services and tools to build a Chatbot aimed at all kinds of use cases, this workshop specifically aims to build a Chatbot for DevSecOps engineers.

In this Workshop, we will be going through a scenario of a fictional company that has DevSecOps challenges. 

This Workshop uses a store of documents to train a chatbot to address the following concerns: 

    1. Easily find potential issues in code via Static application Security Testing (SAST) and Dyanamic Analysis Security Testing (DAST)
    2. Engineers would like to identify potential software vulnerabilities across their software applications
    3. Improve traceability, auditabilty and visiblity
    4. Develop the right Threat Model
    5. Develop the right kind of security policies
    6. Improve Infrastructure as Code (Iaac) Security
    7. Enforce security in the pipeline
    8. DevSecOps leaders would like a way to control the quality of the solutions that are built

**_You can easily build the DevSecOps Chatbot with the assets in this repository and train the chatbot with the documents in the Workshop. These same techniques can be used to customize a chatbot for your own workflows and organization._**

### Architecture
----
![Proposed Architecture](images/DevSecOps_Transparent.png)


## Using this Repository
----

### Step 1:
----

The first step of utilizing this repo is performing a git clone of the repository.

```
git clone https://github.com/aws-samples/generative-ai-to-build-a-devsecops-chatbot/
```

After cloning the repo onto your local machine, open it up in your favorite code editor.The file structure of this repo is broken into 3 key files, the app.py file, the kendra_bedrock_query.py file, and the requirements.txt. The app.py file houses the frontend application (a streamlit app). The kendra_bedrock_query.py file houses the logic of the application, including the Kendra Retrieve API calls and Amazon Bedrock API invocations. The requirements.txt file contains all necessary dependencies for this sample application to work.

### Step 2:
----

Move into the folder just created with the code so that it becomes the current folder:

```
cd generative-ai-to-build-a-devsecops-chatbot
```

### Step 3:
----

Retrieve the Kendra Index ID generated in the Workshop after creating the Amazon Kendra Index and use it in this command (replacing the x's, keep the quotes). This provides our application with the Kendra Index ID that we created earlier so that it knows where to go for the data needed. In turn, Kendra will of course use the Data Source you created to use the documents in the S3 bucket. The Kendra Index ID is obtained in Workshop Studio. 

__The AWS Workshop Use Generative AI to build a DevSecOps Chatbot is available [here.](https://studio.us-east-1.prod.workshops.aws/preview/75a20314-5e15-4246-9352-3643d9dafc43/builds/8db6ec08-b64e-48c0-ba11-6f571975ecde/en-US)__

```
export KENDRA_INDEX_ID="xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
```

### Optional Step:
----

Step 4 outlines how to install the requirements for this repository in your Python environment via pip, the Python package manager. If you do not want these packages installed into your main installation, please consider using a virtual environment. 

To set up a python virtual environment in the root directory of the repository, and ensure that you are using Python 3.9, run the following commands:

```
pip install virtualenv
python3.9 -m venv venv
```
The virtual environment will be extremely useful when you begin installing the requirements. If you need more clarification on the creation of the virtual environment please refer to this [blog](https://www.freecodecamp.org/news/how-to-setup-virtual-environments-in-python/). After the virtual environment is created, ensure that it is activated, following the activation steps of the virtual environment tool you are using. 
Likely:

```
cd venv
cd bin
source activate
cd ../../
```

After your virtual environment has been created and activated, you can install all the requirements found in the requirements.txt file


### Step 4:
----

Here you'll use pip, the Python package manager, to install a set of programs that are listed in the requirements.txt text file. If you're curious about the contents of this file, feel free to look through it and/or the rest of the code in the folder

```
pip install -r requirements.txt
```

### Step 5:
----

Finally, after installing the necessary components, you will now run the command for Streamlit, an open-source app framework that allows you to turn data scripts into shareable web apps in minutes, and all using pure Python. This will let you test your Chatbot easily before deploying it to an actual server and making it public by running the app.py file within the Streamlit framework.

```
streamlit run app.py titan
```

## License
----
This library is licensed under the MIT-0 License. See the LICENSE file.
