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