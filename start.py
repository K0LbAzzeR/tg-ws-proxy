# start.py — упрощённый запуск прокси без GUI и Windows‑зависимостей

import asyncio
import os
import sys
import logging
from pathlib import Path
from typing import Optional

# Импорт основной функции запуска прокси
from proxy.tg_ws_proxy import _run

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('proxy.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Конфигурация по умолчанию
DEFAULT_CONFIG = {
    'port': 1443,
    'host': '127.0.0.1',
    'dc_ip': ['2:149.154.167.220', '4:149.154.167.220'],
    'verbose': False,
    'check_updates': True,
    'log_max_mb': 5,
    'buf_kb': 256,
    'pool_size': 4,
    'cfproxy': True,
    'cfproxy_priority': True,
    'cfproxy_user_domain': '',
    'secret': 'b37989af0db1b25d8546d5f4d7107f73',
    'autostart': False
}

def ensure_dirs():
    """Создаёт необходимые директории для работы прокси"""
    dirs = ['logs', 'data']
    for dir_name in dirs:
        Path(dir_name).mkdir(exist_ok=True)
        logger.info(f"Создана директория: {dir_name}")

async def main():
    """Основная функция запуска прокси"""
    logger.info("Запуск TG WS Proxy...")

    # Создаём необходимые директории
    ensure_dirs()

    # Создаём событие остановки
    stop_event = asyncio.Event()

    try:
        # Запускаем прокси с событием остановки (без передачи config)
        await _run(stop_event)
        logger.info("Прокси успешно запущен")
        logger.info(f"Слушает на {DEFAULT_CONFIG['host']}:{DEFAULT_CONFIG['port']}")
        logger.info(f"Секрет: {DEFAULT_CONFIG['secret']}")

        # Ждём сигнала остановки
        await stop_event.wait()

    except KeyboardInterrupt:
        logger.info("Получен сигнал прерывания (Ctrl+C)")
    except Exception as e:
        logger.error(f"Критическая ошибка: {e}")
        raise
    finally:
        logger.info("Остановка прокси...")

if __name__ == '__main__':
    # Запускаем асинхронное приложение
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nПрокси остановлен пользователем")
    except Exception as e:
        print(f"Ошибка запуска: {e}")
        sys.exit(1)
