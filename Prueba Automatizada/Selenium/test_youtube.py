from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import base64
import webbrowser
from selenium.common.exceptions import NoSuchElementException, TimeoutException

service = Service(executable_path='C:\\Users\\Scarl\\OneDrive\\Documents\\WebDriver\\chromedriver.exe')
driver = webdriver.Chrome(service=service)

try:
    driver.get('https://www.youtube.com/')
    driver.maximize_window()
    time.sleep(2)

    search_box = driver.find_element(By.NAME, 'search_query')
    search_box.send_keys('Encontrando el balance en mi vida')
    search_box.send_keys(Keys.RETURN)
    time.sleep(4)

    for _ in range(5):
        driver.execute_script("window.scrollBy(0, 500)")
        time.sleep(1)

    videos = driver.find_elements(By.ID, 'video-title')
    print("Títulos de los videos encontrados:")
    titulos_videos = []
    for idx, video in enumerate(videos):
        titulo = video.get_attribute("title")
        if titulo:
            print(f"{idx+1}. {titulo}")
            titulos_videos.append(titulo)

    os.makedirs(os.path.join(os.path.expanduser("~"), "Imágenes"), exist_ok=True)
    documentos = os.path.join(os.path.expanduser("~"), "Documents")
    ruta_html = os.path.join(documentos, "reporte_youtube.html")

    html = """
    <html>
        <head>
            <meta charset="UTF-8">
            <title>Reporte de Prueba - YouTube</title>
        </head>
        <body>
            <h1>Reporte de Prueba Automatizada</h1>

            <h2>Títulos de los videos encontrados:</h2>
            <ul>
    """

    for titulo in titulos_videos:
        html += f"<li>{titulo}</li>"

    html += """
            </ul>
    """

    try:
        tabs = driver.find_elements(By.XPATH, '//yt-chip-cloud-chip-renderer//a')
        for tab in tabs:
            if 'Canales' in tab.text:
                tab.click()
                break
        time.sleep(3)

        canal = driver.find_element(By.XPATH, '//a[@id="main-link"]')
        canal_encontrado = 'Encontrando el balance en mi vida' in canal.text
        if canal_encontrado:
            print("Canal 'Encontrando el balance en mi vida' encontrado.")
            canal.click()
            time.sleep(4)

            path_balance = os.path.join(os.path.expanduser("~"), "Imágenes", "canal_balance.png")
            driver.save_screenshot(path_balance)
            print(f"Captura del canal 'Encontrando el balance en mi vida' guardada en: {path_balance}")

            with open(path_balance, "rb") as img_file:
                img_balance_base64 = base64.b64encode(img_file.read()).decode('utf-8')

            html += """
            <h2>Captura del canal 'Encontrando el balance en mi vida':</h2>
            <img src="data:image/png;base64,""" + img_balance_base64 + """" width="500"/>
            """

            driver.get('https://www.youtube.com/')
            time.sleep(2)
        else:
            html += "<p>El canal no coincide exactamente con el nombre.</p>"
    except NoSuchElementException:
        html += "<p>No se encontró canal con ese nombre.</p>"
        canal_encontrado = False

    search_box = driver.find_element(By.NAME, 'search_query')
    search_box.clear()
    search_box.send_keys('Jordi Wu')
    search_box.send_keys(Keys.RETURN)
    time.sleep(3)

    tabs = driver.find_elements(By.XPATH, '//yt-chip-cloud-chip-renderer//a')
    for tab in tabs:
        if 'Canales' in tab.text:
            tab.click()
            break
    time.sleep(3)

    canal = driver.find_element(By.XPATH, '//a[@id="main-link"]')
    canal.click()
    time.sleep(4)

    path_jordi = os.path.join(os.path.expanduser("~"), "Imágenes", "canal_jordiwu.png")
    driver.save_screenshot(path_jordi)
    print(f"Captura guardada en: {path_jordi}")

    primer_video = driver.find_element(By.XPATH, '//ytd-grid-video-renderer[1]//a[@id="thumbnail"]')
    primer_video.click()
    print("Esperando que el usuario omita el anuncio... (tienes 10 segundos)")
    time.sleep(10)

    path_video = os.path.join(os.path.expanduser("~"), "Imágenes", "video_jordiwu.png")
    driver.save_screenshot(path_video)
    print(f"Captura del video guardada en: {path_video}")

    for _ in range(10):
        driver.execute_script("window.scrollBy(0, 500)")
        time.sleep(1)

    comentarios_texto = []
    try:
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, '//ytd-comment-thread-renderer'))
        )
        comentarios = driver.find_elements(By.XPATH, '//ytd-comment-thread-renderer')
        if len(comentarios) >= 5:
            print("Hay al menos 5 comentarios.")
        else:
            print("Hay menos de 5 comentarios.")

        print("\nPrimeros 2 comentarios:")
        for idx in range(min(2, len(comentarios))):
            texto = comentarios[idx].find_element(By.ID, "content-text").text
            print(f"{idx+1}. {texto}")
            comentarios_texto.append(texto)
    except TimeoutException:
        print("Los comentarios no se cargaron correctamente.")

    relacionados = driver.find_elements(By.XPATH, '//ytd-compact-video-renderer//span[@id="video-title"]')
    print("\nVideos relacionados:")
    relacionados_texto = []
    for idx, r in enumerate(relacionados[:5]):
        print(f"{idx+1}. {r.text}")
        relacionados_texto.append(r.text)

    path_comentarios = os.path.join(os.path.expanduser("~"), "Imágenes", "comentarios_jordiwu.png")
    driver.save_screenshot(path_comentarios)
    print(f"Captura de comentarios guardada en: {path_comentarios}")

    driver.execute_script("window.scrollBy(0, 600)")
    time.sleep(2)
    path_relacionados = os.path.join(os.path.expanduser("~"), "Imágenes", "relacionados_jordiwu.png")
    driver.save_screenshot(path_relacionados)
    print(f"Captura de videos relacionados guardada en: {path_relacionados}")

    with open(path_jordi, "rb") as img_file:
        img_jordi_base64 = base64.b64encode(img_file.read()).decode('utf-8')

    with open(path_video, "rb") as img_file:
        img_video_base64 = base64.b64encode(img_file.read()).decode('utf-8')

    with open(path_comentarios, "rb") as img_file:
        img_comentarios_base64 = base64.b64encode(img_file.read()).decode('utf-8')

    with open(path_relacionados, "rb") as img_file:
        img_relacionados_base64 = base64.b64encode(img_file.read()).decode('utf-8')

    html += """
        <h2>Captura del canal Jordi Wu:</h2>
        <img src="data:image/png;base64,""" + img_jordi_base64 + """" width="500"/>

        <h2>Captura del video:</h2>
        <img src="data:image/png;base64,""" + img_video_base64 + """" width="500"/>

        <h2>Captura de la sección de comentarios:</h2>
        <img src="data:image/png;base64,""" + img_comentarios_base64 + """" width="500"/>

        <h2>Comentarios (2):</h2>
        <ul>
    """

    for comentario in comentarios_texto:
        html += f"<li>{comentario}</li>"

    html += """
        </ul>

        <h2>Captura de la sección de videos sugeridos:</h2>
        <img src="data:image/png;base64,""" + img_relacionados_base64 + """" width="500"/>

        <h2>Videos sugeridos:</h2>
        <ul>
    """

    for relacionado in relacionados_texto:
        html += f"<li>{relacionado}</li>"

    html += """
        </ul>
        </body>
    </html>
    """

    with open(ruta_html, "w", encoding="utf-8") as archivo:
        archivo.write(html)

    print(f"\nReporte HTML generado en: {ruta_html}")
    webbrowser.open(f'file://{ruta_html}')

finally:
    time.sleep(3)
    driver.quit()