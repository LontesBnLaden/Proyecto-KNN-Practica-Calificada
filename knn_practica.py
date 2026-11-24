from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler


CLIENT_COLUMNS = ["Puntaje de atención", "Tiempo de respuesta"]
INVESTMENT_COLUMNS = ["Beneficio esperado", "Riesgo percibido"]


def build_client_dataset() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "Puntaje de atención": [9, 8, 7, 9, 6, 4, 3, 5],
            "Tiempo de respuesta": [8, 12, 18, 15, 25, 30, 40, 28],
            "Resultado": [
                "Satisfecho",
                "Satisfecho",
                "Satisfecho",
                "Satisfecho",
                "No satisfecho",
                "No satisfecho",
                "No satisfecho",
                "No satisfecho",
            ],
        }
    )


def build_investment_dataset() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "Beneficio esperado": [85, 78, 90, 68, 55, 40, 25, 48],
            "Riesgo percibido": [18, 25, 30, 35, 75, 82, 90, 68],
            "Resultado": [
                "Invierte",
                "Invierte",
                "Invierte",
                "Invierte",
                "No invierte",
                "No invierte",
                "No invierte",
                "No invierte",
            ],
        }
    )


def predict(
    dataframe: pd.DataFrame,
    feature_columns: list[str],
    point: list[float],
    k: int,
) -> str:
    features = dataframe[feature_columns]
    labels = dataframe["Resultado"]

    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(features)
    scaled_point = scaler.transform(
        pd.DataFrame([point], columns=feature_columns)
    )

    model = KNeighborsClassifier(n_neighbors=k)
    model.fit(scaled_features, labels)
    return str(model.predict(scaled_point)[0])


def save_scatter(
    dataframe: pd.DataFrame,
    feature_columns: list[str],
    point: list[float],
    prediction: str,
    output_path: Path,
) -> None:
    fig, axis = plt.subplots(figsize=(8, 5))

    for label in dataframe["Resultado"].unique():
        rows = dataframe[dataframe["Resultado"] == label]
        axis.scatter(
            rows[feature_columns[0]],
            rows[feature_columns[1]],
            label=label,
            s=90,
        )

    axis.scatter(
        point[0],
        point[1],
        marker="*",
        s=240,
        color="black",
        label=f"Nuevo caso: {prediction}",
    )
    axis.set_xlabel(feature_columns[0])
    axis.set_ylabel(feature_columns[1])
    axis.set_title("Clasificación con el algoritmo KNN")
    axis.grid(True, alpha=0.3)
    axis.legend()
    fig.tight_layout()
    fig.savefig(output_path, dpi=150)
    plt.close(fig)


def run_practice(k: int) -> None:
    output_directory = Path("salidas")
    output_directory.mkdir(exist_ok=True)

    client_point = [8, 12]
    client_dataframe = build_client_dataset()
    client_prediction = predict(
        client_dataframe,
        CLIENT_COLUMNS,
        client_point,
        k,
    )
    print(
        f"Práctica 1 - Atención={client_point[0]}, "
        f"respuesta={client_point[1]} minutos -> {client_prediction}"
    )
    save_scatter(
        client_dataframe,
        CLIENT_COLUMNS,
        client_point,
        client_prediction,
        output_directory / "practica_1.png",
    )

    investment_point = [75, 25]
    investment_dataframe = build_investment_dataset()
    investment_prediction = predict(
        investment_dataframe,
        INVESTMENT_COLUMNS,
        investment_point,
        k,
    )
    print(
        f"Práctica 2 - Beneficio={investment_point[0]}%, "
        f"riesgo={investment_point[1]} -> {investment_prediction}"
    )
    save_scatter(
        investment_dataframe,
        INVESTMENT_COLUMNS,
        investment_point,
        investment_prediction,
        output_directory / "practica_2.png",
    )

    print(f"Gráficas guardadas en: {output_directory.resolve()}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Prácticas calificadas de clasificación con KNN"
    )
    parser.add_argument(
        "--k",
        type=int,
        choices=range(1, 8),
        default=3,
        help="Cantidad de vecinos (1-7)",
    )
    arguments = parser.parse_args()
    run_practice(arguments.k)


if __name__ == "__main__":
    main()
