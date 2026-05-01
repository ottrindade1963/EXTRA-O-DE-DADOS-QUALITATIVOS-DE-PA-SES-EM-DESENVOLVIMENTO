"""Configurações centrais para treino e avaliação dos modelos."""

import os

# ─── Caminhos ───
# Os ficheiros estão diretamente na raiz do repositório
BASE_DIR = os.getcwd()
OUTPUT_DIR = os.path.join(BASE_DIR, "resultados_modelos")

# ─── Datasets (os ficheiros estão na raiz com prefixo {dataset}_) ───
DATASETS = ["inner", "left", "outer"]

# ─── Target ───
TARGET = "pib_per_capita_ppc"

# ─── Hiperparâmetros LSTM ───
LSTM_CONFIG = {
    "units_1": 64,
    "units_2": 32,
    "dropout": 0.2,
    "epochs": 100,
    "batch_size": 32,
    "patience": 15,
    "learning_rate": 0.001,
}

# ─── Hiperparâmetros Random Forest ───
RF_CONFIG = {
    "n_estimators": 200,
    "max_depth": 15,
    "min_samples_split": 5,
    "min_samples_leaf": 2,
    "random_state": 42,
    "n_jobs": -1,
}

# ─── Hiperparâmetros XGBoost ───
XGB_CONFIG = {
    "n_estimators": 300,
    "max_depth": 8,
    "learning_rate": 0.05,
    "subsample": 0.8,
    "colsample_bytree": 0.8,
    "reg_alpha": 0.1,
    "reg_lambda": 1.0,
    "random_state": 42,
}

# ─── Hiperparâmetros SARIMAX ───
SARIMAX_CONFIG = {
    "order": (1, 1, 1),
    "seasonal_order": (1, 0, 1, 5),
    "max_paises": 10,
}

# ─── Hiperparâmetros TFT ───
TFT_CONFIG = {
    "hidden_size": 32,
    "attention_head_size": 2,
    "dropout": 0.1,
    "hidden_continuous_size": 16,
    "max_epochs": 50,
    "batch_size": 64,
    "learning_rate": 0.01,
    "patience": 10,
}

# ─── Split ───
TRAIN_RATIO = 0.8
RANDOM_STATE = 42
