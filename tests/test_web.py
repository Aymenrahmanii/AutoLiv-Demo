import json

from fastapi.testclient import TestClient

from coding_buddy.benchmark import load_cases, load_codebook
from coding_buddy.reviewer import Finding
from coding_buddy.runner import run_benchmark, to_json
from coding_buddy.web.app import create_app


class StubReviewer:
    name = "stub-model"

    def __init__(self):
        self.calls = []

    def review(self, code, codebook):
        self.calls.append(codebook is not None)
        return [Finding(line=3, category="b", explanation="later"), Finding(line=1, category="a", explanation="first")]


def test_index_and_static_assets_are_served(tmp_path):
    client = TestClient(create_app(StubReviewer(), results_path=tmp_path / "none.json"))
    assert "Coding Buddy" in client.get("/").text
    assert client.get("/static/app.js").status_code == 200
    assert client.get("/static/app.css").status_code == 200


def test_benchmark_without_results_returns_cases_only(tmp_path):
    client = TestClient(create_app(StubReviewer(), results_path=tmp_path / "none.json"))
    data = client.get("/api/benchmark").json()
    assert len(data["cases"]) == 8 and data["results"] is None


def test_benchmark_payload_is_rescored_with_per_finding_verdicts(tmp_path):
    cases = load_cases()
    result = run_benchmark(StubReviewer(), cases, load_codebook())
    path = tmp_path / "results.json"
    path.write_text(json.dumps(to_json(result)))
    data = TestClient(create_app(StubReviewer(), results_path=path)).get("/api/benchmark").json()
    res = data["results"]
    assert res["model"] == "stub-model"
    assert set(res["summary"]) == {"without_codebook", "with_codebook"}
    finding = res["runs"]["with_codebook"][0][0]["findings"][0]
    assert {"hit", "explained", "line"} <= finding.keys()


def test_review_sorts_findings_and_passes_codebook_flag(tmp_path):
    stub = StubReviewer()
    client = TestClient(create_app(stub, results_path=tmp_path / "none.json"))
    body = client.post("/api/review", json={"code": "x <- 1", "use_codebook": False}).json()
    assert [f["line"] for f in body["findings"]] == [1, 3]
    assert body["model"] == "stub-model"
    client.post("/api/review", json={"code": "x <- 1", "use_codebook": True})
    assert stub.calls == [False, True]


def test_review_rejects_empty_script(tmp_path):
    client = TestClient(create_app(StubReviewer(), results_path=tmp_path / "none.json"))
    assert client.post("/api/review", json={"code": ""}).status_code == 422


def test_review_reports_provider_failure_as_502(tmp_path):
    class Failing:
        name = "x"

        def review(self, code, codebook):
            raise RuntimeError("quota exceeded")

    client = TestClient(create_app(Failing(), results_path=tmp_path / "none.json"))
    res = client.post("/api/review", json={"code": "x <- 1"})
    assert res.status_code == 502 and "quota exceeded" in res.json()["detail"]
