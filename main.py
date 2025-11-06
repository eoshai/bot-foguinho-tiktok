import json
import time
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
import pyperclip

RESET      = "\033[0m"
LARANJA    = "\033[38;5;208m"
VERDE      = "\033[92m"
VERMELHO   = "\033[91m"
AZUL       = "\033[94m"
CINZA      = "\033[90m"
AMARELO    = "\033[93m"
BRANCO = "\033[97m"

banner = f"""
{BRANCO}
░▒▓████████▓▒░▒▓██████▓▒░ ░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░▒▓███████▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓██████▓▒░  
░▒▓█▓▒░     ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ 
░▒▓█▓▒░     ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ 
░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒▒▓███▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓████████▓▒░▒▓█▓▒░░▒▓█▓▒░ 
░▒▓█▓▒░     ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ 
░▒▓█▓▒░     ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ 
░▒▓█▓▒░      ░▒▓██████▓▒░ ░▒▓██████▓▒░ ░▒▓██████▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░░▒▓██████▓▒░  
🛠️  Desenvolvido por Shai
{RESET}
"""

def carregar_config():
    """Carrega configurações do config.json ou usa valores padrão."""
    config_path = Path("config.json")
    config_padrao = {
        "mensagem_padrao": "🔥 Acende nosso foguinho aee - 🤖",
        "pessoas_especiais": {},
        "delay_entre_mensagens": 2.0,
        "usar_headless": False,
        "tempo_espera_load": 15,
        "screenshot_final": True
    }
    
    if config_path.exists():
        try:
            with config_path.open("r", encoding="utf-8") as f:
                config_usuario = json.load(f)
                # Mescla com configurações padrão
                config_padrao.update(config_usuario)
                print(f"{VERDE}✅ Configurações carregadas de config.json{RESET}")
        except Exception as e:
            print(f"{VERMELHO}⚠️ Erro ao ler config.json: {e}. Usando valores padrão.{RESET}")
    else:
        print(f"{AMARELO}⚠️ config.json não encontrado, usando valores padrão.{RESET}")
        print(f"{AMARELO}💡 Dica: Crie um config.json para personalizar as mensagens!{RESET}")
    
    return config_padrao

def carregar_fogos():
    """Carrega lista de nomes do fogos.json."""
    fogos_path = Path("fogos.json")
    if fogos_path.exists():
        try:
            with fogos_path.open("r", encoding="utf-8") as f:
                nomes = json.load(f)
                print(f"{VERDE}✅ Lista de fogos carregada: {len(nomes)} pessoas{RESET}")
                return nomes
        except Exception as e:
            print(f"{VERMELHO}❌ Erro ao ler fogos.json: {e}{RESET}")
            return []
    else:
        print(f"{VERMELHO}❌ fogos.json não encontrado{RESET}")
        return []

def carregar_cookies(driver):
    """Carrega e injeta cookies do cookies.json."""
    cookies_path = Path("cookies.json")
    if not cookies_path.exists():
        print(f"{VERMELHO}❌ cookies.json não encontrado!{RESET}")
        return False
    
    try:
        with cookies_path.open("r", encoding="utf-8") as f:
            raw_cookies = json.load(f)
        
        print(f"{BRANCO}🍪 Injetando cookies...{RESET}")
        for cookie in raw_cookies:
            try:
                new_cookie = {
                    "name": cookie["name"],
                    "value": cookie["value"],
                    "domain": cookie["domain"] if cookie["domain"].startswith(".") else "." + cookie["domain"],
                    "path": cookie.get("path", "/"),
                    "secure": cookie.get("secure", False),
                    "httpOnly": cookie.get("httpOnly", False),
                }
                if "expirationDate" in cookie:
                    new_cookie["expiry"] = int(float(cookie["expirationDate"]))
                driver.add_cookie(new_cookie)
            except Exception as e:
                print(f"{VERMELHO}❌ Erro ao add cookie {cookie['name']}: {e}{RESET}")
        return True
    except Exception as e:
        print(f"{VERMELHO}❌ Erro ao carregar cookies: {e}{RESET}")
        return False

def enviar_mensagem(driver, wait, nome_pessoa, mensagem, config):
    """Envia mensagem para uma pessoa específica."""
    try:
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div[contenteditable='true']")))
        editor_div = driver.find_element(By.CSS_SELECTOR, "div[contenteditable='true']")
        
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", editor_div)
        time.sleep(0.5)
        
        editor_div.click()
        time.sleep(0.3)
        
        pyperclip.copy(mensagem)
        editor_div.send_keys(Keys.CONTROL, "v")    
        editor_div.send_keys(Keys.ENTER)
        
        # Verifica se é pessoa especial para colorir o log
        if nome_pessoa in config["pessoas_especiais"]:
            print(f"{VERMELHO}💖 Foguinho com {nome_pessoa} aceso com sucesso{RESET}\n")
        else:
            print(f"{LARANJA}🔥 Foguinho com {nome_pessoa} aceso com sucesso{RESET}\n")
        
        time.sleep(config["delay_entre_mensagens"])
        return True
    except Exception as e:
        print(f"{VERMELHO}❌ Erro ao enviar mensagem para {nome_pessoa}: {e}{RESET}")
        return False

def main():
    print(banner)
    
    # Carrega configurações
    config = carregar_config()
    nomes_fogos = carregar_fogos()
    
    if not nomes_fogos:
        print(f"{VERMELHO}❌ Nenhum nome para acender foguinho. Encerrando.{RESET}")
        return
    
    # Configura o navegador
    options = Options()
    options.add_argument("--start-maximized")
    if config.get("usar_headless"):
        options.add_argument("--headless=new")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_experimental_option("detach", True)
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        print(f"{AZUL}🌐 Preparando ambiente...{RESET}")
        driver.get("https://www.tiktok.com/")
        time.sleep(5)
        
        # Carrega cookies
        if not carregar_cookies(driver):
            driver.quit()
            return
        
        # Acessa mensagens
        redirect_url = "https://www.tiktok.com/messages?lang=en"
        print(f"{VERDE}📨 Acessando direct...{RESET}")
        driver.get(redirect_url)
        
        wait = WebDriverWait(driver, 30)
        
        print(f"{CINZA}⏳ Aguardando carregamento ({config['tempo_espera_load']}s)...{RESET}")
        time.sleep(config["tempo_espera_load"])
        
        # Espera os nomes carregarem
        try:
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "p[class*='PInfoNickname']")))
            nickname_elements = driver.find_elements(By.CSS_SELECTOR, "p[class*='PInfoNickname']")
            print(f"{VERDE}✅ Lista de conversas carregada com sucesso!{RESET}")
        except TimeoutException:
            print(f"{VERMELHO}❌ Não foi possível encontrar os contatos.{RESET}")
            if config["screenshot_final"]:
                driver.save_screenshot("erro_tiktok.png")
            driver.quit()
            return
        
        # Procura pelos nomes
        encontrados = []
        print(f"\n{BRANCO}👤 Nomes encontrados:{RESET}")
        for el in nickname_elements:
            nome = el.text.strip()
            if nome:
                # Destaca pessoas especiais
                if nome in config["pessoas_especiais"]:
                    print(f"💖 {VERMELHO}- {nome}{RESET}")
                else:
                    print(f"{BRANCO}- {nome}{RESET}")
                
                if nome in nomes_fogos:
                    encontrados.append((el, nome))
        
        # Envia mensagens
        print(f"\n{LARANJA}🔥 Fogos para acender: {len(encontrados)}{RESET}\n")
        for alvo_element, nome_alvo in encontrados:
            try:
                driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth'});", alvo_element)
                time.sleep(1.5)
                alvo_element.click()
                
                if nome_alvo in config["pessoas_especiais"]:
                    print(f"{VERMELHO}💖 Acendendo o fogo com {nome_alvo}{RESET}")
                else:
                    print(f"{VERDE}✅ Acendendo o fogo com {nome_alvo}{RESET}")
                
                time.sleep(0.6)
                
                # Define a mensagem (especial ou padrão)
                frase = config["pessoas_especiais"].get(nome_alvo, config["mensagem_padrao"])
                enviar_mensagem(driver, wait, nome_alvo, frase, config)
                
            except Exception as e:
                print(f"{VERMELHO}❌ Erro com {nome_alvo}: {e}{RESET}")
        
        # Screenshot final
        if config["screenshot_final"]:
            driver.save_screenshot("tiktok_resultado.png")
            print(f"{AZUL}📸 Resultado salvo em 'tiktok_resultado.png'{RESET}")
        
        print(f"\n{VERDE}✅ Processo concluído!{RESET}")
        time.sleep(5)
        
    finally:
        driver.quit()

if __name__ == "__main__":
    main()