# hate-speech-end-to-end-project


- Git clone the repository and define the template of the project
```bash
git clone https://github.com/-----
touch template.py
python template.py
```

- define setup.py file

- install the new env and requirements.txt
```bash
conda create -n hate python=3.8 -y
conda activate hate
pip install -r requirements.txt
```

- define the logger
- define the exception handler

- Get the dataset and store in AWS S3 bucket
- Run the experiments.ipynb notebook in google colab and try different models
    - EDA
    - Feature Engineering
    - Model 0: Naive Bayes (baseline)
    - Model 1: A simple dense model
    - Model 2: LSTM
    - Model 3: GRU
    - Model 4: Bidirectonal RNN model
    - Model 5: Conv1D
    - Model 6: TensorFlow Hub Pretrained Sentence Encoder
    - Model 7: LSTM (second method)

```bash
## Workflows

- update the constants
- updata the artifact_entity
- update the config_entity
- update the components
- update the pipeline
- update the dvc.yaml
```

- **Data Ingestion**
    - add s3_operations.py for uploading and downloading files from s3 bucket 
    - we need to run the below command which allows to configure AWS credentials and settings 
    ```bash
    aws configure
    ```
    - follow the above workflows to get the data from the S3 bucket

- **Data Transformation**
    - Performing data transformation operations such:
        - Data loading (df1,df2)
        - Concatenation of dataframes(df1,df2)
        - Data Cleaning
        - Saving transformed data to a file
    ```bash
    ## Text Preprocessing
    - Converting to lower case
    - Tokenising
    - Removing stop words
    - Words stemming
    - Removing punctuation
    - Stripping out html tags
    ```
- **Model Training**
    - store the the model architecture in `ml/model.py` 
    - facing with error while tokenizing the raw_data.csv so i just trained the model only on imbalance_data.csv


- **Model Evaluation**

- **Model Pushing**
    - our goal is to push the best model to AWS cloud and store in S3 bucket


- **Prediction Pipeline**
    - adding code to `pipepline/prediction_pipeline.py`
    - add code to app.py


- **Docker**
    - define the docker file
    - bulid and run the docker image
    ```bash
    docker build -t nlp-app .  # build docker image
    docker ps   
    docker images
    docker run -p 8080:8080 nlp-app
    ```

- **Deploy docker image to docker hub**
    - we will use circleci to deploy the docker image


- **Deploy to AWS** =>erorr!
    - In this project i will be using circleci for CI/CD
    - Setup circleci
    - ASW Setup
        - create IAM
        - create EC2 -> virtual machine
        - create ECR -> save docker image in aws
    **Steps:**
    - for circleci setup go to the circleci_setup.sh file for instructions and run all the commands in ec2
    - create .circleci dir and add config.yaml file to it
    - add them inside environment variables in circileci
        - AWS_ACCESS_KEY_ID
        - AWS_SECRET_ACCESS_KEY
        - AWS_REGION
        - AWS_ECR_REGISTRY_ID
```bash
#config.yml
version: 2.1
orbs:
  aws-ecr: circleci/aws-ecr@8.2.1
  aws-cli: circleci/aws-cli@3.1.4
jobs:
  continuous-integration:
    docker:
      - image: cimg/base:stable
    resource_class: medium
    steps:
      - setup_remote_docker:
          version: 20.10.14
          docker_layer_caching: true

      - aws-ecr/build-and-push-image:
          create-repo: true
          dockerfile: Dockerfile
          path: .
          platform: linux/amd64
          push-image: true
          region: '${AWS_REGION}'
          repo: demo
          registry-id: AWS_ECR_REGISTRY_ID
          repo-scan-on-push: true
          tag: latest

  continuous-delivery:
    machine: true
    resource_class: large
    steps:
      - aws-cli/setup

      - run:
          name: auth to aws ecr
          command: aws ecr get-login-password --region eu-west-2 | docker login --username AWS --password-stdin 851725628730.dkr.ecr.eu-west-2.amazonaws.com
          
      - run:
          name: build
          command: docker build -t hatespeech


      - run:
          name: rename the image
          command: docker tag hatespeech:latest 851725628730.dkr.ecr.eu-west-2.amazonaws.com/hatespeech:latest
    

      - run:
          name: push the image
          command: docker push hatespeech:latest 851725628730.dkr.ecr.eu-west-2.amazonaws.com/hatespeech:latest

      - run:
          name: pull image from private repository
          command: docker pull 851725628730.dkr.ecr.eu-west-2.amazonaws.com/hatespeech:latest
          
      
      - run:
          name: run image
          command: docker run -d -p 8080:8080 851725628730.dkr.ecr.eu-west-2.amazonaws.com/hatespeech:latest
workflows:
  CICD:
    jobs:
      - continuous-integration
      - continuous-delivery:
          requires:
          - continuous-integration

```    