import unittest

from app import app


class KnnAppTest(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_health_endpoint(self):
        response = self.client.get("/api/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["status"], "ok")

    def test_client_prediction(self):
        response = self.client.post(
            "/api/predict",
            json={
                "practice": "client",
                "attention": 8,
                "responseTime": 12,
                "k": 3,
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["prediction"], "Satisfecho")
        self.assertEqual(len(response.json["neighbors"]), 3)

    def test_investment_prediction(self):
        response = self.client.post(
            "/api/predict",
            json={
                "practice": "investment",
                "profit": 75,
                "risk": 25,
                "k": 3,
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["prediction"], "Invierte")

    def test_invalid_range(self):
        response = self.client.post(
            "/api/predict",
            json={
                "practice": "client",
                "attention": 99,
                "responseTime": 12,
                "k": 3,
            },
        )
        self.assertEqual(response.status_code, 400)

    def test_plot_endpoint(self):
        response = self.client.get(
            "/api/plot/client?x=8&y=12&prediction=Satisfecho"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, "image/png")


if __name__ == "__main__":
    unittest.main()
