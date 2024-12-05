# Monitorování dostupnosti Automatu - Inosys

## Popis Skriptu
Tento Python skript slouží k automatickému monitorování prodejního automatu, který je spravován společností Inosys. Skript využívá knihovnu Selenium pro automatizované procházení webové stránky a přihlášení do monitorovacího systému. Hlavní funkcí skriptu je zjistit stav automatu a pokud detekuje problém dle stavu na webovém portálu, odešle upozornění prostřednictvím emailu.

Skript kontroluje stránku, kde se nachází informace o stavu prodejního automatu. Pokud je automat ve stavu označeném jako "red" (červený) nebo "orange" (oranžový), skript odešle varovný email na zadanou adresu s informací o posledním čase kdy byl automat dostupný.

## Jak Skript Používat
1. **Instalace Závislostí**: Nejprve nainstalujte potřebné balíčky uvedené v souboru `requirements.txt`. To můžete provést pomocí příkazu:
   ```bash
   pip install -r requirements.txt
   ```

2. **Konfigurace Skriptu**: Údaje pro SMTP odesílání emailů nahraďte svými hodnotami. Skript byl testován oproti SMTP seznam.cz
   ```
   SMTP_SERVER = "smtp.seznam.cz"
   SMTP_PORT = 465
   SMTP_USERNAME = "your_username@example.com"
   SMTP_PASSWORD = "your_password"
   SENDER_EMAIL = "your_sender_email@example.com"
   RECIPIENT_EMAIL = "your_recipient_email@example.com"
   ```

   **Doporučení**: Doporučujeme vytvořit nového uživatele přímo v portále Inosys, který bude mít omezená práva a bude využíván pouze pro účely tohoto skriptu. Tento uživatel by měl mít minimální oprávnění potřebná pro přístup k monitorovacím údajům, což zvyšuje celkovou bezpečnost.

3. **Spuštění Skriptu**: Skript můžete spustit přímo pomocí Pythonu:
   ```bash
   python3 monitor_offline_alert.py
   ```

4. **Doporučení pro Spouštění Skriptu Pravidelně**: Doporučujeme skript spouštět pravidelně pomocí `cron` úloh, například třikrát denně (např. v 5:00, 12:00 a 16:55). Přidejte následující řádek do svého `crontab` souboru:
   ```bash
   0 5,12 * * * /usr/bin/python3 /cesta/k/vasemu/skriptu/monitor_offline_alert.py
   55 16 * * * /usr/bin/python3 /cesta/k/vasemu/skriptu/monitor_offline_alert.py
   ```
   Tím zajistíte, že skript poběží pravidelně a včas vás upozorní na případné problémy.

## Kontakt
Pokud máte jakékoli otázky nebo potřebujete pomoc, neváhejte mě kontaktovat:
- **Jméno**: Lukáš Hájek (eastwickcz)
- **Email**: [mail@lukihajek.cz](mailto:mail@lukihajek.cz)

