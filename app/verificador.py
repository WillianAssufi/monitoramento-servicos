import time
import httpx
from playwright.sync_api import sync_playwright

def verificar_url(url: str) -> dict:
    inicio = time.perf_counter()

    try:
        resposta = httpx.get(url, timeout=10, follow_redirects=True)
        tempo_resposta_ms = round((time.perf_counter() - inicio) * 1000)
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

def verificar_playwright(url: str) -> dict:
    inicio = time.perf_counter()
    try:
        with sync_playwright() as playw:
            navegador = playw.chromium.launch()
            try:
                pagina = navegador.new_page()
                resposta = pagina.goto(url, timeout=15000)
                codigo = resposta.status if resposta else None
                titulo = pagina.title()
                if not titulo:
                    raise Exception("página sem título")
            finally:
                navegador.close()

            tempo_resposta_ms = round((time.perf_counter() - inicio) * 1000)
        return {
            "status": "UP",
            "tempo_resposta_ms": tempo_resposta_ms,
            "codigo_http": codigo,
        }

    except Exception:
        return {
            "status": "DOWN",
            "tempo_resposta_ms": None,
            "codigo_http": None,
        }