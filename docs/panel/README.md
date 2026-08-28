# Panel Campillo CF

Web sencilla para lanzar los workflows de GitHub Actions desde el móvil, sin
pasar por la app de GitHub.

## Puesta en marcha (una sola vez)

1. En el repositorio, ve a **Settings → Pages**.
2. En "Build and deployment" → **Source**, elige **Deploy from a branch**.
3. **Branch**: `main`, carpeta **`/docs`**. Guarda.
4. Espera 1-2 minutos. La web quedará publicada en:
   `https://aplicacionwebcampillo.github.io/Aplicacion_Web/panel/`

## Token de GitHub

La web necesita un token para poder lanzar workflows en tu nombre:

1. En GitHub: **Settings** (de tu cuenta, no del repo) → **Developer settings**
   → **Personal access tokens** → **Fine-grained tokens** → **Generate new token**.
2. **Repository access**: solo este repositorio (`Aplicacion_Web`).
3. **Permissions** → **Actions**: **Read and write**. El resto, sin acceso.
4. Genera el token y pégalo en la web (campo "Token de acceso de GitHub").

El token se guarda solo en el navegador de tu móvil (localStorage) y solo se
usa para hablar con `api.github.com`. Si cambias de móvil o borras datos del
navegador, tendrás que volver a pegarlo.

## Añadir a la pantalla de inicio (Android)

Abre la web en Chrome → menú (⋮) → **Añadir a pantalla de inicio**. Quedará
como un icono más, y se abre en su propia ventana.
