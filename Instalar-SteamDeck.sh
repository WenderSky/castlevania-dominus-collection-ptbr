#!/usr/bin/env bash
# Instalador para Steam Deck / Linux. Rode no Modo Desktop (Konsole).
cd "$(dirname "$0")" || exit 1
python3 instalar.py "$@"
echo
read -rp "Pressione ENTER para sair..."
