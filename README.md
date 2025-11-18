# Secure Secrets Management Lab

## Описание
Демонстрация различных методов управления секретами в приложении.

## Методы работы с секретами

### 1. Environment Variables (Переменные окружения)
```bash
export DB_PASSWORD="your_password"
export API_KEY="your_api_key"
python app.py
```

### 2. Config File (Файл конфигурации)
Расшифруй секреты и запусти:
```bash
./decrypt_secrets.sh
python app.py
```

### 3. HashiCorp Vault
Запусти Vault:
```bash
vault server -dev
```

В другом терминале:
```bash
export VAULT_ADDR='http://127.0.0.1:8200'
export VAULT_TOKEN='your_token'
python app.py
```

## Шифрование с SOPS

Для расшифровки секретов нужен GPG ключ:
```bash
./decrypt_secrets.sh
```

## Требования
- Python 3.7+
- SOPS
- GPG
- HashiCorp Vault