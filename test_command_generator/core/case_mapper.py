"""
Case Mapper - Mapeo de parámetros aplicables por caso

Este módulo determina qué parámetros están disponibles para cada caso de prueba
y gestiona la habilitación/deshabilitación dinámica de parámetros en la UI.
"""

from typing import List, Dict, Any
from core.config_manager import ConfigManager


class CaseMapper:
    """Gestor de mapeo de casos a parámetros"""

    def __init__(self, config_manager: ConfigManager):
        """
        Inicializa el mapeador de casos

        Args:
            config_manager: Instancia del gestor de configuraciones
        """
        self.config = config_manager

    def get_applicable_parameters(self, case_id: str) -> List[str]:
        """
        Obtiene lista de parámetros aplicables a un caso

        Args:
            case_id: ID del caso (ej: "case_1", "case_3")

        Returns:
            Lista de nombres de parámetros aplicables
        """
        case_info = self.config.get_case_info(case_id)
        if case_info:
            return case_info.get("applicable_parameters", [])
        return []

    def is_parameter_applicable(self, case_id: str, parameter_name: str) -> bool:
        """
        Verifica si un parámetro aplica a un caso específico

        Args:
            case_id: ID del caso
            parameter_name: Nombre del parámetro

        Returns:
            True si el parámetro aplica al caso
        """
        applicable_params = self.get_applicable_parameters(case_id)
        return parameter_name in applicable_params

    def requires_testdata(self, case_id: str) -> bool:
        """
        Verifica si un caso requiere datos de prueba

        Args:
            case_id: ID del caso

        Returns:
            True si requiere test data (pasajeros, pago, etc.)
        """
        case_info = self.config.get_case_info(case_id)
        if case_info:
            return case_info.get("requires_testdata", False)
        return False

    def get_testdata_sections(self, case_id: str) -> List[str]:
        """
        Obtiene las secciones de test data requeridas por un caso

        Args:
            case_id: ID del caso

        Returns:
            Lista de secciones (ej: ["passengers", "payment", "billing"])
        """
        case_info = self.config.get_case_info(case_id)
        if case_info:
            return case_info.get("testdata_sections", [])
        return []

    def get_all_parameters(self) -> List[str]:
        """
        Obtiene lista de TODOS los parámetros disponibles en el sistema

        Returns:
            Lista de nombres de parámetros
        """
        # Parámetros principales (no numéricos)
        main_params = [
            "browser",
            "language",
            "pos",
            "env",
            "header-link",
            "footer-link",
            "screenshots",
            "video"
        ]

        # Parámetros de ciudades (se manejan diferente porque son inputs de texto)
        city_params = [
            "origin",
            "destination"
        ]

        # Parámetros numéricos (días)
        numeric_params = [
            "departure-days",
            "return-days"
        ]

        return main_params + city_params + numeric_params

    def get_parameter_type(self, parameter_name: str) -> str:
        """
        Determina el tipo de widget para un parámetro

        Args:
            parameter_name: Nombre del parámetro

        Returns:
            Tipo de widget: "dropdown", "text", "number"
        """
        if parameter_name in ["origin", "destination"]:
            return "dropdown"  # Dropdown de ciudades
        elif parameter_name in ["departure-days", "return-days"]:
            return "number"  # Input numérico
        else:
            return "dropdown"  # Dropdown genérico

    def get_parameter_label(self, parameter_name: str) -> str:
        """
        Obtiene el label legible para mostrar en UI

        Args:
            parameter_name: Nombre del parámetro

        Returns:
            Label formateado
        """
        labels = {
            "browser": "Browser",
            "language": "Language / Idioma",
            "pos": "POS (Country)",
            "env": "Environment",
            "origin": "Origin City",
            "destination": "Destination City",
            "departure-days": "Departure (days from today)",
            "return-days": "Return (days from today)",
            "header-link": "Header Link",
            "footer-link": "Footer Link",
            "screenshots": "Screenshots Mode",
            "video": "Video Recording"
        }
        return labels.get(parameter_name, parameter_name)

    def get_parameter_category(self, parameter_name: str) -> str:
        """
        Categoriza un parámetro para organizar la UI

        Args:
            parameter_name: Nombre del parámetro

        Returns:
            Categoría: "core", "navigation", "redirects", "evidence"
        """
        categories = {
            "browser": "core",
            "env": "core",
            "language": "core",
            "pos": "core",
            "origin": "navigation",
            "destination": "navigation",
            "departure-days": "navigation",
            "return-days": "navigation",
            "header-link": "redirects",
            "footer-link": "redirects",
            "screenshots": "evidence",
            "video": "evidence"
        }
        return categories.get(parameter_name, "other")

    def get_case_description(self, case_id: str) -> str:
        """
        Obtiene descripción de un caso

        Args:
            case_id: ID del caso

        Returns:
            Descripción del caso
        """
        case_info = self.config.get_case_info(case_id)
        if case_info:
            return case_info.get("description", "")
        return ""

    def get_test_file_path(self, case_id: str) -> str:
        """
        Obtiene la ruta del archivo de test

        Args:
            case_id: ID del caso

        Returns:
            Ruta relativa del archivo de test
        """
        case_info = self.config.get_case_info(case_id)
        if case_info:
            return case_info.get("test_file", "")
        return ""

    def get_parameters_by_category(self, case_id: str) -> Dict[str, List[str]]:
        """
        Agrupa parámetros aplicables por categoría

        Args:
            case_id: ID del caso

        Returns:
            Diccionario {categoría: [parámetros]}
        """
        applicable = self.get_applicable_parameters(case_id)

        categorized = {
            "core": [],
            "navigation": [],
            "redirects": [],
            "evidence": []
        }

        for param in applicable:
            category = self.get_parameter_category(param)
            if category in categorized:
                categorized[category].append(param)

        # Eliminar categorías vacías
        return {k: v for k, v in categorized.items() if v}
