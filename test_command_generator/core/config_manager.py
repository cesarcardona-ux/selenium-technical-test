"""
Config Manager - Gestión de archivos JSON de configuración

Este módulo maneja la carga y guardado de todos los archivos JSON:
- case_mappings.json: Mapeo de casos a parámetros
- parameter_options.json: Opciones disponibles para cada parámetro
- testdata.json: Datos de prueba (pasajeros, pago, facturación)
- saved_configs/: Configuraciones guardadas por el usuario
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime


class ConfigManager:
    """Gestor de configuraciones JSON"""

    def __init__(self):
        """Inicializa el gestor de configuraciones"""
        # Obtener directorio base del proyecto (donde está main.py)
        self.base_dir = Path(__file__).parent.parent
        self.config_dir = self.base_dir / "config"

        # Asegurar que exista el directorio
        self.config_dir.mkdir(parents=True, exist_ok=True)

        # Rutas de archivos JSON
        self.case_mappings_file = self.config_dir / "case_mappings.json"
        self.parameter_options_file = self.config_dir / "parameter_options.json"
        self.testdata_file = self.config_dir / "testdata.json"

        # Cache de configuraciones
        self._case_mappings = None
        self._parameter_options = None
        self._testdata = None

    def _load_json(self, file_path: Path) -> Dict[str, Any]:
        """
        Carga un archivo JSON

        Args:
            file_path: Ruta del archivo JSON

        Returns:
            Diccionario con el contenido del JSON

        Raises:
            FileNotFoundError: Si el archivo no existe
            json.JSONDecodeError: Si el JSON está mal formateado
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"Archivo no encontrado: {file_path}")
        except json.JSONDecodeError as e:
            raise json.JSONDecodeError(f"Error al parsear JSON en {file_path}: {e}", e.doc, e.pos)

    def _save_json(self, data: Dict[str, Any], file_path: Path) -> None:
        """
        Guarda datos en un archivo JSON

        Args:
            data: Diccionario a guardar
            file_path: Ruta del archivo JSON
        """
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    # ==================== CASE MAPPINGS ====================

    def load_case_mappings(self) -> Dict[str, Any]:
        """
        Carga el mapeo de casos de prueba

        Returns:
            Diccionario con mapeo de casos (case_1, case_2, etc.)
        """
        if self._case_mappings is None:
            self._case_mappings = self._load_json(self.case_mappings_file)
        return self._case_mappings

    def get_case_info(self, case_id: str) -> Optional[Dict[str, Any]]:
        """
        Obtiene información de un caso específico

        Args:
            case_id: ID del caso (ej: "case_1", "case_3")

        Returns:
            Diccionario con info del caso o None si no existe
        """
        mappings = self.load_case_mappings()
        return mappings.get(case_id)

    def get_all_cases(self) -> Dict[str, str]:
        """
        Obtiene lista de todos los casos disponibles

        Returns:
            Diccionario {case_id: case_name}
        """
        mappings = self.load_case_mappings()
        return {case_id: info["name"] for case_id, info in mappings.items()}

    # ==================== PARAMETER OPTIONS ====================

    def load_parameter_options(self) -> Dict[str, Any]:
        """
        Carga todas las opciones de parámetros

        Returns:
            Diccionario con opciones de cada parámetro
        """
        if self._parameter_options is None:
            self._parameter_options = self._load_json(self.parameter_options_file)
        return self._parameter_options

    def get_parameter_options(self, parameter_name: str) -> Optional[Dict[str, Any]]:
        """
        Obtiene las opciones disponibles de un parámetro específico

        Args:
            parameter_name: Nombre del parámetro (ej: "browser", "language")

        Returns:
            Diccionario con opciones del parámetro o None si no existe
        """
        options = self.load_parameter_options()
        return options.get(parameter_name)

    def get_parameter_display_values(self, parameter_name: str) -> list:
        """
        Obtiene lista de valores para mostrar en dropdowns

        Args:
            parameter_name: Nombre del parámetro

        Returns:
            Lista de display_name values
        """
        options = self.get_parameter_options(parameter_name)
        if options:
            return [opt["display_name"] for opt in options.values()]
        return []

    def get_command_value(self, parameter_name: str, display_value: str) -> Optional[str]:
        """
        Convierte display_name a command_value

        Args:
            parameter_name: Nombre del parámetro
            display_value: Valor mostrado en UI

        Returns:
            Valor para usar en el comando pytest
        """
        options = self.get_parameter_options(parameter_name)
        if options:
            for opt in options.values():
                if opt["display_name"] == display_value:
                    return opt["command_value"]
        return None

    # ==================== TEST DATA ====================

    def load_testdata(self) -> Dict[str, Any]:
        """
        Carga datos de prueba (pasajeros, pago, facturación)

        Returns:
            Diccionario con datos de prueba
        """
        if self._testdata is None:
            self._testdata = self._load_json(self.testdata_file)
        return self._testdata

    def save_testdata(self, testdata: Dict[str, Any]) -> None:
        """
        Guarda cambios en los datos de prueba

        Args:
            testdata: Diccionario con datos actualizados (passengers, payment, billing)
        """
        # Cargar datos actuales para preservar current_session si existe
        try:
            current_data = self._load_json(self.testdata_file)
        except:
            current_data = {}

        # Actualizar solo los datos de test, preservar current_session
        current_data.update({
            "passengers": testdata.get("passengers", {}),
            "payment": testdata.get("payment", {}),
            "billing": testdata.get("billing", {})
        })

        self._save_json(current_data, self.testdata_file)
        self._testdata = current_data  # Actualizar cache

    def save_complete_state(self, case_id: str, parameters: Dict[str, str],
                           pytest_flags: Dict[str, bool], testdata: Dict[str, Any]) -> None:
        """
        Guarda TODO el estado de la aplicación en testdata.json

        Args:
            case_id: ID del caso seleccionado
            parameters: Parámetros configurados
            pytest_flags: Pytest flags configurados
            testdata: Datos de prueba (passengers, payment, billing)
        """
        complete_data = {
            "current_session": {
                "case_id": case_id,
                "parameters": parameters,
                "pytest_flags": pytest_flags
            },
            "passengers": testdata.get("passengers", {}),
            "payment": testdata.get("payment", {}),
            "billing": testdata.get("billing", {})
        }

        self._save_json(complete_data, self.testdata_file)
        self._testdata = complete_data  # Actualizar cache

    def load_current_session(self) -> Optional[Dict[str, Any]]:
        """
        Carga la sesión actual desde testdata.json

        Returns:
            Diccionario con case_id, parameters, pytest_flags o None
        """
        try:
            data = self.load_testdata()
            return data.get("current_session")
        except:
            return None

    def get_passenger_data(self, passenger_type: str) -> Optional[Dict[str, Any]]:
        """
        Obtiene datos de un tipo de pasajero

        Args:
            passenger_type: Tipo de pasajero (adult, teen, child, infant)

        Returns:
            Diccionario con datos del pasajero
        """
        testdata = self.load_testdata()
        return testdata.get("passengers", {}).get(passenger_type)

    def get_payment_data(self) -> Dict[str, Any]:
        """Obtiene datos de pago"""
        testdata = self.load_testdata()
        return testdata.get("payment", {})

    def get_billing_data(self) -> Dict[str, Any]:
        """Obtiene datos de facturación"""
        testdata = self.load_testdata()
        return testdata.get("billing", {})

