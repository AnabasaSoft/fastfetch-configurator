#!/usr/bin/env python

import sys
import subprocess
import shutil
import platform
import json
import tempfile
from ansi2html import Ansi2HTMLConverter
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QTabWidget, QWidget,
                                 QVBoxLayout, QPushButton, QLabel, QCheckBox,
                                 QTextEdit, QMessageBox, QFileDialog,
                                 QDialog, QListWidget, QComboBox,
                                 QDialogButtonBox, QAbstractItemView, QLineEdit, QHBoxLayout,
                                 QTreeWidget, QTreeWidgetItem, QSpinBox, QInputDialog,
                                 QListWidgetItem)
from PyQt6.QtGui import QFont, QAction, QIcon
from PyQt6.QtCore import Qt
import locale

# --- MOTOR DE TRADUCCIÓN AUTOMÁTICO ---
# Detecta el idioma del SO. Si empieza por 'es', usa español, si no, fallback a inglés.
try:
    locale.setlocale(locale.LC_ALL, '')
    loc, _ = locale.getlocale()
except Exception:
    loc = None

if not loc:
    loc = os.environ.get('LANG', 'en')

IDIOMA = "es" if loc and loc.startswith("es") else "en"

TEXTOS = {
    "en": {
        "Configurador de Fastfetch": "Fastfetch Configurator",
        "1. Instalación": "1. Installation",
        "2. Configuración": "2. Configuration",
        "3. Vista Previa": "3. Preview",
        "Archivo": "File",
        "Nuevo": "New",
        "Cargar": "Load",
        "Cargar conf. instalada": "Load installed conf.",
        "Guardar": "Save",
        "Guardar como...": "Save as...",
        "Comprobando estado de fastfetch...": "Checking fastfetch status...",
        "Instalar fastfetch": "Install fastfetch",
        "✅ ¡Fastfetch ya está instalado en el sistema!": "✅ Fastfetch is already installed on the system!",
        "❌ Fastfetch NO está instalado.": "❌ Fastfetch is NOT installed.",
        "Secciones personalizadas:": "Custom sections:",
        "Añadir Sección": "Add Section",
        "Borrar Seleccionada": "Delete Selected",
        "Generar y Guardar config.jsonc": "Generate and Save config.jsonc",
        "Actualizar Vista Previa": "Refresh Preview",
        "Ver en Terminal Real": "View in Real Terminal",
        "Por favor, instala fastfetch primero en la pestaña 1.": "Please install fastfetch first in tab 1.",
        "Añadir Nueva Sección": "Add New Section",
        "Nombre de la sección (ej. SYSTEM, DESKTOP)": "Section name (e.g. SYSTEM, DESKTOP)",
        "Color de la sección (título y líneas):": "Section color (title and lines):",
        "Color de los resultados (valores):": "Results color (values):",
        "Modo Árbol (con líneas ├─ y └─)": "Tree Mode (with ├─ and └─ lines)",
        "Cuadrado cerrado alrededor de la sección": "Closed box around the section",
        "Módulos: Doble click para añadir. Arrastra en la lista derecha para reordenar.": "Modules: Double click to add. Drag in right list to reorder.",
        "Añadir ->": "Add ->",
        "<- Quitar": "<- Remove",
        "Base del Sistema": "System Base",
        "Hardware": "Hardware",
        "Recursos": "Resources",
        "Pantalla y Gráficos": "Display & Graphics",
        "Entorno de Escritorio": "Desktop Environment",
        "Terminal y Consola": "Terminal & Console",
        "Red e Internet": "Network & Internet",
        "Periféricos y Dispositivos": "Peripherals & Devices",
        "Multimedia": "Multimedia",
        "Sistemas de Archivos": "File Systems",
        "Varios / Formato": "Misc / Format",
        "Verde (32)": "Green (32)",
        "Amarillo (33)": "Yellow (33)",
        "Azul (34)": "Blue (34)",
        "Magenta (35)": "Magenta (35)",
        "Cian (36)": "Cyan (36)",
        "Rojo (31)": "Red (31)",
        "Blanco (37)": "White (37)",
        "Por defecto (0)": "Default (0)",
        "Gris (90)": "Gray (90)",
        "Logo del sistema (Izquierda):": "System Logo (Left):",
        "Auto (Grande)": "Auto (Big)",
        "Pequeño (Small)": "Small",
        "Oculto (None)": "Hidden (None)",
        "Ancho del cuadrado (columnas):": "Box width (columns):",
        "Márgenes del Logo (Arriba / Izq / Der):": "Logo Padding (Top / Left / Right):",
        "Recuadro Global alrededor de todo": "Global Box around everything",
        "Título del recuadro (opcional):": "Box title (optional):",
        "Imagen Personalizada": "Custom Image",
        "Seleccionar Imagen": "Select Image",
        "Ancho (col):": "Width (col):",
        "Izquierda": "Left",
        "Centro": "Center",
        "Derecha": "Right",

        # Tooltips de los módulos
        "Nombre y versión del sistema operativo": "Operating system name and version",
        "Modelo, placa base o producto de tu equipo": "Computer model, motherboard or product name",
        "Versión del núcleo de Linux": "Linux kernel version",
        "Sistema de inicio (systemd, openrc...)": "Init system (systemd, openrc...)",
        "Tiempo que lleva encendido el PC": "Time the PC has been running",
        "Número total de paquetes instalados": "Total number of installed packages",
        "Idioma y región del sistema": "System language and region",
        "Fecha y hora actual": "Current date and time",
        "Usuarios conectados actualmente": "Currently logged in users",
        "Usuario @ Hostname": "User @ Hostname",
        "Información detallada de la placa base": "Detailed motherboard information",
        "Información y versión de la BIOS/UEFI": "BIOS/UEFI version and information",
        "Gestor de arranque (GRUB, systemd-boot...)": "Boot manager (GRUB, systemd-boot...)",
        "Tipo de chasis (portátil, sobremesa, etc.)": "Chassis type (laptop, desktop, etc.)",
        "Módulo de plataforma segura (chip TPM)": "Trusted Platform Module (TPM chip)",
        "Nombre, núcleos y frecuencia del procesador": "Processor name, cores, and frequency",
        "Tamaño de la memoria caché del procesador": "Processor cache memory size",
        "Tarjeta gráfica y sus controladores": "Graphics card and its drivers",
        "Hardware físico de los discos duros": "Physical hard drive hardware",
        "Módulos físicos de memoria RAM instalados": "Installed physical RAM modules",
        "Porcentaje de uso actual de la CPU": "Current CPU usage percentage",
        "Uso de la memoria RAM": "RAM memory usage",
        "Uso de la memoria de intercambio (Swap)": "Swap memory usage",
        "Espacio usado/total en las particiones de disco": "Used/total space on disk partitions",
        "Velocidad de lectura/escritura actual de los discos": "Current disk read/write speed",
        "Carga media del sistema": "System load average",
        "Cantidad de procesos en ejecución": "Number of running processes",
        "Resolución y frecuencia de refresco de los monitores": "Monitors resolution and refresh rate",
        "Igual que Display (Monitor principal)": "Same as Display (Main monitor)",
        "Nivel de brillo actual de la pantalla": "Current screen brightness level",
        "Versión soportada de la API OpenCL": "Supported OpenCL API version",
        "Versión soportada de la API OpenGL": "Supported OpenGL API version",
        "Versión soportada de la API Vulkan": "Supported Vulkan API version",
        "Entorno de escritorio (Plasma, GNOME, XFCE...)": "Desktop environment (Plasma, GNOME, XFCE...)",
        "Gestor de ventanas (KWin, Mutter, i3...)": "Window manager (KWin, Mutter, i3...)",
        "Tema aplicado al gestor de ventanas": "Theme applied to the window manager",
        "Tema global del entorno de escritorio": "Global desktop environment theme",
        "Tema de iconos actual": "Current icon theme",
        "Tema del cursor del ratón": "Mouse cursor theme",
        "Fuentes principales configuradas en el sistema": "Main fonts configured in the system",
        "Ruta del fondo de pantalla actual": "Current wallpaper path",
        "Gestor de inicio de sesión (SDDM, GDM, LightDM...)": "Login manager (SDDM, GDM, LightDM...)",
        "Intérprete de comandos (Bash, Zsh, Fish...)": "Command interpreter (Bash, Zsh, Fish...)",
        "Emulador de terminal (Konsole, Alacritty...)": "Terminal emulator (Konsole, Alacritty...)",
        "Fuente tipográfica usada en la terminal": "Font used in the terminal",
        "Dimensiones de la ventana (columnas x filas)": "Window dimensions (columns x rows)",
        "Colores del tema de la terminal": "Terminal theme colors",
        "Muestra una paleta con los colores de la terminal": "Displays a palette with the terminal colors",
        "Editor de texto por defecto del sistema": "System's default text editor",
        "Dirección IP en tu red local (IPv4/IPv6)": "IP address on your local network (IPv4/IPv6)",
        "Dirección IP pública en Internet": "Public IP address on the Internet",
        "Servidores DNS configurados en la red": "DNS servers configured on the network",
        "Información de la red Wi-Fi conectada": "Connected Wi-Fi network information",
        "Tráfico de red actual (subida y bajada)": "Current network traffic (upload and download)",
        "Dispositivos Bluetooth conectados": "Connected Bluetooth devices",
        "Adaptadores Bluetooth de tu equipo": "Bluetooth adapters on your computer",
        "Cámaras conectadas o detectadas": "Connected or detected cameras",
        "Mandos de juego conectados": "Connected gamepads",
        "Teclados conectados": "Connected keyboards",
        "Ratones conectados": "Connected mice",
        "Dispositivos de audio y nivel de volumen": "Audio devices and volume level",
        "Información del cargador (vataje)": "Power adapter information (wattage)",
        "Nivel, salud y estado de la batería": "Battery level, health, and status",
        "Canción o vídeo que se está reproduciendo": "Currently playing song or video",
        "Reproductor multimedia activo actualmente": "Currently active media player",
        "Información de volúmenes y particiones BTRFS": "BTRFS volumes and partitions information",
        "Información de volúmenes de almacenamiento ZFS": "ZFS storage volumes information",
        "Inserta una línea en blanco para dar espacio": "Inserts a blank line to add space",
        "Dibuja una línea punteada separadora": "Draws a dotted separator line",
        "Permite añadir texto puro o etiquetas personalizadas": "Allows adding pure text or custom labels",
        "Ejecuta y muestra la salida de un script o comando bash": "Executes and displays the output of a bash script or command",
        "Versión instalada de Fastfetch": "Installed Fastfetch version",
        "Temperatura y clima local actual": "Current local weather and temperature",
        "Módulo de Fastfetch": "Fastfetch Module",

        # Textos de los diálogos de configuración
        "Configurar Command": "Configure Command",
        "Comando a ejecutar (ej. pacman -Qq | wc -l):": "Command to execute (e.g. pacman -Qq | wc -l):",
        "Configurar Weather": "Configure Weather",
        "Ciudad para el clima (ej. Madrid, London):": "City for weather (e.g. Madrid, London):",
        "Configurar Disk": "Configure Disk",
        "Ruta del disco (ej. / o /home):": "Disk path (e.g. / or /home):",
        "Configurar Custom": "Configure Custom Text",
        "Texto personalizado a mostrar:": "Custom text to display:",
        "Editar Sección": "Edit Section",
        "Usar iconos (Nerd Fonts)": "Use icons (Nerd Fonts)",
        "Icono y Nombre de la sección:": "Section Icon and Name:",
        "Color del icono de la sección:": "Section icon color:",
        "Color de iconos:": "Icons color:",
        "Mismo que el título (0)": "Same as title (0)",
        "Color del icono independiente:": "Independent icon color:",
        "Editar Módulo": "Edit Module",
        "Módulo": "Module",
        "Añadir barra de progreso": "Add progress bar",
        "Color Lleno (Inicial):": "Filled Color (Start):",
        "Color Vacío (Final):": "Empty Color (End):",
        "Formato Personalizado (avanzado, ej: {1} / {2}):": "Custom Format (advanced, e.g: {1} / {2}):",
        "Scripts de Paquetes": "Package Scripts",
        "Nombre a mostrar (opcional):": "Display name (optional):",
        "Color Barra (Lleno / Vacío):": "Bar Color (Filled / Empty):",
        "Automático (Dinámico)": "Automatic (Dynamic)",
        "Caracteres Barra (Lleno / Vacío):": "Bar Chars (Filled / Empty):",
        "¿Cargar plantilla?": "Load template?",
        "Esto borrará tu configuración actual. ¿Deseas continuar?": "This will erase your current configuration. Do you want to continue?",
        "Integración con la Terminal:": "Terminal Integration:",
        "Arrancar fastfetch al abrir la terminal (.bashrc / .zshrc)": "Run fastfetch when opening the terminal (.bashrc / .zshrc)",
        "Ya tienes fastfetch configurado en tu": "You already have fastfetch configured in your",
        "Se ha añadido fastfetch al final de tu": "Fastfetch has been added to the end of your",
        "Plantillas Predefinidas:": "Predefined Templates:",
        "Cargar Plantilla": "Load Template",
        "Cyberpunk (Neón y Cajas)": "Cyberpunk (Neon & Boxes)",
        "Minimalista (Sin bordes)": "Minimalist (No borders)",
        "Mac-Style (Limpio)": "Mac-Style (Clean)",
        "Dracula (Neón Oscuro)": "Dracula (Dark Neon)",
        "Terminal Retro (Hacker)": "Retro Terminal (Hacker)",
        "Catppuccin (Pastel y Bloques)": "Catppuccin (Pastel & Blocks)",
        "Espaciado superior inicial (líneas):": "Initial top spacing (lines):",
        "Espaciado entre secciones (líneas):": "Spacing between sections (lines):",
        "Aviso": "Warning",
        "Error": "Error",
        "Éxito": "Success",
        "Información": "Information",
        "Cargar configuración": "Load configuration",
        "Guardar configuración": "Save configuration",
        "Configuración cargada correctamente.": "Configuration loaded successfully.",
        "Configuración guardada correctamente.": "Configuration saved successfully.",
        "No se pudo cargar el archivo:": "Could not load file:",
        "No se pudo guardar el archivo:": "Could not save file:",
        "No se encontró ni .bashrc ni .zshrc en tu directorio personal.": "Neither .bashrc nor .zshrc were found in your home directory.",
        "No se pudo instalar fastfetch. Operación cancelada o fallida.": "Could not install fastfetch. Operation canceled or failed.",
        "Falta una herramienta necesaria para instalar (ej. winget, brew o pkexec en Linux).": "Missing a required tool for installation (e.g. winget, brew or pkexec on Linux).",
        "No se encontró un emulador de terminal compatible (konsole, gnome-terminal, etc).": "No compatible terminal emulator found (konsole, gnome-terminal, etc).",
        "No se pudo abrir la terminal:": "Could not open terminal:",
        "Error al ejecutar fastfetch:": "Error executing fastfetch:",
        "Ej: Disco Raíz": "e.g. Root Disk"
    }
}

def tr(texto):
    if IDIOMA == "es":
        return texto
    return TEXTOS.get(IDIOMA, {}).get(texto, texto)

def resource_path(relative_path):
    """
    Obtiene la ruta absoluta al recurso.
    Funciona tanto en desarrollo como al compilar con PyInstaller.
    """
    try:
        # PyInstaller crea una carpeta temporal y guarda la ruta en _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)

class DialogoEditarModulo(QDialog):
    def __init__(self, mod_dict, parent=None):
        super().__init__(parent)
        self.setWindowTitle(tr("Editar Módulo"))
        self.resize(350, 250)
        layout = QVBoxLayout()

        self.mod_type = mod_dict.get("type", "unknown")
        layout.addWidget(QLabel(f"{tr('Módulo')}: {self.mod_type.capitalize()}"))

        # Nombre a mostrar (opcional)
        layout.addWidget(QLabel(tr("Nombre a mostrar (opcional):")))
        self.txt_custom_name = QLineEdit()
        self.txt_custom_name.setText(mod_dict.get("custom_text", ""))
        self.txt_custom_name.setPlaceholderText(tr("Ej: Disco Raíz"))
        layout.addWidget(self.txt_custom_name)

        # Formato personalizado
        layout.addWidget(QLabel(tr("Formato Personalizado (avanzado, ej: {1} / {2}):")))
        self.txt_formato = QLineEdit()
        self.txt_formato.setText(mod_dict.get("format", ""))
        layout.addWidget(self.txt_formato)

        # 1. Color del icono independiente
        layout.addWidget(QLabel(tr("Color del icono independiente:")))
        self.cmb_color_icono = QComboBox()
        self.colores_lista = [
            "Por defecto (0)", "Gris (90)", "Rojo (31)", "Verde (32)",
            "Amarillo (33)", "Azul (34)", "Magenta (35)", "Cian (36)", "Blanco (37)"
        ]
        self.cmb_color_icono.addItems([tr(c) for c in self.colores_lista])

        color_str = mod_dict.get("icon_color", "0")
        self._set_combo_by_value(self.cmb_color_icono, color_str)
        layout.addWidget(self.cmb_color_icono)

        # Barra de progreso (Solo para compatibles)
        self.soporta_barra = self.mod_type in ["memory", "swap", "disk", "battery", "cpuusage", "player", "brightness"]
        if self.soporta_barra:
            layout.addSpacing(10)
            self.chk_barra = QCheckBox(tr("Añadir barra de progreso"))
            self.chk_barra.setChecked(mod_dict.get("usar_barra", False))
            layout.addWidget(self.chk_barra)

        botones = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        botones.accepted.connect(self.accept)
        botones.rejected.connect(self.reject)
        layout.addWidget(botones)
        self.setLayout(layout)

    def _set_combo_by_value(self, combo, val):
        for i in range(combo.count()):
            if f"({val})" in combo.itemText(i):
                combo.setCurrentIndex(i)
                break

    def obtener_datos_modulo(self):
        datos = {
            "icon_color": self.cmb_color_icono.currentText().split("(")[1].replace(")", "")
        }

        nombre = self.txt_custom_name.text().strip()
        if nombre:
            datos["custom_text"] = nombre
        else:
            datos["custom_text"] = ""

        formato = self.txt_formato.text().strip()
        if formato:
            datos["format"] = formato
        else:
            datos["format"] = ""

        if self.soporta_barra:
            datos["usar_barra"] = self.chk_barra.isChecked()

        return datos

class DialogoNuevaSeccion(QDialog):
    def __init__(self, parent=None, datos_edicion=None):
        super().__init__(parent)
        self.setWindowTitle(tr("Editar Sección") if datos_edicion else tr("Añadir Nueva Sección"))
        self.resize(500, 450)
        layout = QVBoxLayout()

        # Título e Icono
        layout.addWidget(QLabel(tr("Icono y Nombre de la sección:")))
        layout_titulo = QHBoxLayout()

        self.cmb_icono_titulo = QComboBox()
       # Lista de iconos predefinidos (Icono + Descripción)
        iconos_lista = [
            "󰪥 (Punto)", " (Linux)", " (Manjaro)", "󰣇 (Arch)",
            " (Debian)", " (Ubuntu)", " (Fedora)", " (Mint)",
            "󰒋 (Host/Servidor)", "󰌢 (PC/Chasis)", "󰌽 (Kernel)", "󰅐 (Uptime)",
            "󰏖 (Paquetes)", " (Idioma)", "󰃰 (Reloj)", " (Usuario)",
            " (CPU)", "󰢮 (GPU)", " (RAM)", "󰍛 (Memoria)", "󰓡 (Swap)",
            "󰋊 (Disco)", "󰍹 (Monitor)", "󰃠 (Brillo)", "󰧨 (Escritorio)",
            " (Gestor Ventanas)", "󰉼 (Tema)", "󰀻 (Iconos)", "󰆽 (Cursor)",
            " (Fuente)", "󰸉 (Fondo)", " (Terminal)", "󰏫 (Editor/Custom)",
            "󰩟 (IP Local)", "󰩠 (IP Pública)", " (Red/Wifi)", " (Bluetooth)",
            "󰄀 (Cámara)", "󰊗 (Mando)", "󰌌 (Teclado)", "󰍽 (Ratón)",
            "󰕾 (Sonido)", " (Enchufe)", " (Batería)", "󰝚 (Música)",
            "󰎆 (Reproductor)", " (Clima)", " (Engranaje)"
        ]
        self.cmb_icono_titulo.addItems(iconos_lista)
        # Permite elegir de la lista o borrar y pegar uno custom
        self.cmb_icono_titulo.setEditable(True)
        self.cmb_icono_titulo.setFixedWidth(130)
        layout_titulo.addWidget(self.cmb_icono_titulo)

        self.txt_nombre = QLineEdit()
        self.txt_nombre.setPlaceholderText(tr("Nombre de la sección (ej. SYSTEM, DESKTOP)"))
        layout_titulo.addWidget(self.txt_nombre)
        layout.addLayout(layout_titulo)

        # Color del icono del título
        layout.addWidget(QLabel(tr("Color del icono de la sección:")))
        self.cmb_color_icono_titulo = QComboBox()
        self.cmb_color_icono_titulo.addItems([tr(c) for c in [
            "Mismo que el título (0)", "Gris (90)", "Rojo (31)", "Verde (32)",
            "Amarillo (33)", "Azul (34)", "Magenta (35)", "Cian (36)", "Blanco (37)"
        ]])
        layout.addWidget(self.cmb_color_icono_titulo)

        # Color de la sección (título y líneas)
        layout.addWidget(QLabel(tr("Color de la sección (título y líneas):")))
        self.cmb_color = QComboBox()
        self.cmb_color.addItems([tr(c) for c in [
            "Verde (32)", "Amarillo (33)", "Azul (34)",
            "Magenta (35)", "Cian (36)", "Rojo (31)", "Blanco (37)"
        ]])
        layout.addWidget(self.cmb_color)

        # Color de los resultados
        layout.addWidget(QLabel(tr("Color de los resultados (valores):")))
        self.cmb_color_valores = QComboBox()
        self.cmb_color_valores.addItems([tr(c) for c in [
            "Por defecto (0)", "Gris (90)", "Rojo (31)", "Verde (32)",
            "Amarillo (33)", "Azul (34)", "Magenta (35)", "Cian (36)", "Blanco (37)"
        ]])
        layout.addWidget(self.cmb_color_valores)

        # Opciones visuales
        self.chk_arbol = QCheckBox(tr("Modo Árbol (con líneas ├─ y └─)"))
        self.chk_arbol.setChecked(True)
        layout.addWidget(self.chk_arbol)

        self.chk_cuadrado = QCheckBox(tr("Cuadrado cerrado alrededor de la sección"))
        layout.addWidget(self.chk_cuadrado)

        # Selector de módulos con vista de árbol
        layout.addWidget(QLabel(tr("Módulos: Doble click para añadir. Arrastra en la lista derecha para reordenar.")))
        layout_listas = QHBoxLayout()

        self.tree_disp = QTreeWidget()
        self.tree_disp.setHeaderHidden(True)

        categorias_modules = {
            "Base del Sistema": ["OS", "Host", "Kernel", "InitSystem", "Uptime", "Packages", "Locale", "DateTime", "Users", "Title"],
            "Hardware": ["Board", "BIOS", "Bootmgr", "Chassis", "TPM", "CPU", "CPUCache", "GPU", "PhysicalDisk", "PhysicalMemory"],
            "Recursos": ["CPUUsage", "Memory", "Swap", "Disk", "DiskIO", "Loadavg", "Processes"],
            "Pantalla y Gráficos": ["Display", "Monitor", "Brightness", "OpenCL", "OpenGL", "Vulkan"],
            "Entorno de Escritorio": ["DE", "WM", "WMTheme", "Theme", "Icons", "Cursor", "Font", "Wallpaper", "LM"],
            "Terminal y Consola": ["Shell", "Terminal", "TerminalFont", "TerminalSize", "TerminalTheme", "Colors", "Editor"],
            "Red e Internet": ["LocalIp", "PublicIp", "DNS", "Wifi", "NetIO"],
            "Periféricos y Dispositivos": ["Bluetooth", "BluetoothRadio", "Camera", "Gamepad", "Keyboard", "Mouse", "Sound", "PowerAdapter", "Battery"],
            "Multimedia": ["Media", "Player"],
            "Sistemas de Archivos": ["Btrfs", "Zpool"],
            "Scripts de Paquetes": ["Pacman", "AUR", "Flatpak", "Total_Pkgs"],
            "Varios / Formato": ["Break", "Separator", "Custom", "Command", "Version", "Weather"]
        }

        # Diccionario con las explicaciones de cada módulo
        descripciones = {
            "OS": "Nombre y versión del sistema operativo",
            "Host": "Modelo, placa base o producto de tu equipo",
            "Kernel": "Versión del núcleo de Linux",
            "InitSystem": "Sistema de inicio (systemd, openrc...)",
            "Uptime": "Tiempo que lleva encendido el PC",
            "Packages": "Número total de paquetes instalados",
            "Locale": "Idioma y región del sistema",
            "DateTime": "Fecha y hora actual",
            "Users": "Usuarios conectados actualmente",
            "Title": "Usuario @ Hostname",
            "Board": "Información detallada de la placa base",
            "BIOS": "Información y versión de la BIOS/UEFI",
            "Bootmgr": "Gestor de arranque (GRUB, systemd-boot...)",
            "Chassis": "Tipo de chasis (portátil, sobremesa, etc.)",
            "TPM": "Módulo de plataforma segura (chip TPM)",
            "CPU": "Nombre, núcleos y frecuencia del procesador",
            "CPUCache": "Tamaño de la memoria caché del procesador",
            "GPU": "Tarjeta gráfica y sus controladores",
            "PhysicalDisk": "Hardware físico de los discos duros",
            "PhysicalMemory": "Módulos físicos de memoria RAM instalados",
            "CPUUsage": "Porcentaje de uso actual de la CPU",
            "Memory": "Uso de la memoria RAM",
            "Swap": "Uso de la memoria de intercambio (Swap)",
            "Disk": "Espacio usado/total en las particiones de disco",
            "DiskIO": "Velocidad de lectura/escritura actual de los discos",
            "Loadavg": "Carga media del sistema",
            "Processes": "Cantidad de procesos en ejecución",
            "Display": "Resolución y frecuencia de refresco de los monitores",
            "Monitor": "Igual que Display (Monitor principal)",
            "Brightness": "Nivel de brillo actual de la pantalla",
            "OpenCL": "Versión soportada de la API OpenCL",
            "OpenGL": "Versión soportada de la API OpenGL",
            "Vulkan": "Versión soportada de la API Vulkan",
            "DE": "Entorno de escritorio (Plasma, GNOME, XFCE...)",
            "WM": "Gestor de ventanas (KWin, Mutter, i3...)",
            "WMTheme": "Tema aplicado al gestor de ventanas",
            "Theme": "Tema global del entorno de escritorio",
            "Icons": "Tema de iconos actual",
            "Cursor": "Tema del cursor del ratón",
            "Font": "Fuentes principales configuradas en el sistema",
            "Wallpaper": "Ruta del fondo de pantalla actual",
            "LM": "Gestor de inicio de sesión (SDDM, GDM, LightDM...)",
            "Shell": "Intérprete de comandos (Bash, Zsh, Fish...)",
            "Terminal": "Emulador de terminal (Konsole, Alacritty...)",
            "TerminalFont": "Fuente tipográfica usada en la terminal",
            "TerminalSize": "Dimensiones de la ventana (columnas x filas)",
            "TerminalTheme": "Colores del tema de la terminal",
            "Colors": "Muestra una paleta con los colores de la terminal",
            "Editor": "Editor de texto por defecto del sistema",
            "LocalIp": "Dirección IP en tu red local (IPv4/IPv6)",
            "PublicIp": "Dirección IP pública en Internet",
            "DNS": "Servidores DNS configurados en la red",
            "Wifi": "Información de la red Wi-Fi conectada",
            "NetIO": "Tráfico de red actual (subida y bajada)",
            "Bluetooth": "Dispositivos Bluetooth conectados",
            "BluetoothRadio": "Adaptadores Bluetooth de tu equipo",
            "Camera": "Cámaras conectadas o detectadas",
            "Gamepad": "Mandos de juego conectados",
            "Keyboard": "Teclados conectados",
            "Mouse": "Ratones conectados",
            "Sound": "Dispositivos de audio y nivel de volumen",
            "PowerAdapter": "Información del cargador (vataje)",
            "Battery": "Nivel, salud y estado de la batería",
            "Media": "Canción o vídeo que se está reproduciendo",
            "Player": "Reproductor multimedia activo actualmente",
            "Btrfs": "Información de volúmenes y particiones BTRFS",
            "Zpool": "Información de volúmenes de almacenamiento ZFS",
            "Break": "Inserta una línea en blanco para dar espacio",
            "Separator": "Dibuja una línea punteada separadora",
            "Custom": "Permite añadir texto puro o etiquetas personalizadas",
            "Command": "Ejecuta y muestra la salida de un script o comando bash",
            "Version": "Versión instalada de Fastfetch",
            "Weather": "Temperatura y clima local actual",
            "Pacman": "Script: pacman -Qqn | wc -l",
            "AUR": "Script: pacman -Qqm | wc -l",
            "Flatpak": "Script: flatpak list --app | wc -l",
            "Total_Pkgs": "Script: Suma total de todos los paquetes"
        }

        for cat, mods in categorias_modules.items():
            cat_item = QTreeWidgetItem([tr(cat)])
            for mod in mods:
                mod_item = QTreeWidgetItem([mod])

                # Le asignamos el tooltip. Lo envolvemos en tr() por si en el futuro
                # quieres traducir estas explicaciones al inglés en el diccionario superior.
                tooltip_texto = descripciones.get(mod, "Módulo de Fastfetch")
                mod_item.setToolTip(0, tr(tooltip_texto))

                cat_item.addChild(mod_item)
            self.tree_disp.addTopLevelItem(cat_item)

        self.tree_disp.itemDoubleClicked.connect(self.anadir_modulo)

        layout_botones = QVBoxLayout()
        self.btn_add = QPushButton(tr("Añadir ->"))
        self.btn_add.clicked.connect(self.anadir_modulo_btn)
        self.btn_rem = QPushButton(tr("<- Quitar"))
        self.btn_rem.clicked.connect(self.quitar_modulo_btn)
        layout_botones.addStretch()
        layout_botones.addWidget(self.btn_add)
        layout_botones.addWidget(self.btn_rem)
        layout_botones.addStretch()

        self.lista_sel = QListWidget()
        self.lista_sel.setDragDropMode(QAbstractItemView.DragDropMode.InternalMove)
        self.lista_sel.itemDoubleClicked.connect(self.editar_modulo_lista)

        layout_listas.addWidget(self.tree_disp)
        layout_listas.addLayout(layout_botones)
        layout_listas.addWidget(self.lista_sel)

        layout.addLayout(layout_listas)

        # Botones Aceptar / Cancelar
        botones = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        botones.accepted.connect(self.accept)
        # --- Lógica de Edición (Autorellenado) ---
        if datos_edicion:
            self.txt_nombre.setText(datos_edicion.get("nombre", ""))

            icono_guardado = datos_edicion.get("icono_titulo", "󰪥")
            # Buscamos si el icono guardado coincide con alguno de la lista desplegable
            indice_icono = -1
            for i in range(self.cmb_icono_titulo.count()):
                if self.cmb_icono_titulo.itemText(i).startswith(icono_guardado):
                    indice_icono = i
                    break

            if indice_icono >= 0:
                self.cmb_icono_titulo.setCurrentIndex(indice_icono)
            else:
                # Si es un icono custom que pegó a mano, lo forzamos en la caja
                self.cmb_icono_titulo.setCurrentText(icono_guardado)

            # Recuperar color del icono del titulo
            color_icono_str = datos_edicion.get("color_icono_titulo", "0")
            for i in range(self.cmb_color_icono_titulo.count()):
                if f"({color_icono_str})" in self.cmb_color_icono_titulo.itemText(i):
                    self.cmb_color_icono_titulo.setCurrentIndex(i)
                    break

            # Recuperar color principal
            color_str = datos_edicion.get("color", "32")
            for i in range(self.cmb_color.count()):
                if f"({color_str})" in self.cmb_color.itemText(i):
                    self.cmb_color.setCurrentIndex(i)
                    break

            # Recuperar color de valores
            color_val_str = datos_edicion.get("color_valores", "0")
            for i in range(self.cmb_color_valores.count()):
                if f"({color_val_str})" in self.cmb_color_valores.itemText(i):
                    self.cmb_color_valores.setCurrentIndex(i)
                    break

            # Recuperar checkboxes
            self.chk_arbol.setChecked(datos_edicion.get("arbol", True))
            self.chk_cuadrado.setChecked(datos_edicion.get("cuadrado", False))

            # Recuperar módulos a la lista derecha
            for mod_dict in datos_edicion.get("modulos", []):
                mod_type = mod_dict.get("type", "unknown")
                texto_mostrar = mod_type

                # Reconstruir el texto visual de los módulos configurados
                if mod_type == "custom" and "custom_text" in mod_dict:
                    texto_mostrar = f"custom [{mod_dict['custom_text']}]"
                elif mod_type == "command" and "text" in mod_dict:
                    texto_mostrar = f"command [{mod_dict['text']}]"
                elif mod_type == "weather" and "location" in mod_dict:
                    texto_mostrar = f"weather [{mod_dict['location']}]"
                elif mod_type == "disk" and "folders" in mod_dict:
                    texto_mostrar = f"disk [{mod_dict['folders']}]"

                nuevo_item = QListWidgetItem(texto_mostrar)
                nuevo_item.setData(Qt.ItemDataRole.UserRole, mod_dict)
                self.lista_sel.addItem(nuevo_item)
        botones.rejected.connect(self.reject)
        layout.addWidget(botones)

        self.setLayout(layout)

    def obtener_datos(self):
        color_ansi = self.cmb_color.currentText().split("(")[1].replace(")", "")
        color_val_ansi = self.cmb_color_valores.currentText().split("(")[1].replace(")", "")
        color_icono_ansi = self.cmb_color_icono_titulo.currentText().split("(")[1].replace(")", "")

        modulos_seleccionados = []
        for i in range(self.lista_sel.count()):
            item = self.lista_sel.item(i)
            # Extraemos los datos ocultos que guardamos al configurar
            datos_mod = item.data(Qt.ItemDataRole.UserRole)
            if datos_mod:
                modulos_seleccionados.append(datos_mod)
            else:
                # Fallback de seguridad por si algo falla
                modulos_seleccionados.append({"type": item.text().split(" ")[0].lower()})

        # Extraemos solo el primer carácter del combobox (el icono en sí)
        texto_icono_completo = self.cmb_icono_titulo.currentText()
        icono_limpio = texto_icono_completo.split(" ")[0] if " " in texto_icono_completo else texto_icono_completo

        return {
            "nombre": self.txt_nombre.text(),
            "icono_titulo": icono_limpio,
            "color_icono_titulo": color_icono_ansi,
            "color": color_ansi,
            "color_valores": color_val_ansi,
            "arbol": self.chk_arbol.isChecked(),
            "cuadrado": self.chk_cuadrado.isChecked(),
            "modulos": modulos_seleccionados
        }

    def procesar_adicion_modulo(self, mod_nombre):
        mod_nombre_limpio = mod_nombre.lower()
        texto_mostrar = mod_nombre_limpio
        param_dict = {"type": mod_nombre_limpio}

        # Interceptamos módulos especiales para pedir parámetros
        if mod_nombre_limpio == "pacman":
            param_dict = {"type": "command", "text": "pacman -Qqn | wc -l", "custom_text": "Pacman", "icon_custom": "󰮯"}
            texto_mostrar = "command [Pacman]"
        elif mod_nombre_limpio == "aur":
            param_dict = {"type": "command", "text": "pacman -Qqm | wc -l", "custom_text": "AUR", "icon_custom": "󰣇"}
            texto_mostrar = "command [AUR]"
        elif mod_nombre_limpio == "flatpak":
            param_dict = {"type": "command", "text": "flatpak list --app 2>/dev/null | wc -l", "custom_text": "Flatpak", "icon_custom": "󰏖"}
            texto_mostrar = "command [Flatpak]"
        elif mod_nombre_limpio == "total_pkgs":
            param_dict = {"type": "command", "text": "echo $(($(pacman -Qq | wc -l) + $(flatpak list --app 2>/dev/null | wc -l)))", "custom_text": "Total", "icon_custom": "󰏖"}
            texto_mostrar = "command [Total_Pkgs]"
        elif mod_nombre_limpio == "command":
            texto, ok = QInputDialog.getText(self, tr("Configurar Command"), tr("Comando a ejecutar (ej. pacman -Qq | wc -l):"))
            if ok and texto:
                param_dict["text"] = texto
                texto_mostrar = f"{mod_nombre_limpio} [{texto}]"
            else:
                return # Cancelado por el usuario
        elif mod_nombre_limpio == "weather":
            texto, ok = QInputDialog.getText(self, tr("Configurar Weather"), tr("Ciudad para el clima (ej. Madrid, London):"))
            if ok and texto:
                param_dict["location"] = texto
                texto_mostrar = f"{mod_nombre_limpio} [{texto}]"
            else:
                return
        elif mod_nombre_limpio == "disk":
            texto, ok = QInputDialog.getText(self, tr("Configurar Disk"), tr("Ruta del disco (ej. / o /home):"))
            if ok and texto:
                param_dict["folders"] = texto
                param_dict["custom_text"] = f"Disk {texto}"
                texto_mostrar = f"{mod_nombre_limpio} [{texto}]"
            else:
                return
        elif mod_nombre_limpio == "custom":
            texto, ok = QInputDialog.getText(self, tr("Configurar Custom"), tr("Texto personalizado a mostrar:"))
            if ok and texto:
                param_dict["custom_text"] = texto
                texto_mostrar = f"custom [{texto}]"
            else:
                return

        # Añadimos a la lista visualmente, y guardamos el diccionario por detrás
        nuevo_item = QListWidgetItem(texto_mostrar)
        nuevo_item.setData(Qt.ItemDataRole.UserRole, param_dict)
        self.lista_sel.addItem(nuevo_item)

    # Funciones para manejar módulos en la UI
    def anadir_modulo(self, item, column=0):
        if item.childCount() == 0:
            self.procesar_adicion_modulo(item.text(0))

    def editar_modulo_lista(self, item):
        mod_dict = item.data(Qt.ItemDataRole.UserRole)
        dialogo = DialogoEditarModulo(mod_dict, self)
        if dialogo.exec():
            nuevos_datos = dialogo.obtener_datos_modulo()
            mod_dict.update(nuevos_datos)
            item.setData(Qt.ItemDataRole.UserRole, mod_dict)

    def quitar_modulo(self, item):
        self.lista_sel.takeItem(self.lista_sel.row(item))

    def anadir_modulo_btn(self):
        item = self.tree_disp.currentItem()
        if item and item.childCount() == 0:
            self.procesar_adicion_modulo(item.text(0))

    def quitar_modulo_btn(self):
        fila = self.lista_sel.currentRow()
        if fila >= 0:
            self.lista_sel.takeItem(fila)

class FastfetchConfigurator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(tr("Configurador de Fastfetch"))
        self.resize(650, 450)
        self.current_file = None
        self.crear_menu()

        # Crear el contenedor de pestañas
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        # Crear las pestañas
        self.tab_install = QWidget()
        self.tab_config = QWidget()
        self.tab_preview = QWidget()

        self.tabs.addTab(self.tab_install, tr("1. Instalación"))
        self.tabs.addTab(self.tab_config, tr("2. Configuración"))
        self.tabs.addTab(self.tab_preview, tr("3. Vista Previa"))

        # Inicializar el contenido de cada pestaña
        self.init_install_tab()
        self.init_config_tab()
        self.init_preview_tab()

        # Conectar el cambio de pestaña para actualizar la vista previa automáticamente
        self.tabs.currentChanged.connect(self.on_tab_changed)

    def crear_menu(self):
        # Crea la barra de menú principal
        menu_bar = self.menuBar()

        # Añade la pestaña "Archivo"
        menu_archivo = menu_bar.addMenu(tr("Archivo"))

        # Crea las acciones y las añade al menú
        accion_nuevo = QAction(tr("Nuevo"), self)
        accion_nuevo.triggered.connect(self.archivo_nuevo)
        menu_archivo.addAction(accion_nuevo)

        accion_cargar = QAction(tr("Cargar"), self)
        accion_cargar.triggered.connect(self.archivo_cargar)
        menu_archivo.addAction(accion_cargar)

        accion_cargar_instalada = QAction(tr("Cargar conf. instalada"), self)
        accion_cargar_instalada.triggered.connect(self.archivo_cargar_instalada)
        menu_archivo.addAction(accion_cargar_instalada)

        accion_guardar = QAction(tr("Guardar"), self)
        accion_guardar.triggered.connect(self.archivo_guardar)
        menu_archivo.addAction(accion_guardar)

        accion_guardar_como = QAction(tr("Guardar como..."), self)
        accion_guardar_como.triggered.connect(self.archivo_guardar_como)
        menu_archivo.addAction(accion_guardar_como)

    def archivo_nuevo(self):
        self.current_file = None
        # Desmarca todas las casillas
        for cb in self.checkboxes.values():
            cb.setChecked(False)

    def archivo_cargar_instalada(self):
        ruta_archivo = os.path.expanduser("~/.config/fastfetch/config.jsonc")
        if os.path.exists(ruta_archivo):
            self.cargar_desde_archivo(ruta_archivo)
        else:
            QMessageBox.warning(self, "Aviso", f"No se ha encontrado ninguna configuración instalada en:\n{ruta_archivo}")

    def archivo_cargar(self):
        archivo, _ = QFileDialog.getOpenFileName(self, tr("Cargar configuración"), "", "JSON Files (*.json *.jsonc);;All Files (*)")
        if archivo:
            self.cargar_desde_archivo(archivo)

    def cargar_desde_archivo(self, ruta):
        try:
            with open(ruta, 'r', encoding='utf-8') as f:
                contenido = f.read()
                lineas = [linea for linea in contenido.split('\n') if not linea.strip().startswith('//')]
                datos = json.loads('\n'.join(lineas))

            self.secciones_datos.clear()

            if "$gui_config" in datos:
                gui = datos["$gui_config"]

                self.secciones_datos = gui.get("secciones_datos", [])

                if hasattr(self, 'spin_ancho'):
                    self.spin_ancho.blockSignals(True)
                    self.spin_ancho.setValue(gui.get("ancho_int", 40))
                    self.spin_ancho.blockSignals(False)

                if hasattr(self, 'cmb_logo'):
                    self.cmb_logo.blockSignals(True)
                    self.cmb_logo.setCurrentIndex(gui.get("logo_index", 0))
                    self.cmb_logo.blockSignals(False)

                if hasattr(self, 'spin_pad_top'): self.spin_pad_top.setValue(gui.get("pad_top", 1))
                if hasattr(self, 'spin_pad_left'): self.spin_pad_left.setValue(gui.get("pad_left", 2))
                if hasattr(self, 'spin_pad_right'): self.spin_pad_right.setValue(gui.get("pad_right", 3))

                if hasattr(self, 'chk_caja_global'): self.chk_caja_global.setChecked(gui.get("caja_global", False))
                if hasattr(self, 'cmb_color_global'): self.cmb_color_global.setCurrentIndex(gui.get("color_global", 0))
                if hasattr(self, 'txt_titulo_global'): self.txt_titulo_global.setText(gui.get("titulo_global", ""))
                if hasattr(self, 'cmb_alineacion_global'): self.cmb_alineacion_global.setCurrentIndex(gui.get("alineacion_global", 0))
                if hasattr(self, 'chk_iconos'): self.chk_iconos.setChecked(gui.get("usar_iconos", True))
                if hasattr(self, 'cmb_barra_lleno'): self.cmb_barra_lleno.setCurrentIndex(gui.get("barra_lleno", 0))
                if hasattr(self, 'cmb_barra_vacio'): self.cmb_barra_vacio.setCurrentIndex(gui.get("barra_vacio", 0))
                if hasattr(self, 'cmb_barra_chars'): self.cmb_barra_chars.setCurrentIndex(gui.get("barra_chars", 0))
                if hasattr(self, 'cmb_color_iconos'): self.cmb_color_iconos.setCurrentIndex(gui.get("color_iconos", 0))
                if hasattr(self, 'spin_padding_top_secciones'): self.spin_padding_top_secciones.setValue(gui.get("padding_top_secciones", 0))
                if hasattr(self, 'spin_padding_secciones'): self.spin_padding_secciones.setValue(gui.get("padding_secciones", 1))

                self.ruta_imagen_custom = gui.get("ruta_imagen", "")
                if self.ruta_imagen_custom and hasattr(self, 'btn_buscar_img'):
                    self.btn_buscar_img.setText(os.path.basename(self.ruta_imagen_custom))

                self.on_logo_changed(gui.get("logo_index", 0))

            else:
                modulos_importados = []
                if "modules" in datos:
                    for mod in datos["modules"]:
                        if isinstance(mod, str) and mod != "break":
                            modulos_importados.append({"type": mod})
                        elif isinstance(mod, dict) and "type" in mod and mod["type"] != "custom":
                            modulos_importados.append(mod)

                if modulos_importados:
                    seccion_importada = {
                        "nombre": "IMPORTADA",
                        "color": "37",
                        "color_valores": "0",
                        "arbol": True,
                        "cuadrado": True,
                        "modulos": modulos_importados
                    }
                    self.secciones_datos.append(seccion_importada)

            # Volcamos todo al árbol visual
            self.popular_arbol_secciones()
            self.current_file = ruta
            self.update_preview()
            QMessageBox.information(self, tr("Éxito"), tr("Configuración cargada correctamente."))

        except Exception as e:
            QMessageBox.warning(self, tr("Error"), f"{tr('No se pudo cargar el archivo:')}\n{e}")

    def archivo_guardar(self):
        if self.current_file:
            self.guardar_en_archivo(self.current_file)
        else:
            self.archivo_guardar_como()

    def archivo_guardar_como(self):
        archivo, _ = QFileDialog.getSaveFileName(self, tr("Guardar configuración"), "", "JSONC Files (*.jsonc)")
        if archivo:
            # Forzar extensión .jsonc
            if not archivo.endswith('.jsonc'):
                archivo += '.jsonc'
            self.guardar_en_archivo(archivo)

    def guardar_en_archivo(self, ruta):
        datos = self.generar_json_completo(es_vista_previa=False)
        try:
            with open(ruta, 'w', encoding='utf-8') as f:
                json.dump(datos, f, indent=4)
            self.current_file = ruta
            QMessageBox.information(self, tr("Éxito"), tr("Configuración guardada correctamente."))
        except Exception as e:
            QMessageBox.warning(self, tr("Error"), f"{tr('No se pudo guardar el archivo:')} {e}")

    def init_install_tab(self):
        layout = QVBoxLayout()
        self.lbl_status = QLabel(tr("Comprobando estado de fastfetch..."))

        self.btn_install = QPushButton(tr("Instalar fastfetch"))
        self.btn_install.clicked.connect(self.install_fastfetch)

        layout.addWidget(self.lbl_status)
        layout.addWidget(self.btn_install)

        # --- Integración con la Shell ---
        layout.addSpacing(30)
        layout.addWidget(QLabel(tr("Integración con la Terminal:")))

        self.btn_shell = QPushButton(tr("Arrancar fastfetch al abrir la terminal (.bashrc / .zshrc)"))
        self.btn_shell.clicked.connect(self.integrar_en_shell)
        layout.addWidget(self.btn_shell)

        layout.addStretch()
        self.tab_install.setLayout(layout)

        self.check_installation()

    def check_installation(self):
        if shutil.which("fastfetch"):
            self.lbl_status.setText(tr("✅ ¡Fastfetch ya está instalado en el sistema!"))
            self.btn_install.setEnabled(False)
        else:
            self.lbl_status.setText(tr("❌ Fastfetch NO está instalado."))
            self.btn_install.setEnabled(True)

    def install_fastfetch(self):
        sistema = platform.system()

        try:
            if sistema == "Windows":
                # En Windows 10/11 lo más estándar ahora es winget
                subprocess.run(["winget", "install", "fastfetch"], check=True)
            elif sistema == "Darwin":
                # En macOS el estándar de facto es Homebrew
                subprocess.run(["brew", "install", "fastfetch"], check=True)
            elif sistema == "Linux":
                # En Linux buscamos el gestor de paquetes disponible
                if shutil.which("pacman"):
                    subprocess.run(["pkexec", "pacman", "-S", "--noconfirm", "fastfetch"], check=True)
                elif shutil.which("apt"):
                    subprocess.run(["pkexec", "apt", "install", "-y", "fastfetch"], check=True)
                elif shutil.which("dnf"):
                    subprocess.run(["pkexec", "dnf", "install", "-y", "fastfetch"], check=True)
                elif shutil.which("zypper"):
                    subprocess.run(["pkexec", "zypper", "in", "-y", "fastfetch"], check=True)
                else:
                    QMessageBox.warning(self, "Error", "No se ha detectado un gestor de paquetes compatible (pacman, apt, dnf, zypper).")
                    return
            else:
                QMessageBox.warning(self, "Error", f"Sistema operativo '{sistema}' no soportado automáticamente.")
                return

            self.check_installation()

        except subprocess.CalledProcessError:
            QMessageBox.warning(self, "Error", "No se pudo instalar fastfetch. Operación cancelada o fallida.")
        except FileNotFoundError:
            QMessageBox.warning(self, "Error", "Falta una herramienta necesaria para instalar (ej. winget, brew o pkexec en Linux).")

    def integrar_en_shell(self):
        # Buscamos los archivos de shell más comunes en el home del usuario
        archivos_shell = [os.path.expanduser("~/.bashrc"), os.path.expanduser("~/.zshrc")]
        archivos_modificados = []
        ya_configurados = []

        for ruta in archivos_shell:
            if os.path.exists(ruta):
                with open(ruta, 'r', encoding='utf-8') as f:
                    contenido = f.read()

                # Comprobamos si la palabra fastfetch ya está en el archivo
                # (ignoramos si está comentada con #)
                lineas_limpias = [l.strip() for l in contenido.split('\n') if l.strip() and not l.strip().startswith('#')]

                # Si algún comando activo es fastfetch, asumimos que ya lo tiene
                if any("fastfetch" in linea for linea in lineas_limpias):
                    ya_configurados.append(os.path.basename(ruta))
                else:
                    # Si no está, lo inyectamos al final del archivo
                    with open(ruta, 'a', encoding='utf-8') as f:
                        f.write("\n# Lanzar Fastfetch automáticamente al abrir la terminal\nfastfetch\n")
                    archivos_modificados.append(os.path.basename(ruta))

        # Informamos al usuario del resultado
        if archivos_modificados:
            archivos_str = " y ".join(archivos_modificados)
            QMessageBox.information(self, "Éxito", f"{tr('Se ha añadido fastfetch al final de tu')} {archivos_str}.")
        elif ya_configurados:
            archivos_str = " y ".join(ya_configurados)
            QMessageBox.information(self, "Información", f"{tr('Ya tienes fastfetch configurado en tu')} {archivos_str}.")
        else:
            QMessageBox.warning(self, "Aviso", "No se encontró ni .bashrc ni .zshrc en tu directorio personal.")

    def init_config_tab(self):
        layout = QVBoxLayout()

        # --- Plantillas Predefinidas ---
        layout_plantillas = QHBoxLayout()
        layout_plantillas.addWidget(QLabel(tr("Plantillas Predefinidas:")))

        self.cmb_plantillas = QComboBox()
        self.cmb_plantillas.addItems([
            tr("Cyberpunk (Neón y Cajas)"),
            tr("Minimalista (Sin bordes)"),
            tr("Mac-Style (Limpio)"),
            tr("Dracula (Neón Oscuro)"),
            tr("Terminal Retro (Hacker)"),
            tr("Catppuccin (Pastel y Bloques)")
        ])
        layout_plantillas.addWidget(self.cmb_plantillas)

        self.btn_cargar_plantilla = QPushButton(tr("Cargar Plantilla"))
        self.btn_cargar_plantilla.clicked.connect(self.cargar_plantilla)
        layout_plantillas.addWidget(self.btn_cargar_plantilla)

        layout_plantillas.addStretch()
        layout.addLayout(layout_plantillas)

        # Separador visual
        layout.addSpacing(10)

        # --- Opciones Globales ---
        layout_global = QHBoxLayout()
        layout_global.addWidget(QLabel(tr("Logo del sistema (Izquierda):")))
        self.cmb_logo = QComboBox()
        self.cmb_logo.addItems([tr("Auto (Grande)"), tr("Pequeño (Small)"), tr("Oculto (None)"), tr("Imagen Personalizada")])
        self.cmb_logo.currentIndexChanged.connect(self.on_logo_changed)
        layout_global.addWidget(self.cmb_logo)

        # Botón y opciones para la imagen personalizada
        self.btn_buscar_img = QPushButton(tr("Seleccionar Imagen"))
        self.btn_buscar_img.clicked.connect(self.buscar_imagen)
        self.btn_buscar_img.setEnabled(False)
        layout_global.addWidget(self.btn_buscar_img)

        self.lbl_img_width = QLabel(tr("Ancho (col):"))
        self.lbl_img_width.setEnabled(False)
        layout_global.addWidget(self.lbl_img_width)

        self.spin_img_width = QSpinBox()
        self.spin_img_width.setRange(10, 150)
        self.spin_img_width.setValue(30)
        self.spin_img_width.valueChanged.connect(self.update_preview)
        self.spin_img_width.setEnabled(False)
        layout_global.addWidget(self.spin_img_width)

        self.ruta_imagen_custom = ""

        # Selector de ancho del recuadro
        layout_global.addSpacing(20)
        layout_global.addWidget(QLabel(tr("Ancho del cuadrado (columnas):")))
        self.spin_ancho = QSpinBox()
        self.spin_ancho.setRange(20, 150)
        self.spin_ancho.setValue(40)
        self.spin_ancho.valueChanged.connect(self.update_preview)
        layout_global.addWidget(self.spin_ancho)

        # Casilla para los Iconos Nerd Font
        layout_global.addSpacing(20)
        self.chk_iconos = QCheckBox(tr("Usar iconos (Nerd Fonts)"))
        self.chk_iconos.setChecked(True)
        self.chk_iconos.stateChanged.connect(self.update_preview)
        layout_global.addWidget(self.chk_iconos)

        layout_global.addSpacing(10)
        layout_global.addWidget(QLabel(tr("Color de iconos:")))
        self.cmb_color_iconos = QComboBox()
        self.cmb_color_iconos.addItems([tr(c) for c in [
            "Por defecto (0)", "Gris (90)", "Rojo (31)", "Verde (32)",
            "Amarillo (33)", "Azul (34)", "Magenta (35)", "Cian (36)", "Blanco (37)"
        ]])
        self.cmb_color_iconos.currentIndexChanged.connect(self.update_preview)
        layout_global.addWidget(self.cmb_color_iconos)

        layout_global.addStretch()
        layout.addLayout(layout_global)

        # --- Segunda fila de Opciones Globales (Padding del Logo) ---
        layout_global_2 = QHBoxLayout()
        layout_global_2.addWidget(QLabel(tr("Márgenes del Logo (Arriba / Izq / Der):")))

        self.spin_pad_top = QSpinBox()
        self.spin_pad_top.setRange(0, 20)
        self.spin_pad_top.setValue(1) # Por defecto en tu config
        self.spin_pad_top.valueChanged.connect(self.update_preview)

        self.spin_pad_left = QSpinBox()
        self.spin_pad_left.setRange(0, 20)
        self.spin_pad_left.setValue(2) # Por defecto en tu config
        self.spin_pad_left.valueChanged.connect(self.update_preview)

        self.spin_pad_right = QSpinBox()
        self.spin_pad_right.setRange(0, 30)
        self.spin_pad_right.setValue(3) # Por defecto en tu config
        self.spin_pad_right.valueChanged.connect(self.update_preview)

        layout_global_2.addWidget(self.spin_pad_top)
        layout_global_2.addWidget(self.spin_pad_left)
        layout_global_2.addWidget(self.spin_pad_right)
        layout_global_2.addStretch()

        layout.addLayout(layout_global_2)

        # --- Tercera fila de Opciones Globales (Caja Global) ---
        layout_global_3 = QHBoxLayout()
        self.chk_caja_global = QCheckBox(tr("Recuadro Global alrededor de todo"))
        self.chk_caja_global.stateChanged.connect(self.update_preview)
        layout_global_3.addWidget(self.chk_caja_global)

        self.cmb_color_global = QComboBox()
        self.cmb_color_global.addItems([tr(c) for c in [
            "Azul (34)", "Verde (32)", "Amarillo (33)",
            "Magenta (35)", "Cian (36)", "Rojo (31)", "Blanco (37)"
        ]])
        self.cmb_color_global.currentIndexChanged.connect(self.update_preview)
        layout_global_3.addWidget(self.cmb_color_global)

        self.txt_titulo_global = QLineEdit()
        self.txt_titulo_global.setPlaceholderText(tr("Título del recuadro (opcional):"))
        self.txt_titulo_global.textChanged.connect(self.update_preview)
        layout_global_3.addWidget(self.txt_titulo_global)
        self.cmb_alineacion_global = QComboBox()
        self.cmb_alineacion_global.addItems([tr("Izquierda"), tr("Centro"), tr("Derecha")])
        self.cmb_alineacion_global.currentIndexChanged.connect(self.update_preview)
        layout_global_3.addWidget(self.cmb_alineacion_global)

        layout_global_3.addStretch()
        layout.addLayout(layout_global_3)

        # --- Cuarta fila de Opciones Globales (Barra de progreso) ---
        layout_global_4 = QHBoxLayout()
        layout_global_4.addWidget(QLabel(tr("Color Barra (Lleno / Vacío):")))

        self.cmb_barra_lleno = QComboBox()
        self.opciones_barra = [
            "Automático (Dinámico)", "Gris (90)", "Rojo (31)", "Verde (32)",
            "Amarillo (33)", "Azul (34)", "Magenta (35)", "Cian (36)", "Blanco (37)"
        ]
        self.cmb_barra_lleno.addItems([tr(c) for c in self.opciones_barra])
        self.cmb_barra_lleno.setCurrentIndex(0) # Automático por defecto
        self.cmb_barra_lleno.currentIndexChanged.connect(self.update_preview)
        layout_global_4.addWidget(self.cmb_barra_lleno)

        self.cmb_barra_vacio = QComboBox()
        self.cmb_barra_vacio.addItems([tr(c) for c in self.opciones_barra])
        self.cmb_barra_vacio.setCurrentIndex(0) # Automático por defecto
        self.cmb_barra_vacio.currentIndexChanged.connect(self.update_preview)
        layout_global_4.addWidget(self.cmb_barra_vacio)

        # --- NUEVO SELECTOR DE ESTILO DE CARACTERES ---
        layout_global_4.addSpacing(15)
        layout_global_4.addWidget(QLabel(tr("Caracteres Barra (Lleno / Vacío):")))
        self.cmb_barra_chars = QComboBox()
        self.cmb_barra_chars.addItems(["█ / ▒", "█ / █", "■ / □", "● / ○", "# / -"])
        self.cmb_barra_chars.currentIndexChanged.connect(self.update_preview)
        layout_global_4.addWidget(self.cmb_barra_chars)

        layout_global_4.addStretch()
        layout.addLayout(layout_global_4)

        # --- Quinta fila de Opciones Globales (Espaciado) ---
        layout_global_5 = QHBoxLayout()

        layout_global_5.addWidget(QLabel(tr("Espaciado superior inicial (líneas):")))
        self.spin_padding_top_secciones = QSpinBox()
        self.spin_padding_top_secciones.setRange(0, 5)
        self.spin_padding_top_secciones.setValue(0) # 0 por defecto
        self.spin_padding_top_secciones.valueChanged.connect(self.update_preview)
        layout_global_5.addWidget(self.spin_padding_top_secciones)

        layout_global_5.addSpacing(15)

        layout_global_5.addWidget(QLabel(tr("Espaciado entre secciones (líneas):")))
        self.spin_padding_secciones = QSpinBox()
        self.spin_padding_secciones.setRange(0, 5)
        self.spin_padding_secciones.setValue(1) # 1 línea por defecto
        self.spin_padding_secciones.valueChanged.connect(self.update_preview)
        layout_global_5.addWidget(self.spin_padding_secciones)

        layout_global_5.addStretch()
        layout.addLayout(layout_global_5)

        # Espaciador visual antes de las secciones
        layout.addSpacing(10)
        layout.addWidget(QLabel(tr("Secciones personalizadas:")))

        # Vista en árbol donde veremos las secciones y sus módulos
        self.tree_secciones_ui = QTreeWidget()
        self.tree_secciones_ui.setHeaderHidden(True)
        self.tree_secciones_ui.setDragDropMode(QAbstractItemView.DragDropMode.InternalMove)
        self.tree_secciones_ui.itemDoubleClicked.connect(self.editar_seccion)

        # Sincronización en tiempo real al soltar un módulo arrastrado
        self.tree_secciones_ui.model().rowsInserted.connect(lambda *args: self.update_preview())
        self.tree_secciones_ui.model().rowsMoved.connect(lambda *args: self.update_preview())

        layout.addWidget(self.tree_secciones_ui)

        # Botones para gestionar secciones
        btn_layout = QHBoxLayout()
        self.btn_add_sec = QPushButton(tr("Añadir Sección"))
        self.btn_add_sec.clicked.connect(self.abrir_dialogo_seccion)
        btn_layout.addWidget(self.btn_add_sec)

        self.btn_del_sec = QPushButton(tr("Borrar Seleccionada"))
        self.btn_del_sec.clicked.connect(self.borrar_seccion)
        btn_layout.addWidget(self.btn_del_sec)

        layout.addLayout(btn_layout)

        self.btn_save = QPushButton(tr("Generar y Guardar config.jsonc"))
        self.btn_save.clicked.connect(self.guardar_por_defecto)
        layout.addWidget(self.btn_save)

        self.tab_config.setLayout(layout)

        # Almacén de datos lógicos para el JSON
        self.secciones_datos = []

    def popular_arbol_secciones(self):
        self.tree_secciones_ui.clear()
        for sec in self.secciones_datos:
            sec_item = QTreeWidgetItem([f"{sec['nombre']} ({len(sec['modulos'])} modulos)"])
            # Guardamos la config de la sección vaciando la lista de módulos
            sec_data = sec.copy()
            sec_data['modulos'] = []
            sec_item.setData(0, Qt.ItemDataRole.UserRole, sec_data)
            # Activamos que la sección sea un contenedor donde soltar cosas
            sec_item.setFlags(sec_item.flags() | Qt.ItemFlag.ItemIsDropEnabled | Qt.ItemFlag.ItemIsDragEnabled)

            for mod_dict in sec['modulos']:
                if isinstance(mod_dict, str): mod_dict = {"type": mod_dict}
                mod_type = mod_dict.get("type", "unknown")
                texto_mostrar = mod_type

                if mod_type == "custom" and "custom_text" in mod_dict:
                    texto_mostrar = f"custom [{mod_dict['custom_text']}]"
                elif mod_type == "command" and "text" in mod_dict:
                    texto_mostrar = f"command [{mod_dict['text']}]"
                elif mod_type == "weather" and "location" in mod_dict:
                    texto_mostrar = f"weather [{mod_dict['location']}]"
                elif mod_type == "disk" and "folders" in mod_dict:
                    texto_mostrar = f"disk [{mod_dict['folders']}]"

                mod_item = QTreeWidgetItem([texto_mostrar])
                mod_item.setData(0, Qt.ItemDataRole.UserRole, mod_dict)
                # Un módulo se puede arrastrar, pero NO se le pueden meter cosas dentro
                mod_item.setFlags((mod_item.flags() | Qt.ItemFlag.ItemIsDragEnabled) & ~Qt.ItemFlag.ItemIsDropEnabled)
                sec_item.addChild(mod_item)

            self.tree_secciones_ui.addTopLevelItem(sec_item)
            sec_item.setExpanded(True)

    def sincronizar_datos_arbol(self):
        if not hasattr(self, 'tree_secciones_ui'): return
        self.secciones_datos = []
        for i in range(self.tree_secciones_ui.topLevelItemCount()):
            sec_item = self.tree_secciones_ui.topLevelItem(i)
            sec_data = sec_item.data(0, Qt.ItemDataRole.UserRole)
            if not sec_data: continue

            modulos = []
            for j in range(sec_item.childCount()):
                mod_item = sec_item.child(j)
                mod_data = mod_item.data(0, Qt.ItemDataRole.UserRole)
                if mod_data:
                    modulos.append(mod_data)

            # Reconstruimos la sección con el nuevo orden de sus módulos
            sec_data_completo = sec_data.copy()
            sec_data_completo['modulos'] = modulos
            self.secciones_datos.append(sec_data_completo)

            # Refrescamos el contador visual del título
            sec_item.setText(0, f"{sec_data_completo['nombre']} ({len(modulos)} modulos)")

    def on_logo_changed(self, index):
        es_custom = (index == 3)
        self.btn_buscar_img.setEnabled(es_custom)
        self.lbl_img_width.setEnabled(es_custom)
        self.spin_img_width.setEnabled(es_custom)
        self.update_preview()

    def buscar_imagen(self):
        archivo, _ = QFileDialog.getOpenFileName(self, tr("Seleccionar Imagen"), "", "Images (*.png *.jpg *.jpeg *.bmp)")
        if archivo:
            self.ruta_imagen_custom = archivo
            # Mostramos el nombre del archivo en el botón para confirmar
            self.btn_buscar_img.setText(os.path.basename(archivo))
            self.update_preview()

    def abrir_dialogo_seccion(self):
        self.sincronizar_datos_arbol()
        dialogo = DialogoNuevaSeccion(self)
        if dialogo.exec():
            datos = dialogo.obtener_datos()
            if not datos["nombre"]: datos["nombre"] = "SECCIÓN"
            self.secciones_datos.append(datos)
            self.popular_arbol_secciones()
            self.update_preview()

    def editar_seccion(self, item, column=0):
        # Si el usuario hace doble clic en un módulo (hijo), abrimos el editor independiente del módulo
        if item.parent() is not None:
            self.sincronizar_datos_arbol()
            sec_item = item.parent()
            fila_sec = self.tree_secciones_ui.indexOfTopLevelItem(sec_item)
            fila_mod = sec_item.indexOfChild(item)
            mod_dict = self.secciones_datos[fila_sec]['modulos'][fila_mod]

            dialogo = DialogoEditarModulo(mod_dict, self)
            if dialogo.exec():
                nuevos_datos = dialogo.obtener_datos_modulo()
                mod_dict.update(nuevos_datos)
                item.setData(0, Qt.ItemDataRole.UserRole, mod_dict)
                self.sincronizar_datos_arbol()
                self.update_preview()
            return

        self.sincronizar_datos_arbol()
        fila = self.tree_secciones_ui.indexOfTopLevelItem(item)
        if fila < 0: return

        datos_actuales = self.secciones_datos[fila]
        dialogo = DialogoNuevaSeccion(self, datos_edicion=datos_actuales)
        if dialogo.exec():
            nuevos_datos = dialogo.obtener_datos()
            self.secciones_datos[fila] = nuevos_datos
            self.popular_arbol_secciones()
            self.update_preview()

    def borrar_seccion(self):
        item = self.tree_secciones_ui.currentItem()
        if item:
            # Si es un módulo (tiene padre), lo borramos de esa sección
            if item.parent():
                item.parent().removeChild(item)
            # Si es una sección entera (raíz), nos la cargamos por completo
            else:
                index = self.tree_secciones_ui.indexOfTopLevelItem(item)
                self.tree_secciones_ui.takeTopLevelItem(index)
            self.update_preview()

    def cargar_plantilla(self):
        # Aviso de seguridad
        respuesta = QMessageBox.question(self, tr("¿Cargar plantilla?"),
                                         tr("Esto borrará tu configuración actual. ¿Deseas continuar?"),
                                         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        if respuesta == QMessageBox.StandardButton.No:
            return

        indice = self.cmb_plantillas.currentIndex()
        self.secciones_datos.clear()

        # Silenciamos las señales para que la vista previa no parpadee mil veces
        if hasattr(self, 'spin_ancho'): self.spin_ancho.blockSignals(True)
        if hasattr(self, 'chk_caja_global'): self.chk_caja_global.blockSignals(True)
        if hasattr(self, 'cmb_color_global'): self.cmb_color_global.blockSignals(True)
        if hasattr(self, 'chk_iconos'): self.chk_iconos.blockSignals(True)
        if hasattr(self, 'cmb_color_iconos'): self.cmb_color_iconos.blockSignals(True)
        if hasattr(self, 'spin_padding_top_secciones'): self.spin_padding_top_secciones.blockSignals(True)
        if hasattr(self, 'spin_padding_secciones'): self.spin_padding_secciones.blockSignals(True)

        if indice == 0:  # Cyberpunk
            # Forzamos opciones globales
            if hasattr(self, 'chk_caja_global'): self.chk_caja_global.setChecked(True)
            if hasattr(self, 'cmb_color_global'): self.cmb_color_global.setCurrentIndex(4) # Cian
            if hasattr(self, 'chk_iconos'): self.chk_iconos.setChecked(True)
            if hasattr(self, 'cmb_color_iconos'): self.cmb_color_iconos.setCurrentIndex(6) # Magenta
            if hasattr(self, 'spin_ancho'): self.spin_ancho.setValue(45)
            if hasattr(self, 'cmb_barra_lleno'): self.cmb_barra_lleno.setCurrentIndex(6) # Cian
            if hasattr(self, 'cmb_barra_vacio'): self.cmb_barra_vacio.setCurrentIndex(0) # Gris

            self.secciones_datos = [
                {
                    "nombre": "SISTEMA", "color": "35", "color_valores": "36",
                    "arbol": True, "cuadrado": True, "icono_titulo": "󰣇", "color_icono_titulo": "36",
                    "modulos": [
                        {"type": "os", "icon_color": "36"},
                        {"type": "kernel", "icon_color": "36"},
                        {"type": "uptime", "icon_color": "36"},
                        {"type": "pacman", "icon_custom": "󰮯", "icon_color": "36", "type_real": "command", "text": "pacman -Qqn | wc -l", "custom_text": "Pacman"}
                    ]
                },
                {
                    "nombre": "HARDWARE", "color": "36", "color_valores": "35",
                    "arbol": True, "cuadrado": True, "icono_titulo": "", "color_icono_titulo": "35",
                    "modulos": [
                        {"type": "cpu", "icon_color": "35"},
                        {"type": "gpu", "icon_color": "35"},
                        {"type": "memory", "icon_color": "35", "usar_barra": True},
                        {"type": "disk", "folders": "/", "custom_text": "Disk /", "icon_color": "35", "usar_barra": True}
                    ]
                }
            ]

        elif indice == 1:  # Minimalista
            if hasattr(self, 'chk_caja_global'): self.chk_caja_global.setChecked(False)
            if hasattr(self, 'chk_iconos'): self.chk_iconos.setChecked(True)
            if hasattr(self, 'cmb_color_iconos'): self.cmb_color_iconos.setCurrentIndex(8) # Blanco
            if hasattr(self, 'spin_ancho'): self.spin_ancho.setValue(40)

            self.secciones_datos = [
                {
                    "nombre": "INFO", "color": "37", "color_valores": "90",
                    "arbol": False, "cuadrado": False, "icono_titulo": "󰪥", "color_icono_titulo": "37",
                    "modulos": [
                        {"type": "os"},
                        {"type": "kernel"},
                        {"type": "uptime"},
                        {"type": "shell"},
                        {"type": "memory", "format": "{1} / {2}"}
                    ]
                }
            ]

        elif indice == 2:  # Mac-Style
            if hasattr(self, 'chk_caja_global'): self.chk_caja_global.setChecked(False)
            if hasattr(self, 'chk_iconos'): self.chk_iconos.setChecked(True)
            if hasattr(self, 'cmb_color_iconos'): self.cmb_color_iconos.setCurrentIndex(0) # Default
            if hasattr(self, 'spin_ancho'): self.spin_ancho.setValue(45)

            self.secciones_datos = [
                {
                    "nombre": "Mac OS", "color": "37", "color_valores": "0",
                    "arbol": True, "cuadrado": False, "icono_titulo": "", "color_icono_titulo": "37",
                    "modulos": [
                        {"type": "os", "icon_custom": ""},
                        {"type": "host"},
                        {"type": "uptime"},
                        {"type": "packages"},
                        {"type": "memory"},
                        {"type": "battery"}
                    ]
                }
            ]

        elif indice == 3:  # Dracula (Neón Oscuro)
            if hasattr(self, 'chk_caja_global'): self.chk_caja_global.setChecked(False)
            if hasattr(self, 'chk_iconos'): self.chk_iconos.setChecked(True)
            if hasattr(self, 'cmb_color_iconos'): self.cmb_color_iconos.setCurrentIndex(6) # Magenta
            if hasattr(self, 'spin_ancho'): self.spin_ancho.setValue(45)
            if hasattr(self, 'cmb_barra_lleno'): self.cmb_barra_lleno.setCurrentIndex(7) # Cian
            if hasattr(self, 'cmb_barra_vacio'): self.cmb_barra_vacio.setCurrentIndex(1) # Gris

            self.secciones_datos = [
                {
                    "nombre": "VAMPIRE", "color": "35", "color_valores": "36",
                    "arbol": True, "cuadrado": False, "icono_titulo": "󰎆", "color_icono_titulo": "35",
                    "modulos": [
                        {"type": "os", "icon_color": "35"},
                        {"type": "kernel", "icon_color": "35"},
                        {"type": "packages", "icon_color": "35"},
                        {"type": "shell", "icon_color": "35"},
                        {"type": "terminal", "icon_color": "35"},
                        {"type": "memory", "usar_barra": True, "icon_color": "35"},
                        {"type": "uptime", "icon_color": "35"}
                    ]
                }
            ]

        elif indice == 4:  # Terminal Retro (Hacker)
            if hasattr(self, 'chk_caja_global'): self.chk_caja_global.setChecked(True)
            if hasattr(self, 'cmb_color_global'): self.cmb_color_global.setCurrentIndex(1) # Verde
            if hasattr(self, 'txt_titulo_global'): self.txt_titulo_global.setText("MAINFRAME TERMINAL")
            if hasattr(self, 'cmb_alineacion_global'): self.cmb_alineacion_global.setCurrentIndex(1) # Centro
            if hasattr(self, 'chk_iconos'): self.chk_iconos.setChecked(False) # ¡Sin iconos!
            if hasattr(self, 'spin_ancho'): self.spin_ancho.setValue(50)
            if hasattr(self, 'cmb_barra_lleno'): self.cmb_barra_lleno.setCurrentIndex(3) # Verde
            if hasattr(self, 'cmb_barra_vacio'): self.cmb_barra_vacio.setCurrentIndex(1) # Gris
            if hasattr(self, 'cmb_barra_chars'): self.cmb_barra_chars.setCurrentIndex(1) # █ / █

            self.secciones_datos = [
                {
                    "nombre": "SYSTEM", "color": "32", "color_valores": "32",
                    "arbol": False, "cuadrado": False, "icono_titulo": ">", "color_icono_titulo": "32",
                    "modulos": [
                        {"type": "os"},
                        {"type": "host"},
                        {"type": "kernel"},
                        {"type": "cpu"},
                        {"type": "memory", "usar_barra": True},
                        {"type": "disk", "folders": "/", "custom_text": "Disk /", "usar_barra": True},
                        {"type": "localip"}
                    ]
                }
            ]

        elif indice == 5:  # Catppuccin (Pastel y Bloques)
            if hasattr(self, 'chk_caja_global'): self.chk_caja_global.setChecked(False)
            if hasattr(self, 'chk_iconos'): self.chk_iconos.setChecked(True)
            if hasattr(self, 'cmb_color_iconos'): self.cmb_color_iconos.setCurrentIndex(5) # Azul
            if hasattr(self, 'spin_ancho'): self.spin_ancho.setValue(45)
            if hasattr(self, 'cmb_barra_lleno'): self.cmb_barra_lleno.setCurrentIndex(5) # Azul
            if hasattr(self, 'cmb_barra_vacio'): self.cmb_barra_vacio.setCurrentIndex(1) # Gris
            if hasattr(self, 'cmb_barra_chars'): self.cmb_barra_chars.setCurrentIndex(3) # ● / ○

            self.secciones_datos = [
                {
                    "nombre": "SOFTWARE", "color": "34", "color_valores": "37",
                    "arbol": False, "cuadrado": True, "icono_titulo": "󰾆", "color_icono_titulo": "34",
                    "modulos": [
                        {"type": "os", "icon_color": "34"},
                        {"type": "wm", "icon_color": "34"},
                        {"type": "theme", "icon_color": "34"},
                        {"type": "icons", "icon_color": "34"},
                        {"type": "terminal", "icon_color": "34"}
                    ]
                },
                {
                    "nombre": "HARDWARE", "color": "36", "color_valores": "37",
                    "arbol": False, "cuadrado": True, "icono_titulo": "", "color_icono_titulo": "36",
                    "modulos": [
                        {"type": "cpu", "icon_color": "36"},
                        {"type": "gpu", "icon_color": "36"},
                        {"type": "memory", "icon_color": "36", "usar_barra": True},
                        {"type": "battery", "icon_color": "36", "usar_barra": True}
                    ]
                }
            ]

        # Restauramos las señales
        if hasattr(self, 'spin_ancho'): self.spin_ancho.blockSignals(False)
        if hasattr(self, 'spin_padding_top_secciones'):
            self.spin_padding_top_secciones.setValue(0) # Restablecer a 0 por defecto al cargar plantilla
            self.spin_padding_top_secciones.blockSignals(False)
        if hasattr(self, 'spin_padding_secciones'):
            self.spin_padding_secciones.setValue(1) # Restablecer a 1 por defecto al cargar plantilla
            self.spin_padding_secciones.blockSignals(False)
        if hasattr(self, 'chk_caja_global'): self.chk_caja_global.blockSignals(False)
        if hasattr(self, 'cmb_color_global'): self.cmb_color_global.blockSignals(False)
        if hasattr(self, 'chk_iconos'): self.chk_iconos.blockSignals(False)
        if hasattr(self, 'cmb_color_iconos'): self.cmb_color_iconos.blockSignals(False)

        # Refrescamos la interfaz gráfica
        self.popular_arbol_secciones()
        self.update_preview()

    def guardar_por_defecto(self):
        # Ruta estándar de fastfetch en todos los SO (suele ser ~/.config/fastfetch/config.jsonc)
        ruta_directorio = os.path.expanduser("~/.config/fastfetch")
        ruta_archivo = os.path.join(ruta_directorio, "config.jsonc")

        # Crea el directorio si no existe para evitar errores
        os.makedirs(ruta_directorio, exist_ok=True)

        self.guardar_en_archivo(ruta_archivo)

    def init_preview_tab(self):
        layout = QVBoxLayout()

        self.txt_preview = QTextEdit()
        self.txt_preview.setReadOnly(True)

        # Usar fuente monoespaciada para que el arte ASCII y las columnas cuadren bien
        font = QFont("Monospace")
        font.setStyleHint(QFont.StyleHint.Monospace)
        self.txt_preview.setFont(font)

        # Botonera de la vista previa
        layout_botones_prev = QHBoxLayout()

        self.btn_refresh = QPushButton(tr("Actualizar Vista Previa"))
        self.btn_refresh.clicked.connect(self.update_preview)

        self.btn_terminal = QPushButton(tr("Ver en Terminal Real"))
        self.btn_terminal.clicked.connect(self.ver_en_terminal_real)

        layout_botones_prev.addWidget(self.btn_refresh)
        layout_botones_prev.addWidget(self.btn_terminal)

        layout.addLayout(layout_botones_prev)
        layout.addWidget(self.txt_preview)
        self.tab_preview.setLayout(layout)

    def generar_json_completo(self, es_vista_previa=False):
        modulos = []

    def generar_json_completo(self, es_vista_previa=False):
        self.sincronizar_datos_arbol()
        modulos = []

        # El ancho interior de la caja (leído desde la interfaz, por defecto 40)
        ancho_int = self.spin_ancho.value() if hasattr(self, 'spin_ancho') else 40

        # Matemáticas para cuadrar el borde derecho de las secciones en la terminal real
        mov_adelante = f"\u001b[{ancho_int + 2}C"
        mov_atras = f"\u001b[{ancho_int + 3}D"

        # Opciones de la Caja Global
        usar_caja_global = self.chk_caja_global.isChecked() if hasattr(self, 'chk_caja_global') else False
        if usar_caja_global:
            color_gl_num = self.cmb_color_global.currentText().split("(")[1].replace(")", "") if hasattr(self, 'cmb_color_global') else "34"
            c_gl = f"\u001b[0;{color_gl_num}m"
            titulo_global = self.txt_titulo_global.text() if hasattr(self, 'txt_titulo_global') else ""
            alineacion = self.cmb_alineacion_global.currentIndex() if hasattr(self, 'cmb_alineacion_global') else 0

            # Ancho total en guiones
            guiones_totales = ancho_int + 5

            if titulo_global:
                # Calculamos el espacio que sobra quitando el título y sus dos espacios laterales
                espacio_libre = guiones_totales - (len(titulo_global) + 2)
                if espacio_libre < 0: espacio_libre = 0

                if alineacion == 0: # Izquierda
                    guiones_izq = 2
                    guiones_der = max(0, espacio_libre - 2)
                elif alineacion == 1: # Centro
                    guiones_izq = espacio_libre // 2
                    guiones_der = espacio_libre - guiones_izq
                else: # Derecha
                    guiones_der = 2
                    guiones_izq = max(0, espacio_libre - 2)

                lin_sup = "─" * guiones_izq + f" {titulo_global} " + "─" * guiones_der
                # Aseguramos que si por caracteres extraños se pasa del ancho, se recorte
                lin_sup = lin_sup[:guiones_totales]
                modulos.append({"type": "custom", "format": f"{c_gl}┌{lin_sup}┐\u001b[0m"})
            else:
                modulos.append({"type": "custom", "format": f"{c_gl}┌{'─'*guiones_totales}┐\u001b[0m"})

            pared_izq_gl = f"{c_gl}│ \u001b[0m"

            # Matemáticas para la pared derecha global
            # El cursor estará en la columna 3 (después de '│ '). Saltamos ancho_int + 4 columnas para llegar al final exacto.
            mov_adel_gl = f"\u001b[{ancho_int + 4}C"
            mov_atras_gl = f"\u001b[{ancho_int + 5}D"
        else:
            pared_izq_gl = ""
            c_gl = ""
            mov_adel_gl = ""
            mov_atras_gl = ""
            guiones_totales = 0

        # Diccionario maestro y color de Iconos Nerd Font
        usar_iconos = self.chk_iconos.isChecked() if hasattr(self, 'chk_iconos') else True
        color_iconos_global = self.cmb_color_iconos.currentText().split("(")[1].replace(")", "") if hasattr(self, 'cmb_color_iconos') else "0"
        c_icono_global = f"\u001b[0;{color_iconos_global}m" if color_iconos_global != "0" else ""
        iconos = {
            "os": "󰣇", "host": "󰒋", "kernel": "󰌽", "initsystem": "󱄅", "uptime": "󰅐",
            "packages": "󰏖", "locale": "", "datetime": "󰃰", "users": "", "title": "",
            "board": "󱥎", "bios": "󰒡", "bootmgr": "󰒡", "chassis": "󰌢", "tpm": "󰒡",
            "cpu": "", "cpucache": "", "gpu": "󰢮", "physicaldisk": "󰋊", "physicalmemory": "󰍛",
            "cpuusage": "", "memory": "", "swap": "󰓡", "disk": "󰋊", "diskio": "󰋊",
            "loadavg": "󰊚", "processes": "󰒓", "display": "󰍹", "monitor": "󰍹", "brightness": "󰃠",
            "opencl": "󰢮", "opengl": "󰢮", "vulkan": "󰢮", "de": "󰧨", "wm": "",
            "wmtheme": "󰉼", "theme": "󰉼", "icons": "󰀻", "cursor": "󰆽", "font": "",
            "wallpaper": "󰸉", "lm": "󰧨", "shell": "", "terminal": "", "terminalfont": "",
            "terminalsize": "󰍹", "terminaltheme": "󰉼", "colors": "󰏘", "editor": "󰏫",
            "localip": "󰩟", "publicip": "󰩠", "dns": "󰩠", "wifi": "", "netio": "󰩠",
            "bluetooth": "", "bluetoothradio": "", "camera": "󰄀", "gamepad": "󰊗",
            "keyboard": "󰌌", "mouse": "󰍽", "sound": "󰕾", "poweradapter": "", "battery": "",
            "media": "󰝚", "player": "󰎆", "btrfs": "󰋊", "zpool": "󰋊", "command": "",
            "weather": "", "version": "󰏖", "custom": "󰏫"
        }

        # Espaciado superior inicial antes de que empiece la primera sección
        espacio_top = self.spin_padding_top_secciones.value() if hasattr(self, 'spin_padding_top_secciones') else 0
        for _ in range(espacio_top):
            if usar_caja_global:
                if es_vista_previa:
                    modulos.append({"type": "custom", "format": f"{c_gl}│{reset}"})
                else:
                    modulos.append({"type": "custom", "format": f"{pared_izq_gl}{c_gl}{mov_adel_gl}│{mov_atras_gl}{reset}"})
            else:
                modulos.append("break")

        total_secciones = len(self.secciones_datos)
        for idx_sec, sec in enumerate(self.secciones_datos):
            color = f"\u001b[0;{sec['color']}m"
            color_val_num = sec.get('color_valores', '0')
            color_val_ansi = f"\u001b[0;{color_val_num}m" if color_val_num != '0' else ""
            reset = "\u001b[0m"

            # Personalización del icono del título
            icono_tit = sec.get('icono_titulo', '󰪥')
            color_icono_tit_num = sec.get('color_icono_titulo', '0')
            c_icono_tit = f"\u001b[0;{color_icono_tit_num}m" if color_icono_tit_num != '0' else color

            if sec['cuadrado']:
                linea_sup = "─" * ancho_int
                format_sup = f"{pared_izq_gl}{color} ┌{linea_sup}┐{reset}"
                if usar_caja_global and not es_vista_previa:
                    format_sup = f"{pared_izq_gl}{c_gl}{mov_adel_gl}│{mov_atras_gl}{reset}{color} ┌{linea_sup}┐{reset}"
                modulos.append({"type": "custom", "format": format_sup})

                if es_vista_previa:
                    formato_titulo = f"{pared_izq_gl}{color} │ {c_icono_tit}{icono_tit} {color}{sec['nombre'].upper()}{reset}"
                else:
                    formato_titulo = f"{pared_izq_gl}{c_gl}{mov_adel_gl}│{mov_atras_gl}{reset}{color}{mov_adelante}│{mov_atras} │ {c_icono_tit}{icono_tit} {color}{sec['nombre'].upper()}{reset}" if usar_caja_global else f"{pared_izq_gl}{color}{mov_adelante}│{mov_atras} │ {c_icono_tit}{icono_tit} {color}{sec['nombre'].upper()}{reset}"
                modulos.append({"type": "custom", "format": formato_titulo})
            else:
                # Si no hay cuadrado, usamos el icono libremente en vez del triángulo fijo
                formato_titulo = f"{pared_izq_gl} {c_icono_tit}{icono_tit} {color}{sec['nombre'].upper()}{reset}"
                if usar_caja_global and not es_vista_previa:
                    formato_titulo = f"{pared_izq_gl}{c_gl}{mov_adel_gl}│{mov_atras_gl}{reset} {c_icono_tit}{icono_tit} {color}{sec['nombre'].upper()}{reset}"
                modulos.append({"type": "custom", "format": formato_titulo})

            total = len(sec['modulos'])
            for i, mod_dict in enumerate(sec['modulos']):

                # Compatibilidad por si hay módulos antiguos guardados como texto puro
                if isinstance(mod_dict, str):
                    mod_dict = {"type": mod_dict}

                mod_type = mod_dict.get("type", "unknown")

                # 1. Definimos el dibujo de la izquierda
                if sec['cuadrado']:
                    if sec['arbol']:
                        prefijo = " │ ├─ " if i < total - 1 else " │ └─ "
                    else:
                        prefijo = " │   "
                else:
                    if sec['arbol']:
                        prefijo = " ├─ " if i < total - 1 else " └─ "
                    else:
                        prefijo = "   "

                # 2. Determinar el nombre a mostrar (usamos el texto custom si existe)
                nombre_mostrar = mod_type.capitalize()
                if "custom_text" in mod_dict and mod_dict["custom_text"]:
                    nombre_mostrar = mod_dict["custom_text"]

                if usar_iconos and (mod_type in iconos or "icon_custom" in mod_dict):
                    # Usamos el icono custom si lo tiene, si no el normal
                    icono_final = mod_dict.get("icon_custom", iconos.get(mod_type, "󰏫"))

                    # Color del icono específico de este módulo
                    mod_icon_color = mod_dict.get("icon_color", "0")
                    c_icono_mod = f"\u001b[0;{mod_icon_color}m" if mod_icon_color != "0" else ""

                    if c_icono_mod:
                        nombre_mostrar = f"{c_icono_mod}{icono_final}{color} {nombre_mostrar}"
                    elif c_icono_global:
                        nombre_mostrar = f"{c_icono_global}{icono_final}{color} {nombre_mostrar}"
                    else:
                        nombre_mostrar = f"{icono_final} {nombre_mostrar}"

                # 3. Aplicamos la magia según el motor
                if es_vista_previa:
                    key_str = f"{pared_izq_gl}{color}{prefijo}{nombre_mostrar}{color_val_ansi}"
                    if mod_type == "custom":
                        mod_obj = {"type": "custom", "format": key_str}
                    else:
                        mod_obj = {"type": mod_type, "key": key_str}
                else:
                    # MODO TERMINAL REAL
                    linea = f"{pared_izq_gl}"
                    if usar_caja_global:
                        linea += f"{c_gl}{mov_adel_gl}│{mov_atras_gl}{reset}"
                    linea += f"{color}"
                    if sec['cuadrado']:
                        linea += f"{mov_adelante}│{mov_atras}"
                    linea += f"{prefijo}{nombre_mostrar}{reset}"

                    if mod_type == "custom":
                        mod_obj = {"type": "custom", "format": linea}
                    else:
                        mod_obj = {"type": mod_type, "key": linea}
                        if color_val_num != '0':
                            mod_obj["outputColor"] = color_val_num

               # 4. Inyectar los parámetros nativos configurados (text, location, folders...)
                for k, v in mod_dict.items():
                    # Filtramos nuestras variables internas para no ensuciar el JSON
                    if k not in ["type", "custom_text", "icon_color", "usar_barra", "icon_custom"]:
                        if v != "": # Ignoramos campos vacíos para no romper fastfetch
                            mod_obj[k] = v

                # Magia de la barra de progreso
                if mod_dict.get("usar_barra", False):
                    # Tipo 3 le dice a Fastfetch que pinte el valor + la barra
                    mod_obj["percent"] = {"type": 3}

                modulos.append(mod_obj)

            if sec['cuadrado']:
                linea_inf = "─" * ancho_int
                format_inf = f"{pared_izq_gl}{color} └{linea_inf}┘{reset}"
                if usar_caja_global and not es_vista_previa:
                    format_inf = f"{pared_izq_gl}{c_gl}{mov_adel_gl}│{mov_atras_gl}{reset}{color} └{linea_inf}┘{reset}"
                modulos.append({"type": "custom", "format": format_inf})

            # Espaciado entre secciones (Padding)
            espacio = self.spin_padding_secciones.value() if hasattr(self, 'spin_padding_secciones') else 1

            # Si es la última sección y NO hay caja global, no hace falta salto extra al final
            if idx_sec == total_secciones - 1 and not usar_caja_global:
                espacio = 0

            for _ in range(espacio):
                if usar_caja_global:
                    if es_vista_previa:
                        modulos.append({"type": "custom", "format": f"{c_gl}│{reset}"})
                    else:
                        modulos.append({"type": "custom", "format": f"{pared_izq_gl}{c_gl}{mov_adel_gl}│{mov_atras_gl}{reset}"})
                else:
                    modulos.append("break")

        if usar_caja_global:
            # Cerramos la caja global por abajo
            modulos.append({"type": "custom", "format": f"{c_gl}└{'─'*guiones_totales}┘\u001b[0m"})

        # Obtener el tipo de logo
        tipo_logo = "auto"
        if hasattr(self, 'cmb_logo'):
            idx = self.cmb_logo.currentIndex()
            if idx == 1: tipo_logo = "small"
            elif idx == 2: tipo_logo = "none"
            elif idx == 3: tipo_logo = "custom"

        # Obtener los paddings
        pad_top = self.spin_pad_top.value() if hasattr(self, 'spin_pad_top') else 1
        pad_left = self.spin_pad_left.value() if hasattr(self, 'spin_pad_left') else 2
        pad_right = self.spin_pad_right.value() if hasattr(self, 'spin_pad_right') else 3

        # Configuración dinámica del logo
        logo_config = {
            "padding": { "top": pad_top, "left": pad_left, "right": pad_right }
        }

        # Inyectamos source y width si es imagen, o el tipo si es logo del sistema
        if es_vista_previa and tipo_logo == "custom":
            # MODO VISTA PREVIA: Evitamos enviar datos binarios de la imagen que rompen el UTF-8
            logo_config["type"] = "auto"
        elif tipo_logo == "custom" and hasattr(self, 'ruta_imagen_custom') and self.ruta_imagen_custom:
            logo_config["source"] = self.ruta_imagen_custom
            logo_config["width"] = self.spin_img_width.value() if hasattr(self, 'spin_img_width') else 30
        else:
            logo_config["type"] = tipo_logo if tipo_logo != "custom" else "auto"

        # Obtener colores y caracteres de la barra global
        txt_lleno = self.cmb_barra_lleno.currentText() if hasattr(self, 'cmb_barra_lleno') else tr("Automático (Dinámico)")
        txt_vacio = self.cmb_barra_vacio.currentText() if hasattr(self, 'cmb_barra_vacio') else tr("Automático (Dinámico)")
        txt_chars = self.cmb_barra_chars.currentText() if hasattr(self, 'cmb_barra_chars') else "█ / ▒"

        # Separar el carácter de la parte llena y la vacía (ej: "█" y "▒")
        char_lleno_base = txt_chars.split(" / ")[0]
        char_vacio_base = txt_chars.split(" / ")[1]

        if "Automático" in txt_lleno or "Automatic" in txt_lleno:
            char_lleno = char_lleno_base
        else:
            color_num = txt_lleno.split("(")[1].replace(")", "")
            char_lleno = f"\u001b[0;{color_num}m{char_lleno_base}\u001b[0m"

        if "Automático" in txt_vacio or "Automatic" in txt_vacio:
            char_vacio = char_vacio_base
        else:
            color_num = txt_vacio.split("(")[1].replace(")", "")
            char_vacio = f"\u001b[0;{color_num}m{char_vacio_base}\u001b[0m"

        # Construir el objeto JSON final
        datos = {
            "$schema": "https://github.com/fastfetch-cli/fastfetch/raw/master/doc/json_schema.json",
            "$gui_config": {
                "secciones_datos": self.secciones_datos,
                "ancho_int": self.spin_ancho.value() if hasattr(self, 'spin_ancho') else 40,
                "logo_index": self.cmb_logo.currentIndex() if hasattr(self, 'cmb_logo') else 0,
                "pad_top": self.spin_pad_top.value() if hasattr(self, 'spin_pad_top') else 1,
                "pad_left": self.spin_pad_left.value() if hasattr(self, 'spin_pad_left') else 2,
                "pad_right": self.spin_pad_right.value() if hasattr(self, 'spin_pad_right') else 3,
                "caja_global": self.chk_caja_global.isChecked() if hasattr(self, 'chk_caja_global') else False,
                "color_global": self.cmb_color_global.currentIndex() if hasattr(self, 'cmb_color_global') else 0,
                "titulo_global": self.txt_titulo_global.text() if hasattr(self, 'txt_titulo_global') else "",
                "alineacion_global": self.cmb_alineacion_global.currentIndex() if hasattr(self, 'cmb_alineacion_global') else 0,
                "ruta_imagen": getattr(self, 'ruta_imagen_custom', ""),
                "usar_iconos": self.chk_iconos.isChecked() if hasattr(self, 'chk_iconos') else True,
                "color_iconos": self.cmb_color_iconos.currentIndex() if hasattr(self, 'cmb_color_iconos') else 0,
                "barra_lleno": self.cmb_barra_lleno.currentIndex() if hasattr(self, 'cmb_barra_lleno') else 0,
                "barra_vacio": self.cmb_barra_vacio.currentIndex() if hasattr(self, 'cmb_barra_vacio') else 0,
                "barra_chars": self.cmb_barra_chars.currentIndex() if hasattr(self, 'cmb_barra_chars') else 0,
                "padding_top_secciones": self.spin_padding_top_secciones.value() if hasattr(self, 'spin_padding_top_secciones') else 0,
                "padding_secciones": self.spin_padding_secciones.value() if hasattr(self, 'spin_padding_secciones') else 1
            },
            "logo": logo_config,
            "display": {
                "separator": "  ",
                "color": { "keys": "white" },
                "bar": {
                    "char": {
                        "elapsed": char_lleno,
                        "total": char_vacio
                    },
                    "width": 15
                }
            },
            "modules": modulos
        }

        return datos

    def ver_en_terminal_real(self):
        if not shutil.which("fastfetch"):
            QMessageBox.warning(self, "Error", tr("Por favor, instala fastfetch primero en la pestaña 1."))
            return

        # 1. Generar configuración con el diseño actual
        datos_temp = self.generar_json_completo(es_vista_previa=False)

        # 2. Guardar en una ruta persistente (si usamos tempfile normal se borra
        # antes de que la terminal externa tenga tiempo de leerlo)
        ruta_temp = os.path.expanduser("~/.config/fastfetch/preview.jsonc")
        os.makedirs(os.path.dirname(ruta_temp), exist_ok=True)

        try:
            with open(ruta_temp, 'w', encoding='utf-8') as f:
                json.dump(datos_temp, f)

            sistema = platform.system()

            # Lanzamos la terminal nativa y metemos un 'pause/read' para que
            # la ventana no se cierre de golpe al terminar de imprimir fastfetch
            if sistema == "Windows":
                comando = f'fastfetch --config "{ruta_temp}" & pause'
                subprocess.Popen(['start', 'cmd', '/c', comando], shell=True)

            elif sistema == "Darwin": # macOS
                comando_mac = f'fastfetch --config "{ruta_temp}"; read -p "Presiona Enter para cerrar..."'
                subprocess.Popen(['osascript', '-e', f'tell application "Terminal" to do script "{comando_mac}"'])

            elif sistema == "Linux":
                comando_linux = f'fastfetch --config "{ruta_temp}"; read -p "Presiona Enter para cerrar..."'

                # Lista de terminales comunes en Linux (arrancará la primera que encuentre, como tu Konsole)
                terminales = ["konsole", "gnome-terminal", "xfce4-terminal", "alacritty", "kitty", "xterm"]
                lanzado = False
                for term in terminales:
                    if shutil.which(term):
                        if term == "gnome-terminal":
                            subprocess.Popen([term, '--', 'bash', '-c', comando_linux])
                        else:
                            subprocess.Popen([term, '-e', 'bash', '-c', comando_linux])
                        lanzado = True
                        break

                if not lanzado:
                    QMessageBox.warning(self, "Error", "No se encontró un emulador de terminal compatible (konsole, gnome-terminal, etc).")

        except Exception as e:
            QMessageBox.warning(self, "Error", f"No se pudo abrir la terminal: {e}")

    def update_preview(self):
        # Evita errores si esta función se dispara antes de que la interfaz esté 100% construida
        if not hasattr(self, 'txt_preview'):
            return

        if not shutil.which("fastfetch"):
            self.txt_preview.setText(tr("Por favor, instala fastfetch primero en la pestaña 1."))
            return

        # 1. Generar configuración temporal en modo básico compatible con HTML
        datos_temp = self.generar_json_completo(es_vista_previa=True)

        try:
            # 2. Guardar en un archivo temporal
            with tempfile.NamedTemporaryFile(mode='w', suffix='.jsonc', delete=False) as f:
                json.dump(datos_temp, f)
                temp_path = f.name

            # 3. Ejecutar fastfetch leyendo ese archivo temporal.
            # Engañamos al sistema de entorno para forzar a fastfetch a usar colores
            # aunque detecte que no se está ejecutando en una terminal real.
            env = os.environ.copy()
            env["COLORTERM"] = "truecolor"

            result = subprocess.run(
                ["fastfetch", "--config", temp_path],
                capture_output=True, text=True, env=env
            )
            os.remove(temp_path) # Limpiamos la basura

            # 4. Traducir la maraña ANSI a HTML
            conv = Ansi2HTMLConverter(inline=True, dark_bg=True)
            html = conv.convert(result.stdout)

            # 5. Envolver en un div con fondo oscuro y forzar la fuente Nerd Font para los iconos
            html_final = f"""
            <div style="background-color: #1e1e2e; padding: 10px; font-family: 'Hack Nerd Font Mono', monospace; font-size: 13px;">
                {html}
            </div>
            """
            self.txt_preview.setHtml(html_final)

        except Exception as e:
            self.txt_preview.setText(f"Error al ejecutar fastfetch: {e}")

    def on_tab_changed(self, index):
        # Si el usuario hace clic en la pestaña 3, actualizamos la vista previa
        if index == 2:
            self.update_preview()

if __name__ == "__main__":
    # Truco para que Windows reconozca el icono en la barra de tareas al compilar
    if platform.system() == "Windows":
        import ctypes
        myappid = 'anabasasoft.fastfetchconfig.gui.1.0'
        try:
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        except Exception:
            pass

    app = QApplication(sys.argv)

    # --- Aplicar el icono globalmente ---
    ruta_icono = resource_path("icono.png")
    app.setWindowIcon(QIcon(ruta_icono))

    window = FastfetchConfigurator()
    window.showMaximized()
    sys.exit(app.exec())
