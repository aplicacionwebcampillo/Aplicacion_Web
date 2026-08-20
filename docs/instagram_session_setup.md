# Configurar la sesión de Instagram para el importador de noticias

`scraper_instagram.py` ya no inicia sesión con usuario/contraseña por su
cuenta (eso es lo que Instagram detecta y bloquea). En su lugar reutiliza una
sesión ya autenticada a mano en un navegador real. Esto solo hay que
configurarlo una vez (y repetirlo si la sesión llega a expirar/cerrarse).

## 1. Inicia sesión en Instagram con Firefox

Abre Firefox y entra normalmente en instagram.com con la cuenta que quieras
usar para el scraping (puede ser una cuenta secundaria, no hace falta que
sea la del club). Resuelve a mano cualquier verificación que te pida.

## 2. Importa esa sesión con instaloader

En tu terminal, dentro del entorno virtual que ya tienes (`.venv_ig`):

```bash
source .venv_ig/bin/activate
pip install browser_cookie3
instaloader --load-cookies firefox
```

Si todo va bien verás algo como:

```
Cookies loaded successfully from firefox
<tu_usuario> has been successfully logged in.
Next time use --login=<tu_usuario> to reuse the same session.
```

Esto guarda la sesión en `~/.config/instaloader/session-<tu_usuario>`. Si
falla porque no encuentra cookies, cierra Firefox del todo y vuelve a
intentarlo (algunos sistemas bloquean la lectura de la base de datos de
cookies mientras el navegador está abierto).

## 3. Codifica el fichero de sesión para guardarlo como secret

```bash
base64 -w0 ~/.config/instaloader/session-<tu_usuario> > /tmp/session_b64.txt
cat /tmp/session_b64.txt
```

Copia toda la salida (una única línea larga).

## 4. Configura los secrets en GitHub

En **Settings → Secrets and variables → Actions** del repositorio:

- `IG_SESSION_FILE_B64`: pega el contenido de `/tmp/session_b64.txt`.
- `IG_SESSION_USERNAME`: tu usuario de Instagram (el mismo que salió en el
  paso 2, sin @).

Y borra los secrets antiguos que ya no se usan: `IG_LOGIN_USER`,
`IG_LOGIN_PASS` (el script ya no los lee, y además esa contraseña conviene
rotarla si no lo has hecho ya).

## 5. Limpieza local

```bash
rm /tmp/session_b64.txt
```

El fichero de sesión da acceso a esa cuenta de Instagram igual que la
contraseña — trátalo con el mismo cuidado, no lo subas al repositorio ni lo
compartas.

## 6. Probar

Lanza el workflow "Importar noticias desde Instagram" manualmente desde la
pestaña Actions. En el log deberías ver `[INFO] Sesión cargada para
<tu_usuario>` seguido de `[INFO] Perfil <usuario_del_club> obtenido
correctamente`.

## Cuándo repetir esto

Si la sesión caduca o Instagram la invalida, el script lo indicará con
`[AVISO] No se pudo cargar la sesión guardada...` y caerá a acceso anónimo.
Si pasa, repite los pasos 1-4 para generar una sesión nueva.
