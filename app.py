from io import BytesIO

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
from flask import Flask, jsonify, send_file, send_from_directory
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler


app = Flask(__name__)


CLIENT_COLUMNS = ["Puntaje de atención", "Tiempo de respuesta"]
INVESTMENT_COLUMNS = ["Beneficio esperado", "Riesgo percibido"]


def get_client_dataset() -> pd.DataFrame:
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


def get_investment_dataset() -> pd.DataFrame:
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


def predict(dataframe: pd.DataFrame, feature_columns: list[str],
            point: list[float], k: int) -> dict:
    scaler = StandardScaler()
    features = dataframe[feature_columns]
    scaled_features = scaler.fit_transform(features)
    scaled_point = scaler.transform(
        pd.DataFrame([point], columns=feature_columns)
    )

    model = KNeighborsClassifier(n_neighbors=k)
    model.fit(scaled_features, dataframe["Resultado"])
    prediction = str(model.predict(scaled_point)[0])
    probabilities = model.predict_proba(scaled_point)[0]
    probability_by_label = {
        str(label): round(float(probability) * 100, 1)
        for label, probability in zip(model.classes_, probabilities)
    }
    counts = dataframe["Resultado"].value_counts()
    neighbor_distances, neighbor_indices = model.kneighbors(scaled_point)

    neighbors = []
    for distance, index in zip(
        neighbor_distances[0], neighbor_indices[0]
    ):
        neighbors.append({
            "values": [
                float(dataframe.iloc[index][column])
                for column in feature_columns
            ],
            "label": str(dataframe.iloc[index]["Resultado"]),
            "distance": round(float(distance), 4),
        })

    return {
        "prediction": prediction,
        "confidence": probability_by_label[prediction],
        "probabilities": probability_by_label,
        "neighbors": neighbors,
        "training_accuracy": round(
            float(model.score(scaled_features, dataframe["Resultado"])) * 100,
            1,
        ),
        "dataset_size": int(len(dataframe)),
        "class_counts": {
            str(label): int(count) for label, count in counts.items()
        },
    }


@app.route("/api/health")
def health():
    return jsonify({
        "status": "ok",
        "libraries": ["pandas", "scikit-learn", "matplotlib"],
    })


@app.route("/")
def index():
    return send_from_directory(app.root_path, "index.html")


@app.route("/css/<path:filename>")
def styles(filename):
    return send_from_directory(app.root_path, f"css/{filename}")


@app.route("/js/<path:filename>")
def scripts(filename):
    return send_from_directory(app.root_path, f"js/{filename}")


@app.route("/api/predict", methods=["POST"])
def api_predict():
    from flask import request

    body = request.get_json(silent=True) or {}
    practice = body.get("practice")
    try:
        k = int(body.get("k", 3))
    except (TypeError, ValueError):
        return jsonify({"error": "El valor de K no es válido"}), 400

    if not 1 <= k <= 7:
        return jsonify({"error": "K debe estar entre 1 y 7"}), 400

    try:
        if practice == "client":
            attention = float(body["attention"])
            response_time = float(body["responseTime"])
            dataframe = get_client_dataset()
            point = [attention, response_time]
            columns = CLIENT_COLUMNS
        elif practice == "investment":
            profit = float(body["profit"])
            risk = float(body["risk"])
            dataframe = get_investment_dataset()
            point = [profit, risk]
            columns = INVESTMENT_COLUMNS
        else:
            return jsonify({"error": "Práctica no válida"}), 400
    except (KeyError, TypeError, ValueError):
        return jsonify({"error": "Datos de entrada no válidos"}), 400

    if practice == "client":
        if not 1 <= point[0] <= 10:
            return jsonify({"error": "La atención debe estar entre 1 y 10"}), 400
        if not 0 <= point[1] <= 60:
            return jsonify({"error": "El tiempo debe estar entre 0 y 60"}), 400
    else:
        if not 0 <= point[0] <= 100:
            return jsonify({"error": "El beneficio debe estar entre 0 y 100"}), 400
        if not 0 <= point[1] <= 100:
            return jsonify({"error": "El riesgo debe estar entre 0 y 100"}), 400

    result = predict(dataframe, columns, point, k)
    return jsonify({"k": k, "point": point, **result})


@app.route("/api/plot/<practice>")
def api_plot(practice):
    from flask import request

    if practice == "client":
        dataframe = get_client_dataset()
        columns = CLIENT_COLUMNS
    elif practice == "investment":
        dataframe = get_investment_dataset()
        columns = INVESTMENT_COLUMNS
    else:
        return "Práctica no válida", 404

    figure, axis = plt.subplots(figsize=(8, 5))
    for label in dataframe["Resultado"].unique():
        rows = dataframe[dataframe["Resultado"] == label]
        axis.scatter(
            rows[columns[0]],
            rows[columns[1]],
            label=label,
            s=80,
        )

    axis.set_xlabel(columns[0])
    axis.set_ylabel(columns[1])
    axis.set_title("Datos de entrenamiento - KNN")
    axis.grid(True, alpha=0.3)
    axis.legend()

    try:
        point_x = float(request.args.get("x"))
        point_y = float(request.args.get("y"))
        prediction = str(request.args.get("prediction", "Nuevo caso"))
        axis.scatter(
            [point_x],
            [point_y],
            marker="*",
            s=220,
            color="black",
            edgecolor="white",
            linewidth=1.5,
            label=f"{prediction}",
            zorder=5,
        )
        axis.legend()
    except (TypeError, ValueError):
        pass
    figure.tight_layout()

    output = BytesIO()
    figure.savefig(output, format="png", dpi=150)
    plt.close(figure)
    output.seek(0)
    return send_file(output, mimetype="image/png")


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5050, debug=False)
