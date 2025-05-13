import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from sqlalchemy.orm import Session
from app.models.jugador import Jugador
from app.models.equipo import Equipo

# Conexión a la base de datos usando SQLAlchemy
from app.database import SessionLocal  # Aquí importamos SessionLocal

# Configuración Selenium para Firefox (modo headless)
firefox_options = FirefoxOptions()
firefox_options.add_argument("--headless")
driver = webdriver.Firefox(options=firefox_options)

# Establecer conexión a la base de datos
db: Session = SessionLocal()

# URL del club Campillo del Río CF
URL_CLUB = "https://www.rfaf.es/pnfg/NPcd/NFG_VerClub?cod_primaria=1000118&codigo_club=28701965"
driver.get(URL_CLUB)
time.sleep(3)

# Ir a la pestaña "Equipos"
equipos_link = driver.find_element(By.LINK_TEXT, "Equipos")
equipos_link.click()
time.sleep(3)

# Obtener la tabla de equipos
equipos = driver.find_elements(By.CSS_SELECTOR, "table tbody tr")

for eq in equipos:
    try:
        categoria = eq.find_element(By.CSS_SELECTOR, "td:nth-child(2)").text
        enlace_equipo = eq.find_element(By.TAG_NAME, "a").get_attribute("href")

        # Insertar equipo
        equipo_db = Equipo(categoria=categoria, num_jugadores=0)
        db.add(equipo_db)
        db.commit()
        db.refresh(equipo_db)  # Obtén el id del equipo después de insertarlo
        id_equipo = equipo_db.id_equipo

        # Ir a la página del equipo
        driver.get(enlace_equipo)
        time.sleep(3)

        # Intentar ir a la plantilla del equipo
        try:
            plantilla_link = driver.find_element(By.LINK_TEXT, "Plantilla")
            plantilla_link.click()
            time.sleep(3)

            jugadores = driver.find_elements(By.CSS_SELECTOR, "table tbody tr")
            num_jugadores = 0

            for fila in jugadores:
                celdas = fila.find_elements(By.TAG_NAME, "td")
                if len(celdas) >= 4:
                    nombre = celdas[0].text
                    dorsal = int(celdas[1].text)
                    posicion = celdas[2].text
                    fecha_str = celdas[3].text
                    try:
                        fecha_nacimiento = fecha_str
                    except:
                        fecha_nacimiento = "2000-01-01"  # Fallback

                    # Insertar jugador
                    jugador_db = Jugador(
                        id_equipo=id_equipo, nombre=nombre, posicion=posicion,
                        fecha_nacimiento=fecha_nacimiento, dorsal=dorsal
                    )
                    db.add(jugador_db)
                    num_jugadores += 1

            # Actualizar número de jugadores en el equipo
            equipo_db.num_jugadores = num_jugadores
            db.commit()

        except Exception as e:
            print(f"⚠️ No se pudo acceder a la plantilla de '{categoria}': {e}")

        # Volver a la lista de equipos
        driver.get(URL_CLUB)
        time.sleep(2)
        equipos_link = driver.find_element(By.LINK_TEXT, "Equipos")
        equipos_link.click()
        time.sleep(2)

    except Exception as e:
        print(f"❌ Error procesando un equipo: {e}")
        continue

# Finalizar
db.close()
driver.quit()
print("✅ Datos actualizados correctamente.")

