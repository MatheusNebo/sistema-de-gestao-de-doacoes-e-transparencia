#!/usr/bin/env python
"""
run_service_tests.py - Testes dos serviços (camada de negócio)
"""

import subprocess
import sys
import os

os.chdir(r"c:\Users\Pichau\Desktop\sistema-gestao-transparencia-ong")

# Instalar pytest se necessário
try:
    import pytest
except ImportError:
    print("[*] Instalando pytest...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", "pytest", "pytest-asyncio", "pytest-cov", "httpx"])
    import pytest

# Executar testes dos SERVICES (sem os testes de API)
print("\n[+] Executando testes de SERVICES (camada de negócio)...\n")
sys.exit(pytest.main([
    "tests/test_product_service.py",
    "tests/test_beneficiary_service.py",
    "tests/test_donor_service.py",
    "-v",
    "--tb=short",
]))
