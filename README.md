# SoyCarepi Downloader API V1

Servidor backend para la APK SoyCarepi Downloader.

## Qué hace

- Recibe un enlace en `POST /api/resolve`.
- Detecta TikTok, Instagram, Facebook o YouTube.
- Usa `yt-dlp` para obtener los formatos que el proveedor disponible exponga.
- Devuelve metadatos y URLs temporales.
- Incluye `GET /api/health` para comprobar que el servidor está activo.
- Incluye `GET /api/download` como proxy de descarga sin guardar permanentemente el archivo.

## Arranque local

```bash
python -m pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Prueba:
`http://localhost:8000/api/health`

## Conectar la APK

En el HTML único, cambia:

```js
const API_BASE=localStorage.getItem("soycarepi_api")||"";
```

por:

```js
const API_BASE="https://TU-DOMINIO/api";
```

No uses una URL HTTP sin HTTPS en una APK distribuida.

## Importante

El servidor no incluye una base de datos ni una carpeta de almacenamiento permanente de vídeos.
La disponibilidad de cada plataforma depende del acceso que tenga `yt-dlp` en ese momento y de las respuestas del propio proveedor.
