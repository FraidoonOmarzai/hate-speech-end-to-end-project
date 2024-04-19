from dataclasses import dataclass


@dataclass
# @dataclass decorator is used to automatically generate __init__, and other special methods based on class variables.
class DataIngestionArtifact:
    imbalanced_data_path: str
    raw_data_path: str


@dataclass
class DataTransformationArtifact:
    tansformed_df_path: str


@dataclass
class ModelTrainingArtifact:
    model_path: str
    X_test_path: str
    y_test_path: str