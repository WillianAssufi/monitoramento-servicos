import time
import httpx

def verificar_url(url: str) -> dict:
    inicio = time.perf_counter()

    try:
        resposta = httpx.get(url, timeout=10, follow_redirects=True)
        tempo_resposta_ms = (time.perf_counter() - inicio) * 1000
        status = "UP" if 200 <= resposta.status_code < 300 else "DOWN"

        resultado = {"status" : status,
                     "tempo_resposta_ms": tempo_resposta_ms,
                     "codigo_http": resposta.status_code}
        
        return resultado
        
    except httpx.RequestError:
        resultado = {"status" : "DOWN",
                     "tempo_resposta_ms": None,
                     "codigo_http": None}
        
        return resultado