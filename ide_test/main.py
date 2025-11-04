"""
Pytest Command Generator - Main Entry Point

Aplicación de escritorio para generar comandos pytest configurando parámetros
de forma visual mediante interfaz gráfica.

Author: César Cardona
Company: FLYR Inc / Avianca
Date: 2025-01-03
"""

import sys
from pathlib import Path

# Agregar directorio actual al path para imports
current_dir = Path(__file__).parent
if str(current_dir) not in sys.path:
    sys.path.insert(0, str(current_dir))

from gui.main_window import MainWindow


def main():
    """Punto de entrada principal de la aplicación"""
    try:
        app = MainWindow()
        app.mainloop()
    except KeyboardInterrupt:
        print("\n\nApplication terminated by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n\nFatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
