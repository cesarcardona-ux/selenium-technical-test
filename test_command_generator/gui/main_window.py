"""
Main Window - Ventana principal de la aplicación

Contiene la interfaz gráfica completa con:
- Selector de caso de prueba
- Panel de parámetros dinámico
- Panel de datos de prueba (cuando aplica)
- Panel de salida del comando generado
- Botones de acción (Copy, Execute, Save Config)
"""

import customtkinter as ctk
from tkinter import messagebox
import pyperclip
import subprocess
import sys
from pathlib import Path
from typing import Dict, Any, Optional

# Agregar carpeta padre al path para imports
current_dir = Path(__file__).parent.parent
if str(current_dir) not in sys.path:
    sys.path.insert(0, str(current_dir))

from core.config_manager import ConfigManager
from core.case_mapper import CaseMapper
from core.command_builder import CommandBuilder


class MainWindow(ctk.CTk):
    """Ventana principal de la aplicación"""

    def __init__(self):
        super().__init__()

        # Configuración de la ventana
        self.title("Pytest Command Generator - Test Automation Suite")
        self.geometry("1400x1000")

        # Hacer la ventana maximizable y con scroll
        self.resizable(True, True)

        # Inicializar componentes core
        self.config_manager = ConfigManager()
        self.case_mapper = CaseMapper(self.config_manager)
        self.command_builder = CommandBuilder(self.config_manager, self.case_mapper)

        # Variables de estado
        self.current_case_id = None
        self.parameter_widgets = {}  # {parameter_name: widget}
        self.pytest_flag_vars = {}   # {flag_name: BooleanVar}
        self.testdata_widgets = {}   # {field_path: widget}

        # Configurar tema
        ctk.set_appearance_mode("dark")  # Default: dark mode
        ctk.set_default_color_theme("blue")

        # Crear interfaz
        self._create_ui()

        # Cargar primer caso por defecto
        self._load_first_case()

    def _create_ui(self):
        """Crea la interfaz de usuario completa"""

        # ============ HEADER ============
        self._create_header()

        # ============ MAIN CONTENT ============
        # Frame principal con dos columnas
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill="both", expand=True, padx=20, pady=(5, 10))

        # Columna izquierda: Parámetros
        left_column = ctk.CTkFrame(main_frame)
        left_column.pack(side="left", fill="both", expand=True, padx=(0, 10))

        self._create_parameters_panel(left_column)

        # Columna derecha: Test Data
        right_column = ctk.CTkFrame(main_frame)
        right_column.pack(side="right", fill="both", expand=True, padx=(10, 0))

        self._create_testdata_panel(right_column)

        # ============ FOOTER ============
        self._create_command_output_panel()

    def _create_header(self):
        """Crea el encabezado con selector de caso, flags y botones de acción"""
        header_frame = ctk.CTkFrame(self, height=160)
        header_frame.pack(fill="x", padx=20, pady=15)

        # ========== COLUMNA DERECHA - BOTONES ==========
        right_section = ctk.CTkFrame(header_frame)
        right_section.pack(side="right", fill="y", padx=(10, 10))

        # Título de botones
        ctk.CTkLabel(
            right_section,
            text="Actions",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(pady=(10, 5))

        # Botón Copy
        ctk.CTkButton(
            right_section,
            text="📋 Copy Command",
            command=self._copy_command,
            width=200,
            height=32,
            font=ctk.CTkFont(size=12, weight="bold")
        ).pack(pady=3)

        # Botón Execute
        ctk.CTkButton(
            right_section,
            text="▶️ Execute Command",
            command=self._execute_command,
            width=200,
            height=32,
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color="green",
            hover_color="darkgreen"
        ).pack(pady=3)

        # Botón Save Config
        ctk.CTkButton(
            right_section,
            text="💾 Save Config",
            command=self._save_configuration,
            width=200,
            height=32,
            font=ctk.CTkFont(size=12, weight="bold")
        ).pack(pady=3)

        # Botón de tema (más pequeño)
        self.theme_button = ctk.CTkButton(
            right_section,
            text="🌙 Dark",
            command=self._toggle_theme,
            width=100,
            height=28,
            font=ctk.CTkFont(size=11)
        )
        self.theme_button.pack(pady=(5, 5))

        # ========== COLUMNA PYTEST FLAGS (DERECHA, ANTES DE ACTIONS) ==========
        flags_section = ctk.CTkFrame(header_frame, width=220)
        flags_section.pack(side="right", fill="y", expand=False, padx=(10, 5))

        # Título de flags
        ctk.CTkLabel(
            flags_section,
            text="🚩 Pytest Flags",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(anchor="w", pady=(10, 5), padx=10)

        # Crear checkboxes de flags
        self._create_pytest_flags(flags_section)

        # ========== COLUMNA IZQUIERDA (SE EXPANDE) ==========
        left_section = ctk.CTkFrame(header_frame)
        left_section.pack(side="left", fill="both", expand=True, padx=(10, 10))

        # Título
        title_label = ctk.CTkLabel(
            left_section,
            text="🧪 Pytest Command Generator",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.pack(anchor="w", pady=(10, 3))

        # Subtítulo
        subtitle_label = ctk.CTkLabel(
            left_section,
            text="Configure test parameters and generate pytest commands",
            font=ctk.CTkFont(size=11),
            text_color="gray"
        )
        subtitle_label.pack(anchor="w", pady=(0, 10))

        # Selector de caso
        case_frame = ctk.CTkFrame(left_section, fg_color="transparent")
        case_frame.pack(anchor="w", pady=5)

        ctk.CTkLabel(
            case_frame,
            text="Select Test Case:",
            font=ctk.CTkFont(size=13, weight="bold")
        ).pack(side="left", padx=(0, 10))

        # Obtener lista de casos
        cases = self.config_manager.get_all_cases()
        case_names = list(cases.values())

        self.case_selector = ctk.CTkComboBox(
            case_frame,
            values=case_names,
            command=self._on_case_changed,
            width=350,
            font=ctk.CTkFont(size=13)
        )
        self.case_selector.pack(side="left")

    def _create_parameters_panel(self, parent):
        """Crea el panel de parámetros"""
        # Título
        title = ctk.CTkLabel(
            parent,
            text="⚙️ Test Parameters",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        title.pack(pady=(10, 5), anchor="w", padx=20)

        # Frame scrollable para parámetros
        self.params_scroll = ctk.CTkScrollableFrame(parent, height=520)
        self.params_scroll.pack(fill="both", expand=True, padx=10, pady=10)

    def _create_pytest_flags(self, parent):
        """Crea checkboxes para flags de pytest"""
        flags = [
            ("verbose", "Verbose (-v)", True),
            ("show_prints", "Show Prints (-s)", False),
            ("stop_on_first_failure", "Stop on Fail (-x)", False),
            ("allure_report", "Allure Report", False),
            ("parallel_execution", "Parallel (-n auto)", False)
        ]

        for flag_name, label, default in flags:
            var = ctk.BooleanVar(value=default)
            self.pytest_flag_vars[flag_name] = var

            checkbox = ctk.CTkCheckBox(
                parent,
                text=label,
                variable=var,
                command=self._update_command,
                font=ctk.CTkFont(size=11)
            )
            checkbox.pack(anchor="w", padx=15, pady=2)

    def _create_testdata_panel(self, parent):
        """Crea el panel de datos de prueba"""
        # Título
        title = ctk.CTkLabel(
            parent,
            text="📋 Test Data",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        title.pack(pady=(10, 5), anchor="w", padx=20)

        # Frame scrollable para test data
        self.testdata_scroll = ctk.CTkScrollableFrame(parent, height=500)
        self.testdata_scroll.pack(fill="both", expand=True, padx=10, pady=10)

    def _create_command_output_panel(self):
        """Crea el panel de salida del comando"""
        output_frame = ctk.CTkFrame(self, height=150)
        output_frame.pack(fill="x", padx=20, pady=(10, 20))

        # Título
        title = ctk.CTkLabel(
            output_frame,
            text="📟 Generated Command",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        title.pack(pady=(10, 5), anchor="w", padx=20)

        # Textbox para el comando
        self.command_textbox = ctk.CTkTextbox(
            output_frame,
            height=90,
            font=ctk.CTkFont(family="Consolas", size=11)
        )
        self.command_textbox.pack(fill="both", padx=20, pady=(5, 15))

    def _load_first_case(self):
        """Carga el primer caso disponible al iniciar"""
        # Intentar cargar la sesión actual desde testdata.json
        current_session = self.config_manager.load_current_session()

        if current_session:
            # Cargar sesión guardada
            self._load_session(current_session)
        else:
            # Si no hay sesión, cargar el primer caso por defecto
            cases = self.config_manager.get_all_cases()
            if cases:
                first_case_name = list(cases.values())[0]
                self.case_selector.set(first_case_name)
                self._on_case_changed(first_case_name)

    def _on_case_changed(self, selected_case_name: str):
        """Callback cuando cambia el caso seleccionado"""
        # Encontrar case_id basándose en el nombre
        cases = self.config_manager.get_all_cases()
        case_id = None
        for cid, cname in cases.items():
            if cname == selected_case_name:
                case_id = cid
                break

        if not case_id:
            return

        self.current_case_id = case_id

        # Actualizar parámetros
        self._update_parameters_panel()

        # Actualizar test data
        self._update_testdata_panel()

        # Actualizar comando
        self._update_command()

    def _update_parameters_panel(self):
        """Actualiza el panel de parámetros según el caso seleccionado"""
        # Limpiar widgets existentes
        for widget in self.params_scroll.winfo_children():
            widget.destroy()
        self.parameter_widgets.clear()

        if not self.current_case_id:
            return

        # Obtener parámetros aplicables
        applicable_params = self.case_mapper.get_applicable_parameters(self.current_case_id)

        # Crear widgets para cada parámetro
        row = 0
        for param_name in applicable_params:
            label_text = self.case_mapper.get_parameter_label(param_name)
            param_type = self.case_mapper.get_parameter_type(param_name)

            # Label
            label = ctk.CTkLabel(
                self.params_scroll,
                text=label_text,
                font=ctk.CTkFont(size=13, weight="bold")
            )
            label.grid(row=row, column=0, sticky="w", padx=10, pady=10)

            # Widget según tipo
            if param_type == "dropdown":
                if param_name in ["origin", "destination"]:
                    # Dropdown de ciudades
                    cities = self.config_manager.get_parameter_options("cities")
                    city_names = [city["display_name"] for city in cities.values()]
                    widget = ctk.CTkComboBox(
                        self.params_scroll,
                        values=city_names,
                        command=lambda _: self._update_command(),
                        width=300
                    )
                    widget.set(city_names[0] if city_names else "")
                else:
                    # Dropdown normal
                    options = self.config_manager.get_parameter_display_values(param_name)
                    widget = ctk.CTkComboBox(
                        self.params_scroll,
                        values=options,
                        command=lambda _: self._update_command(),
                        width=300
                    )
                    widget.set(options[0] if options else "")

            elif param_type == "number":
                # Entry numérico
                widget = ctk.CTkEntry(
                    self.params_scroll,
                    width=300,
                    placeholder_text="Enter number of days"
                )
                default_value = "4" if param_name == "departure-days" else "5"
                widget.insert(0, default_value)
                widget.bind("<KeyRelease>", lambda e: self._update_command())

            else:
                # Entry de texto
                widget = ctk.CTkEntry(
                    self.params_scroll,
                    width=300
                )
                widget.bind("<KeyRelease>", lambda e: self._update_command())

            widget.grid(row=row, column=1, sticky="w", padx=10, pady=10)
            self.parameter_widgets[param_name] = widget

            row += 1

    def _update_testdata_panel(self):
        """Actualiza el panel de datos de prueba"""
        # Limpiar widgets existentes
        for widget in self.testdata_scroll.winfo_children():
            widget.destroy()
        self.testdata_widgets.clear()

        if not self.current_case_id:
            return

        # Verificar si el caso requiere test data
        if not self.case_mapper.requires_testdata(self.current_case_id):
            no_data_label = ctk.CTkLabel(
                self.testdata_scroll,
                text="This test case does not require test data",
                font=ctk.CTkFont(size=13),
                text_color="gray"
            )
            no_data_label.pack(pady=20)
            return

        # Cargar test data
        testdata = self.config_manager.load_testdata()

        # Secciones a mostrar
        sections = self.case_mapper.get_testdata_sections(self.current_case_id)

        row = 0

        # Passengers section
        if "passengers" in sections:
            self._create_passengers_section(testdata.get("passengers", {}), row)
            row += 50

        # Payment section
        if "payment" in sections:
            self._create_payment_section(testdata.get("payment", {}), row)
            row += 20

        # Billing section
        if "billing" in sections:
            self._create_billing_section(testdata.get("billing", {}), row)

    def _create_passengers_section(self, passengers_data: Dict, start_row: int):
        """Crea la sección de pasajeros"""
        section_label = ctk.CTkLabel(
            self.testdata_scroll,
            text="👥 Passengers",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        section_label.grid(row=start_row, column=0, columnspan=2, sticky="w", padx=10, pady=(10, 5))

        passenger_types = ["adult", "teen", "child", "infant"]
        row = start_row + 1

        for ptype in passenger_types:
            pdata = passengers_data.get(ptype, {})

            # Subtítulo del tipo de pasajero
            type_label = ctk.CTkLabel(
                self.testdata_scroll,
                text=ptype.capitalize(),
                font=ctk.CTkFont(size=14, weight="bold"),
                text_color="#4A9EFF"
            )
            type_label.grid(row=row, column=0, columnspan=2, sticky="w", padx=20, pady=(10, 5))
            row += 1

            # Campos del pasajero
            for field, value in pdata.items():
                field_label = ctk.CTkLabel(
                    self.testdata_scroll,
                    text=field.replace("_", " ").title(),
                    font=ctk.CTkFont(size=12)
                )
                field_label.grid(row=row, column=0, sticky="w", padx=30, pady=3)

                entry = ctk.CTkEntry(
                    self.testdata_scroll,
                    width=250
                )
                entry.insert(0, str(value))
                entry.grid(row=row, column=1, sticky="w", padx=10, pady=3)

                # Guardar referencia
                self.testdata_widgets[f"passengers.{ptype}.{field}"] = entry

                row += 1

    def _create_payment_section(self, payment_data: Dict, start_row: int):
        """Crea la sección de pago"""
        section_label = ctk.CTkLabel(
            self.testdata_scroll,
            text="💳 Payment",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        section_label.grid(row=start_row, column=0, columnspan=2, sticky="w", padx=10, pady=(15, 5))

        row = start_row + 1

        for field, value in payment_data.items():
            field_label = ctk.CTkLabel(
                self.testdata_scroll,
                text=field.replace("_", " ").title(),
                font=ctk.CTkFont(size=12)
            )
            field_label.grid(row=row, column=0, sticky="w", padx=20, pady=3)

            entry = ctk.CTkEntry(
                self.testdata_scroll,
                width=250
            )
            entry.insert(0, str(value))
            entry.grid(row=row, column=1, sticky="w", padx=10, pady=3)

            self.testdata_widgets[f"payment.{field}"] = entry

            row += 1

    def _create_billing_section(self, billing_data: Dict, start_row: int):
        """Crea la sección de facturación"""
        section_label = ctk.CTkLabel(
            self.testdata_scroll,
            text="📬 Billing",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        section_label.grid(row=start_row, column=0, columnspan=2, sticky="w", padx=10, pady=(15, 5))

        row = start_row + 1

        for field, value in billing_data.items():
            field_label = ctk.CTkLabel(
                self.testdata_scroll,
                text=field.replace("_", " ").title(),
                font=ctk.CTkFont(size=12)
            )
            field_label.grid(row=row, column=0, sticky="w", padx=20, pady=3)

            entry = ctk.CTkEntry(
                self.testdata_scroll,
                width=250
            )
            entry.insert(0, str(value))
            entry.grid(row=row, column=1, sticky="w", padx=10, pady=3)

            self.testdata_widgets[f"billing.{field}"] = entry

            row += 1

    def _update_command(self):
        """Actualiza el comando generado"""
        if not self.current_case_id:
            return

        # Obtener valores de parámetros
        selected_params = {}
        for param_name, widget in self.parameter_widgets.items():
            if isinstance(widget, ctk.CTkComboBox):
                selected_params[param_name] = widget.get()
            elif isinstance(widget, ctk.CTkEntry):
                selected_params[param_name] = widget.get()

        # Obtener flags de pytest
        pytest_flags = {
            name: var.get()
            for name, var in self.pytest_flag_vars.items()
        }

        # Generar comando
        command = self.command_builder.build_multiline_command(
            self.current_case_id,
            selected_params,
            pytest_flags
        )

        # Actualizar textbox
        self.command_textbox.delete("1.0", "end")
        self.command_textbox.insert("1.0", command)

    def _copy_command(self):
        """Copia el comando al portapapeles"""
        command = self.command_textbox.get("1.0", "end").strip()
        if command:
            # Convertir a una sola línea (quitar backslashes y saltos de línea)
            single_line = command.replace(" \\\n", " ").replace("\n", " ")
            pyperclip.copy(single_line)
            messagebox.showinfo("Success", "Command copied to clipboard!")
        else:
            messagebox.showwarning("Warning", "No command to copy")

    def _execute_command(self):
        """Ejecuta el comando pytest"""
        command = self.command_textbox.get("1.0", "end").strip()
        if not command:
            messagebox.showwarning("Warning", "No command to execute")
            return

        # Convertir a una sola línea
        single_line = command.replace(" \\\n", " ").replace("\n", " ")

        # Confirmar ejecución
        response = messagebox.askyesno(
            "Execute Command",
            f"Execute this command?\n\n{single_line[:100]}..."
        )

        if response:
            try:
                # Ejecutar en una nueva terminal (Windows)
                subprocess.Popen(
                    f'start cmd /k "{single_line}"',
                    shell=True
                )
                messagebox.showinfo("Success", "Command launched in new terminal window")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to execute command:\n{str(e)}")

    def _save_configuration(self):
        """Guarda TODO el estado de la aplicación en testdata.json"""
        if not self.current_case_id:
            messagebox.showwarning("Warning", "No case selected")
            return

        # Recopilar parámetros
        parameters = {
            name: widget.get()
            for name, widget in self.parameter_widgets.items()
        }

        # Recopilar pytest flags
        pytest_flags = {
            name: var.get()
            for name, var in self.pytest_flag_vars.items()
        }

        # Recopilar test data
        testdata = {
            "passengers": {"adult": {}, "teen": {}, "child": {}, "infant": {}},
            "payment": {},
            "billing": {}
        }

        for field_path, widget in self.testdata_widgets.items():
            parts = field_path.split(".")
            value = widget.get()

            if parts[0] == "passengers":
                testdata["passengers"][parts[1]][parts[2]] = value
            elif parts[0] == "payment":
                testdata["payment"][parts[1]] = value
            elif parts[0] == "billing":
                testdata["billing"][parts[1]] = value

        # Guardar TODO en testdata.json
        self.config_manager.save_complete_state(
            self.current_case_id,
            parameters,
            pytest_flags,
            testdata
        )

        messagebox.showinfo("Success", "All configuration saved to testdata.json")

    def _load_session(self, session_data: dict):
        """
        Carga una sesión guardada y aplica los valores a la UI

        Args:
            session_data: Diccionario con case_id, parameters, pytest_flags
        """
        # Obtener datos de la sesión
        case_id = session_data.get("case_id")
        parameters = session_data.get("parameters", {})
        pytest_flags = session_data.get("pytest_flags", {})

        if not case_id:
            return

        # Encontrar el nombre del caso
        cases = self.config_manager.get_all_cases()
        case_name = cases.get(case_id)

        if not case_name:
            return

        # Establecer el caso en el selector
        self.case_selector.set(case_name)
        self.current_case_id = case_id

        # Actualizar parámetros y test data
        self._update_parameters_panel()
        self._update_testdata_panel()

        # Aplicar valores de parámetros guardados
        for param_name, param_value in parameters.items():
            if param_name in self.parameter_widgets:
                widget = self.parameter_widgets[param_name]
                if isinstance(widget, ctk.CTkComboBox):
                    widget.set(param_value)
                elif isinstance(widget, ctk.CTkEntry):
                    widget.delete(0, "end")
                    widget.insert(0, param_value)

        # Aplicar valores de pytest flags guardados
        for flag_name, flag_value in pytest_flags.items():
            if flag_name in self.pytest_flag_vars:
                self.pytest_flag_vars[flag_name].set(flag_value)

        # Actualizar comando generado
        self._update_command()

    def _toggle_theme(self):
        """Alterna entre tema claro y oscuro"""
        current_mode = ctk.get_appearance_mode()
        if current_mode == "Dark":
            ctk.set_appearance_mode("light")
            self.theme_button.configure(text="☀️ Light Mode")
        else:
            ctk.set_appearance_mode("dark")
            self.theme_button.configure(text="🌙 Dark Mode")
