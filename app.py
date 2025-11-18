import os
import json
import hvac
from pathlib import Path

class SecretManager:
    def __init__(self):
        self.secrets = {}
    
    def load_from_env(self):
        """Загрузка секретов из переменных окружения"""
        self.secrets['db_password'] = os.getenv('DB_PASSWORD', 'not_set')
        self.secrets['api_key'] = os.getenv('API_KEY', 'not_set')
        print("✅ Секреты загружены из переменных окружения")
        return self.secrets
    
    def load_from_file(self, filepath='config/secrets.json'):
        """Загрузка секретов из файла"""
        try:
            with open(filepath, 'r') as f:
                self.secrets = json.load(f)
            print(f"✅ Секреты загружены из файла {filepath}")
            return self.secrets
        except FileNotFoundError:
            print(f"❌ Файл {filepath} не найден")
            return {}
    
    def load_from_vault(self, vault_url='http://127.0.0.1:8200', token=None):
        """Загрузка секретов из HashiCorp Vault"""
        try:
            if not token:
                token = os.getenv('VAULT_TOKEN')
            
            client = hvac.Client(url=vault_url, token=token)
            
            if not client.is_authenticated():
                print("❌ Не удалось аутентифицироваться в Vault")
                return {}
            
            # Читаем секреты из Vault
            secret_response = client.secrets.kv.v2.read_secret_version(
                path='myapp/config',
                mount_point='secret'
            )
            
            self.secrets = secret_response['data']['data']
            print("✅ Секреты загружены из Vault")
            return self.secrets
            
        except Exception as e:
            print(f"❌ Ошибка при работе с Vault: {e}")
            return {}
    
    def display_secrets(self):
        """Отображение загруженных секретов"""
        print("\n" + "="*50)
        print("🔐 ЗАГРУЖЕННЫЕ СЕКРЕТЫ:")
        print("="*50)
        for key, value in self.secrets.items():
            # Маскируем значения для безопасности
            masked_value = value[:3] + "*"*(len(value)-3) if len(value) > 3 else "***"
            print(f"  {key}: {masked_value}")
        print("="*50 + "\n")


def main():
    print("\n" + "🚀"*25)
    print("   SECURE SECRETS MANAGEMENT DEMO")
    print("🚀"*25 + "\n")
    
    manager = SecretManager()
    
    # Меню выбора метода загрузки
    print("Выберите метод загрузки секретов:")
    print("1. Переменные окружения (Environment Variables)")
    print("2. Файл конфигурации (Config File)")
    print("3. HashiCorp Vault")
    
    choice = input("\nВведите номер (1-3): ").strip()
    
    if choice == '1':
        manager.load_from_env()
    elif choice == '2':
        manager.load_from_file()
    elif choice == '3':
        manager.load_from_vault()
    else:
        print("❌ Неверный выбор!")
        return
    
    manager.display_secrets()
    
    # Симуляция использования секретов
    print("✨ Приложение успешно запущено с загруженными секретами!")
    print("💾 Подключение к базе данных...")
    print("🔑 API аутентификация...")
    print("✅ Всё работает!\n")


if __name__ == "__main__":
    main()
