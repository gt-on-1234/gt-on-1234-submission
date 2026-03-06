"""
This module contains integration tests for the examples in the README.

You will need to have the server running locally at `http://localhost:8080` for these tests to pass,
which can be done by:

```bash
docker compose up --build
```

See `README.md` for more details.
"""

import functools

import httpx
import pytest

HOSTNAME = "http://localhost:8080"


class UnsortedList(list):
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, list):
            return NotImplemented
        return sorted(self) == sorted(other)


approx = functools.partial(pytest.approx, abs=1e-4)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ["url", "request_payload", "expected_body"],
    [
        pytest.param(
            "/event-impact",
            {
                "impactedByEvent": ["ud", "ax", "ih"],
                "trackedSuppliers": ["wu", "wr"],
                "minImpact": 0.2,
            },
            {"affectedSuppliers": UnsortedList(["wu"])},
            id="event-impact-working-example",
        ),
        pytest.param(
            "/event-impact",
            {
                "impactedByEvent": ["ud", "ax", "ih"],
                "trackedSuppliers": ["nh", "os", "rg", "wu", "wr"],
                "minImpact": 0.1,
            },
            {"affectedSuppliers": UnsortedList(["nh", "os", "rg", "wu", "wr"])},
            id="event-impact-example-1",
        ),
        pytest.param(
            "/event-impact",
            {
                "impactedByEvent": ["ud", "ax", "ih"],
                "trackedSuppliers": ["nh", "os", "rg", "wu", "wr"],
                "minImpact": 0.3,
            },
            {"affectedSuppliers": UnsortedList(["nh", "os", "rg"])},
            id="event-impact-example-2",
        ),
        pytest.param(
            "/event-impact",
            {
                "impactedByEvent": ["ud", "ax", "ih"],
                "trackedSuppliers": ["nh", "os", "rg", "wu", "wr"],
                "minImpact": 0.7,
            },
            {"affectedSuppliers": UnsortedList(["nh", "os"])},
            id="event-impact-example-3",
        ),
        pytest.param(
            "/event-impact",
            {
                "impactedByEvent": ["ta", "xd", "rc", "he"],
                "trackedSuppliers": ["rg", "os", "nh", "ba", "ud", "sn"],
                "minImpact": 0.4,
            },
            {"affectedSuppliers": UnsortedList(["rg", "os", "nh", "ba"])},
            # id="highest-impact-example-4",
            id="event-impact-example-4",
        ),
        pytest.param(
            "/event-impact",
            {
                "impactedByEvent": ["ta", "xd", "rc", "he"],
                "trackedSuppliers": ["rg", "os", "nh", "ba", "ud", "sn"],
                "minImpact": 0.6,
            },
            {"affectedSuppliers": UnsortedList(["os", "nh"])},
            # id="highest-impact-example-5",
            id="event-impact-example-5",
        ),
        pytest.param(
            "/highest-impact",
            {
                "impactedByEvent": ["ud", "ax", "ih"],
                "trackedSuppliers": ["wu", "wr", "os"],
            },
            {
                "highestImpacts": {
                    "wu": {
                        "path": ["ud", "vx", "hq", "wu"],
                        "impact": approx(0.251559),
                    },
                    "wr": {
                        "path": ["ud", "vx", "hq", "wr"],
                        "impact": approx(0.175329),
                    },
                    "os": {
                        "path": ["ax", "xd", "cg", "os"],
                        "impact": approx(0.792396),
                    },
                }
            },
            id="highest-impact-working-example",
        ),
        pytest.param(
            "/highest-impact",
            {
                "impactedByEvent": ["ud", "ax", "ih"],
                "trackedSuppliers": ["nh", "os", "rg", "wu", "wr"],
            },
            {
                "highestImpacts": {
                    "nh": {
                        "path": ["ax", "xd", "cg", "nh"],
                        "impact": approx(0.719532),
                    },
                    "os": {
                        "path": ["ax", "xd", "cg", "os"],
                        "impact": approx(0.792396),
                    },
                    "rg": {
                        "path": ["ud", "vx", "hq", "rg"],
                        "impact": approx(0.312543),
                    },
                    "wu": {
                        "path": ["ud", "vx", "hq", "wu"],
                        "impact": approx(0.251559),
                    },
                    "wr": {
                        "path": ["ud", "vx", "hq", "wr"],
                        "impact": approx(0.175329),
                    },
                }
            },
            id="highest-impact-example-1",
        ),
        pytest.param(
            "/highest-impact",
            {
                "impactedByEvent": ["ta", "xd", "rc", "he"],
                "trackedSuppliers": ["rg", "os", "nh", "ba", "ud", "sn"],
            },
            {
                "highestImpacts": {
                    "os": {"path": ["xd", "cg", "os"], "impact": approx(0.8004)},
                    "rg": {"path": ["ta", "rg"], "impact": approx(0.4)},
                    "nh": {"path": ["xd", "cg", "nh"], "impact": approx(0.7268)},
                    "ba": {"path": ["he", "ba"], "impact": approx(0.46)},
                }
            },
            id="highest-impact-example-2",
        ),
        pytest.param(
            "/highest-impact",
            {
                "impactedByEvent": ["ta", "sn", "he"],
                "trackedSuppliers": ["rg", "wu", "nh", "he"],
            },
            {
                "highestImpacts": {
                    "rg": {"path": ["ta", "rg"], "impact": approx(0.4)},
                    "wu": {"path": ["sn", "ba", "wu"], "impact": approx(0.147)},
                    "nh": {
                        "path": ["he", "xd", "cg", "nh"],
                        "impact": approx(0.712264),
                    },
                    "he": {"path": ["he"], "impact": approx(1.0)},
                }
            },
            id="highest-impact-example-3",
        ),
    ],
)
async def test_readme_examples(
    url: str,
    request_payload: dict,
    expected_body: dict,
) -> None:
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{HOSTNAME}{url}", json=request_payload)
        assert response.status_code == 200
        assert response.json() == expected_body
