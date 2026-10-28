# Backend de la lista de compras

API sencilla con FastAPI y PostgreSQL para una lista compartida. No incluye cuentas ni autenticación; úsala localmente o en una red privada.

## Estado en este equipo

La base `compras` ya existe en el PostgreSQL instalado en `127.0.0.1:5432` y tiene aplicada la migración `0001`. Es independiente de cualquier otra base del servidor. El archivo `.env` guarda la URL completa de conexión, incluido el usuario y la contraseña, y está excluido de Git.

La carpeta ignorada `.postgres-data/` pertenece a una instancia provisional ya detenida en `5433`; la API actual no la utiliza.

Para iniciar la API desde esta carpeta con el Python del entorno virtual:

```powershell
.\.venv\Scripts\python.exe run.py
```

`run.py` usa la conexión de `.env`, aplica las migraciones pendientes y arranca Uvicorn. La API estará en `http://127.0.0.1:8000` y la documentación interactiva en `http://127.0.0.1:8000/docs`. Detén Uvicorn con `Ctrl+C`. Si tu editor ya tiene seleccionado `.venv` como intérprete, también puedes ejecutar `python run.py`.

## Preparar en otro equipo

Requiere Python 3.11 o posterior y PostgreSQL. Crea una base llamada `compras` y copia `.env.example` como `.env`; sustituye `usuario` y `contrasena` por las credenciales de tu base y ajusta host, puerto o nombre si hace falta. Luego instala las dependencias:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e ".[dev]"
Copy-Item .env.example .env
.\.venv\Scripts\python.exe run.py
```

`.env` está excluido de Git para que las credenciales locales no entren al repositorio.

## Rutas

- `GET /items`: lista todos los elementos por fecha de creación.
- `POST /items`: agrega un elemento (`201`).
- `PATCH /items/{id}`: cambia los campos enviados, incluido `is_purchased`.
- `DELETE /items/{id}`: elimina definitivamente (`204`).

Ejemplo de creación:

```json
{
  "name": "Arroz",
  "quantity": "0.5",
  "unit": "kg",
  "note": "Integral",
  "unit_price": "12.50"
}
```

`quantity` vale `1` por defecto. `unit`, `note` y `unit_price` son opcionales. Los precios están en BOB y `total` se calcula como cantidad por precio unitario; es `null` si falta el precio. Se permiten nombres repetidos. Los importes y cantidades se serializan como cadenas decimales para conservar precisión.

## Pruebas

```powershell
.\.venv\Scripts\python.exe -m pytest
```

Las pruebas usan SQLite en memoria para verificar las rutas. La migración se aplicó y verificó además en el PostgreSQL local.

