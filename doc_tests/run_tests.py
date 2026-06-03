#!/usr/bin/env python
"""
run_tests.py - Script para rodar testes pytest
"""

import subprocess
import sys
import os

os.chdir(r"c:..\sistema-gestao-transparencia-ong")

# Instalar pytest se necessário
try:
    import pytest
except ImportError:
    print("[*] Instalando pytest...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", "pytest", "pytest-asyncio", "pytest-cov", "httpx"])
    import pytest

# Executar testes
print("\n[+] Executando testes...\n")
sys.exit(pytest.main(["tests/", "-v", "--tb=short", "-x"]))
