#!/bin/bash
export GPG_TTY=$(tty)
sops -d config/secrets.enc.json > config/secrets.json
echo "✅ Секреты расшифрованы в config/secrets.json"