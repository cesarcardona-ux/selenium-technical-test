"""
Command Builder - Construcción de comandos pytest

Este módulo genera el comando pytest completo basándose en:
- Caso de prueba seleccionado
- Parámetros configurados
- Flags adicionales de pytest
"""

from typing import Dict, Any, List, Optional
from core.config_manager import ConfigManager
from core.case_mapper import CaseMapper


class CommandBuilder:
    """Constructor de comandos pytest"""

    def __init__(self, config_manager: ConfigManager, case_mapper: CaseMapper):
        """
        Inicializa el constructor de comandos

        Args:
            config_manager: Instancia del gestor de configuraciones
            case_mapper: Instancia del mapeador de casos
        """
        self.config = config_manager
        self.mapper = case_mapper

    def build_command(
        self,
        case_id: str,
        selected_parameters: Dict[str, str],
        pytest_flags: Optional[Dict[str, bool]] = None
    ) -> str:
        """
        Construye el comando pytest completo

        Args:
            case_id: ID del caso a ejecutar (ej: "case_1")
            selected_parameters: Diccionario {parameter_name: selected_value}
            pytest_flags: Flags adicionales de pytest (verbose, stop_on_failure, etc.)

        Returns:
            Comando pytest completo listo para ejecutar

        Example:
            >>> builder.build_command(
            ...     "case_1",
            ...     {"browser": "chrome", "language": "Español", "env": "qa5"},
            ...     {"verbose": True, "allure_report": True}
            ... )
            'pytest tests/nuxqa/test_oneway_booking_Case1.py --browser=chrome --language=Español --env=qa5 -v --alluredir=reports/allure'
        """
        # Obtener información del caso
        test_file = self.mapper.get_test_file_path(case_id)
        if not test_file:
            return f"# Error: Caso {case_id} no encontrado"

        # Iniciar comando base
        command_parts = ["pytest", test_file]

        # Obtener parámetros aplicables al caso
        applicable_params = self.mapper.get_applicable_parameters(case_id)

        # Agregar parámetros CLI
        for param_name in applicable_params:
            if param_name in selected_parameters:
                selected_value = selected_parameters[param_name]

                # Convertir display_name a command_value
                command_value = self._get_command_value(param_name, selected_value)

                if command_value:
                    command_parts.append(f"--{param_name}={command_value}")

        # Agregar flags de pytest
        if pytest_flags:
            flag_parts = self._build_pytest_flags(pytest_flags)
            command_parts.extend(flag_parts)

        # Unir todo el comando
        return " ".join(command_parts)

    def build_multiline_command(
        self,
        case_id: str,
        selected_parameters: Dict[str, str],
        pytest_flags: Optional[Dict[str, bool]] = None
    ) -> str:
        """
        Construye el comando pytest en formato multilínea (con backslashes)

        Args:
            case_id: ID del caso
            selected_parameters: Parámetros seleccionados
            pytest_flags: Flags de pytest

        Returns:
            Comando en formato multilínea
        """
        # Obtener información del caso
        test_file = self.mapper.get_test_file_path(case_id)
        if not test_file:
            return f"# Error: Caso {case_id} no encontrado"

        # Iniciar comando
        lines = [f"pytest {test_file} \\"]

        # Obtener parámetros aplicables
        applicable_params = self.mapper.get_applicable_parameters(case_id)

        # Agregar parámetros CLI (uno por línea)
        param_lines = []
        for param_name in applicable_params:
            if param_name in selected_parameters:
                selected_value = selected_parameters[param_name]
                command_value = self._get_command_value(param_name, selected_value)

                if command_value:
                    param_lines.append(f"  --{param_name}={command_value}")

        # Agregar flags de pytest
        if pytest_flags:
            flag_parts = self._build_pytest_flags(pytest_flags)
            if flag_parts:
                # Último parámetro sin backslash
                if param_lines:
                    param_lines[-1] += " \\"
                    lines.extend(param_lines)
                    lines.append(f"  {' '.join(flag_parts)}")
                else:
                    lines[-1] = lines[-1].rstrip(" \\")
                    lines.append(f"  {' '.join(flag_parts)}")
            else:
                # Sin flags, quitar backslash del último parámetro
                if param_lines:
                    lines.extend(param_lines)
                    lines[-1] = lines[-1].rstrip(" \\")
        else:
            if param_lines:
                lines.extend(param_lines)
                lines[-1] = lines[-1].rstrip(" \\")

        return "\n".join(lines)

    def _get_command_value(self, param_name: str, selected_value: str) -> Optional[str]:
        """
        Convierte valor seleccionado en UI a valor de comando

        Args:
            param_name: Nombre del parámetro
            selected_value: Valor seleccionado en dropdown/input

        Returns:
            Valor para usar en el comando o None si no se encuentra
        """
        # Para parámetros numéricos y de texto, usar el valor directamente
        if param_name in ["departure-days", "return-days"]:
            return str(selected_value) if selected_value else None

        # Para ciudades (origin/destination), extraer código IATA
        if param_name in ["origin", "destination"]:
            # El formato en UI es "Bogotá (BOG)", extraemos "BOG"
            if "(" in selected_value and ")" in selected_value:
                iata_code = selected_value.split("(")[1].split(")")[0]
                return iata_code
            return selected_value  # Si no tiene formato esperado, usar directo

        # Para otros parámetros, buscar en parameter_options
        return self.config.get_command_value(param_name, selected_value)

    def _build_pytest_flags(self, pytest_flags: Dict[str, bool]) -> List[str]:
        """
        Construye lista de flags de pytest

        Args:
            pytest_flags: Diccionario {flag_name: enabled}

        Returns:
            Lista de flags habilitados
        """
        flags = []

        flag_mapping = {
            "verbose": "-v",
            "show_prints": "-s",
            "stop_on_first_failure": "-x",
            "last_failed": "--lf",
            "allure_report": "--alluredir=reports/allure",
            "parallel_execution": "-n auto"
        }

        for flag_name, flag_value in flag_mapping.items():
            if pytest_flags.get(flag_name, False):
                flags.append(flag_value)

        return flags

    def validate_parameters(
        self,
        case_id: str,
        selected_parameters: Dict[str, str]
    ) -> tuple[bool, str]:
        """
        Valida que los parámetros seleccionados sean correctos

        Args:
            case_id: ID del caso
            selected_parameters: Parámetros seleccionados

        Returns:
            Tupla (is_valid, error_message)
        """
        applicable_params = self.mapper.get_applicable_parameters(case_id)

        # Verificar que todos los parámetros aplicables tengan un valor
        for param in applicable_params:
            if param not in selected_parameters or not selected_parameters[param]:
                param_label = self.mapper.get_parameter_label(param)
                return False, f"Falta seleccionar: {param_label}"

        # Validar parámetros numéricos
        if "departure-days" in selected_parameters:
            try:
                days = int(selected_parameters["departure-days"])
                if days < 1 or days > 365:
                    return False, "Departure days debe estar entre 1 y 365"
            except ValueError:
                return False, "Departure days debe ser un número"

        if "return-days" in selected_parameters:
            try:
                days = int(selected_parameters["return-days"])
                if days < 1 or days > 365:
                    return False, "Return days debe estar entre 1 y 365"

                # Validar que return sea mayor que departure
                if "departure-days" in selected_parameters:
                    departure = int(selected_parameters["departure-days"])
                    if days <= departure:
                        return False, "Return days debe ser mayor que departure days"
            except ValueError:
                return False, "Return days debe ser un número"

        return True, ""

    def get_parameter_summary(
        self,
        case_id: str,
        selected_parameters: Dict[str, str]
    ) -> Dict[str, str]:
        """
        Genera un resumen legible de los parámetros seleccionados

        Args:
            case_id: ID del caso
            selected_parameters: Parámetros seleccionados

        Returns:
            Diccionario {parameter_label: selected_value}
        """
        summary = {}
        applicable_params = self.mapper.get_applicable_parameters(case_id)

        for param in applicable_params:
            if param in selected_parameters:
                label = self.mapper.get_parameter_label(param)
                value = selected_parameters[param]
                summary[label] = value

        return summary
