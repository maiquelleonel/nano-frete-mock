import traceback
import httpx
from fastapi import FastAPI, Request
from starlette.responses import JSONResponse
from frete.calculator import calcular_frete

app = FastAPI(title="Nano Frete Mock Service")

BUGHUNTER_URL = "http://localhost:4318/v1/traces"

@app.middleware("http")
async def otel_error_reporter_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as exc:
        tb = traceback.format_exc()
        payload = {
            "resourceSpans": [{
                "resource": {
                    "attributes": [
                        {"key": "service.name", "value": {"stringValue": "nano-frete-mock"}},
                        {"key": "service.version", "value": {"stringValue": "master"}}
                    ]
                },
                "scopeSpans": [{
                    "spans": [{
                        "traceId": "4bf92f3577b34da6a3ce929d0e0e4736",
                        "spanId": "00f067aa0ba902b7",
                        "name": f"{request.method} {request.url.path}",
                        "status": {"code": 2},
                        "events": [{
                            "name": "exception",
                            "attributes": [
                                {"key": "exception.type", "value": {"stringValue": type(exc).__name__}},
                                {"key": "exception.message", "value": {"stringValue": str(exc)}},
                                {"key": "exception.stacktrace", "value": {"stringValue": tb}}
                            ]
                        }]
                    }]
                }]
            }]
        }
        try:
            async with httpx.AsyncClient(timeout=1.0) as client:
                await client.post(BUGHUNTER_URL, json=payload)
        except Exception:
            pass
        return JSONResponse(status_code=500, content={"error": "Internal Server Error", "detail": str(exc)})

@app.post("/api/v1/frete/calcular")
async def rota_calcular_frete(dados: dict):
    dimensoes = dados.get("dimensoes", {})
    peso_kg = dados.get("peso_kg", 1.0)
    cep_destino = dados.get("cep_destino", "01001-000")
    resultado = calcular_frete(dimensoes, peso_kg, cep_destino)
    return resultado
