import tkinter as tk
from tkinter import ttk, messagebox, font
import pandas as pd
from datetime import datetime
import os
import hashlib
import json

class SistemaCitasMedicas:
    def __init__(self):
        # Archivos del sistema
        self.archivo_citas = "citas_medicas.xlsx"
        self.archivo_usuarios = "usuarios.json"
        
        # Variables de sesión
        self.usuario_actual = None
        self.df = None
        
        # Configuración inicial
        self.inicializar_archivos()
        self.crear_ventana_login()
    
    def inicializar_archivos(self):
        """Crear archivos necesarios si no existen"""
        # Archivo de citas
        if not os.path.exists(self.archivo_citas):
            df_vacio = pd.DataFrame(columns=["Paciente", "Fecha", "Hora", "Motivo", "Estado"])
            df_vacio.to_excel(self.archivo_citas, index=False)
        
        # Archivo de usuarios con usuario por defecto
        if not os.path.exists(self.archivo_usuarios):
            usuarios_default = {
                "admin": {
                    "password": self.hash_password("admin123"),
                    "nombre": "Administrador"
                },
                "doctor": {
                    "password": self.hash_password("doctor123"),
                    "nombre": "Dr. García"
                }
            }
            with open(self.archivo_usuarios, 'w') as f:
                json.dump(usuarios_default, f, indent=4)
    
    def hash_password(self, password):
        """Encriptar contraseña"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def verificar_credenciales(self, usuario, password):
        """Verificar login del usuario"""
        try:
            with open(self.archivo_usuarios, 'r') as f:
                usuarios = json.load(f)
            
            if usuario in usuarios:
                password_hash = self.hash_password(password)
                if usuarios[usuario]["password"] == password_hash:
                    return usuarios[usuario]["nombre"]
            return None
        except:
            return None
    
    def crear_ventana_login(self):
        """Crear ventana de login"""
        self.login_window = tk.Tk()
        self.login_window.title("Login - Sistema de Citas Médicas")
        self.login_window.geometry("400x300")
        self.login_window.configure(bg='#f0f8ff')
        
        # Centrar ventana
        self.centrar_ventana(self.login_window, 400, 300)
        
        # Título principal
        title_font = font.Font(family="Arial", size=16, weight="bold")
        tk.Label(self.login_window, text="🏥 Sistema de Citas Médicas", 
                font=title_font, bg='#f0f8ff', fg='#2c3e50').pack(pady=30)
        
        # Frame para el formulario
        form_frame = tk.Frame(self.login_window, bg='#f0f8ff')
        form_frame.pack(pady=20)
        
        # Campos de login
        tk.Label(form_frame, text="👤 Usuario:", font=("Arial", 10), 
                bg='#f0f8ff', fg='#34495e').grid(row=0, column=0, sticky='e', padx=10, pady=10)
        self.entry_usuario = tk.Entry(form_frame, font=("Arial", 10), width=20)
        self.entry_usuario.grid(row=0, column=1, padx=10, pady=10)
        
        tk.Label(form_frame, text="🔒 Contraseña:", font=("Arial", 10), 
                bg='#f0f8ff', fg='#34495e').grid(row=1, column=0, sticky='e', padx=10, pady=10)
        self.entry_password = tk.Entry(form_frame, font=("Arial", 10), width=20, show="*")
        self.entry_password.grid(row=1, column=1, padx=10, pady=10)
        
        # Botón de login
        btn_login = tk.Button(form_frame, text="Iniciar Sesión", command=self.login,
                             bg='#3498db', fg='white', font=("Arial", 10, "bold"),
                             padx=20, pady=5, relief='flat')
        btn_login.grid(row=2, column=0, columnspan=2, pady=20)
        
        # Información de usuarios de prueba
        info_frame = tk.Frame(self.login_window, bg='#f0f8ff')
        info_frame.pack(pady=10)
        
        tk.Label(info_frame, text="👥 Usuarios de prueba:", 
                font=("Arial", 9, "bold"), bg='#f0f8ff', fg='#7f8c8d').pack()
        tk.Label(info_frame, text="admin / admin123", 
                font=("Arial", 8), bg='#f0f8ff', fg='#7f8c8d').pack()
        tk.Label(info_frame, text="doctor / doctor123", 
                font=("Arial", 8), bg='#f0f8ff', fg='#7f8c8d').pack()
        
        # Bind Enter key
        self.entry_password.bind('<Return>', lambda e: self.login())
        
        self.login_window.mainloop()
    
    def centrar_ventana(self, ventana, ancho, alto):
        """Centrar ventana en la pantalla"""
        screen_width = ventana.winfo_screenwidth()
        screen_height = ventana.winfo_screenheight()
        x = (screen_width // 2) - (ancho // 2)
        y = (screen_height // 2) - (alto // 2)
        ventana.geometry(f"{ancho}x{alto}+{x}+{y}")
    
    def login(self):
        """Procesar login"""
        usuario = self.entry_usuario.get()
        password = self.entry_password.get()
        
        if not usuario or not password:
            messagebox.showerror("Error", "Complete todos los campos")
            return
        
        nombre_usuario = self.verificar_credenciales(usuario, password)
        if nombre_usuario:
            self.usuario_actual = nombre_usuario
            self.login_window.destroy()
            self.crear_ventana_principal()
        else:
            messagebox.showerror("Error", "Credenciales incorrectas")
            self.entry_password.delete(0, tk.END)
    
    def crear_ventana_principal(self):
        """Crear ventana principal del sistema"""
        self.root = tk.Tk()
        self.root.title(f"Sistema de Citas Médicas - {self.usuario_actual}")
        self.root.geometry("1200x700")
        self.root.configure(bg='#ecf0f1')
        
        # Centrar ventana
        self.centrar_ventana(self.root, 1200, 700)
        
        # Cargar datos
        self.df = pd.read_excel(self.archivo_citas)
        
        self.crear_header()
        self.crear_formulario()
        self.crear_tabla()
        self.actualizar_tabla()
        
        self.root.mainloop()
    
    def crear_header(self):
        """Crear header con título y botón de logout"""
        header_frame = tk.Frame(self.root, bg='#2c3e50', height=60)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        # Título
        title_label = tk.Label(header_frame, text="🏥 Sistema de Gestión de Citas Médicas",
                              font=("Arial", 18, "bold"), bg='#2c3e50', fg='white')
        title_label.pack(side='left', padx=20, pady=15)
        
        # Usuario y logout
        user_frame = tk.Frame(header_frame, bg='#2c3e50')
        user_frame.pack(side='right', padx=20, pady=15)
        
        tk.Label(user_frame, text=f"👤 {self.usuario_actual}",
                font=("Arial", 12), bg='#2c3e50', fg='white').pack(side='left', padx=10)
        
        btn_logout = tk.Button(user_frame, text="Cerrar Sesión", command=self.logout,
                              bg='#e74c3c', fg='white', font=("Arial", 10, "bold"),
                              padx=15, pady=5, relief='flat')
        btn_logout.pack(side='right')
    
    def crear_formulario(self):
        """Crear formulario de citas"""
        form_frame = tk.Frame(self.root, bg='white', relief='solid', bd=1)
        form_frame.pack(fill='x', padx=20, pady=10)
        
        # Título del formulario
        tk.Label(form_frame, text="📋 Gestión de Citas", 
                font=("Arial", 14, "bold"), bg='white', fg='#2c3e50').pack(pady=10)
        
        # Frame para campos
        campos_frame = tk.Frame(form_frame, bg='white')
        campos_frame.pack(pady=10)
        
        # Primera fila
        fila1 = tk.Frame(campos_frame, bg='white')
        fila1.pack(fill='x', pady=5)
        
        tk.Label(fila1, text="👤 Paciente:", font=("Arial", 10), 
                bg='white', fg='#34495e', width=12, anchor='e').pack(side='left', padx=5)
        self.entry_paciente = tk.Entry(fila1, font=("Arial", 10), width=20)
        self.entry_paciente.pack(side='left', padx=5)
        
        tk.Label(fila1, text="📅 Fecha:", font=("Arial", 10), 
                bg='white', fg='#34495e', width=12, anchor='e').pack(side='left', padx=5)
        self.entry_fecha = tk.Entry(fila1, font=("Arial", 10), width=15)
        self.entry_fecha.pack(side='left', padx=5)
        self.entry_fecha.insert(0, datetime.now().strftime("%Y-%m-%d"))
        
        # Segunda fila
        fila2 = tk.Frame(campos_frame, bg='white')
        fila2.pack(fill='x', pady=5)
        
        tk.Label(fila2, text="🕐 Hora:", font=("Arial", 10), 
                bg='white', fg='#34495e', width=12, anchor='e').pack(side='left', padx=5)
        self.entry_hora = tk.Entry(fila2, font=("Arial", 10), width=15, fg='gray')
        self.entry_hora.pack(side='left', padx=5)
        self.entry_hora.insert(0, "Ej: 4:00 PM")
        self.entry_hora.bind('<FocusIn>', self.on_entry_hora_click)
        self.entry_hora.bind('<FocusOut>', self.on_entry_hora_focusout)
        
        tk.Label(fila2, text="📝 Motivo:", font=("Arial", 10), 
                bg='white', fg='#34495e', width=12, anchor='e').pack(side='left', padx=5)
        self.entry_motivo = tk.Entry(fila2, font=("Arial", 10), width=25)
        self.entry_motivo.pack(side='left', padx=5)
        
        # Instrucciones de formato
        instrucciones_frame = tk.Frame(campos_frame, bg='white')
        instrucciones_frame.pack(fill='x', pady=5)
        
        tk.Label(instrucciones_frame, text="💡 Formatos de hora válidos: 9:00 AM, 2:30 PM, 14:30, 08:15", 
                font=("Arial", 8), bg='white', fg='#7f8c8d').pack()
        
        # Botones
        botones_frame = tk.Frame(form_frame, bg='white')
        botones_frame.pack(pady=15)
        
        btn_agendar = tk.Button(botones_frame, text="✅ Agendar", command=self.agendar_cita,
                               bg='#27ae60', fg='white', font=("Arial", 10, "bold"),
                               padx=20, pady=8, relief='flat')
        btn_agendar.pack(side='left', padx=5)
        
        btn_reprogramar = tk.Button(botones_frame, text="🔄 Reprogramar", command=self.reprogramar_cita,
                                   bg='#f39c12', fg='white', font=("Arial", 10, "bold"),
                                   padx=20, pady=8, relief='flat')
        btn_reprogramar.pack(side='left', padx=5)
        
        btn_eliminar = tk.Button(botones_frame, text="🗑️ Eliminar", command=self.eliminar_cita,
                                bg='#e74c3c', fg='white', font=("Arial", 10, "bold"),
                                padx=20, pady=8, relief='flat')
        btn_eliminar.pack(side='left', padx=5)
        
        btn_limpiar = tk.Button(botones_frame, text="🧹 Limpiar", command=self.limpiar_formulario,
                               bg='#95a5a6', fg='white', font=("Arial", 10, "bold"),
                               padx=20, pady=8, relief='flat')
        btn_limpiar.pack(side='left', padx=5)
    
    def crear_tabla(self):
        """Crear tabla de citas"""
        tabla_frame = tk.Frame(self.root, bg='white', relief='solid', bd=1)
        tabla_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Título de la tabla
        tk.Label(tabla_frame, text="📊 Lista de Citas", 
                font=("Arial", 14, "bold"), bg='white', fg='#2c3e50').pack(pady=10)
        
        # Frame para tabla y scrollbar
        tree_frame = tk.Frame(tabla_frame, bg='white')
        tree_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Tabla
        columnas = ["Paciente", "Fecha", "Hora", "Motivo", "Estado"]
        self.tabla = ttk.Treeview(tree_frame, columns=columnas, show="headings", height=15)
        
        # Configurar columnas
        for col in columnas:
            self.tabla.heading(col, text=col)
            self.tabla.column(col, width=200 if col == "Motivo" else 150, anchor='center')
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=scrollbar.set)
        
        # Posicionar tabla y scrollbar
        self.tabla.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Event binding para selección
        self.tabla.bind('<<TreeviewSelect>>', self.seleccionar_fila)
    
    def on_entry_hora_click(self, event):
        """Limpiar placeholder cuando se hace clic en el campo hora"""
        if self.entry_hora.get() == "Ej: 4:00 PM":
            self.entry_hora.delete(0, tk.END)
            self.entry_hora.config(fg='black')
    
    def on_entry_hora_focusout(self, event):
        """Restaurar placeholder si el campo está vacío"""
        if self.entry_hora.get() == "":
            self.entry_hora.insert(0, "Ej: 4:00 PM")
            self.entry_hora.config(fg='gray')
    
    def seleccionar_fila(self, event):
        """Cargar datos de fila seleccionada en el formulario"""
        seleccion = self.tabla.selection()
        if seleccion:
            item = self.tabla.item(seleccion[0])
            valores = item['values']
            
            self.limpiar_formulario()
            if len(valores) > 2:  # Asegurar que hay suficientes valores
                self.entry_paciente.insert(0, valores[0])
                self.entry_fecha.insert(0, valores[1])
                # Limpiar placeholder antes de insertar hora real
                self.entry_hora.delete(0, tk.END)
                self.entry_hora.insert(0, valores[2])
                self.entry_hora.config(fg='black')
                if len(valores) > 3:
                    self.entry_motivo.insert(0, valores[3])
    
    def agendar_cita(self):
        """Agregar nueva cita"""
        paciente = self.entry_paciente.get().strip()
        fecha = self.entry_fecha.get().strip()
        hora = self.entry_hora.get().strip()
        motivo = self.entry_motivo.get().strip()
        
        # Verificar si el campo hora tiene el placeholder
        if hora == "Ej: 4:00 PM":
            hora = ""
        
        if not paciente or not fecha or not hora:
            messagebox.showerror("Error", "Complete todos los campos obligatorios (Paciente, Fecha, Hora)")
            return
        
        # Validar formato de fecha
        try:
            datetime.strptime(fecha, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Error", "Formato de fecha incorrecto. Use YYYY-MM-DD")
            return
        
        # Validar formato de hora (acepta tanto 24h como AM/PM)
        hora_valida = False
        try:
            # Intentar formato 24 horas (HH:MM)
            datetime.strptime(hora, "%H:%M")
            hora_valida = True
        except ValueError:
            try:
                # Intentar formato 12 horas con AM/PM
                datetime.strptime(hora.upper(), "%I:%M %p")
                hora_valida = True
            except ValueError:
                pass
        
        if not hora_valida:
            messagebox.showerror("Error", "Formato de hora incorrecto. Use HH:MM o H:MM AM/PM\nEjemplos: 14:30, 2:30 PM, 4:00 AM")
            return
        
        nueva_cita = {
            "Paciente": paciente,
            "Fecha": fecha,
            "Hora": hora,
            "Motivo": motivo if motivo else "Consulta general",
            "Estado": "Agendada"
        }
        
        self.df.loc[len(self.df)] = nueva_cita
        self.guardar_citas()
        self.actualizar_tabla()
        self.limpiar_formulario()
        messagebox.showinfo("Éxito", "Cita agendada correctamente")
    
    def reprogramar_cita(self):
        """Reprogramar cita seleccionada"""
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showwarning("Atención", "Seleccione una cita para reprogramar")
            return
        
        fecha = self.entry_fecha.get().strip()
        hora = self.entry_hora.get().strip()
        motivo = self.entry_motivo.get().strip()
        
        if not fecha or not hora:
            messagebox.showerror("Error", "Complete los campos de fecha y hora")
            return
        
        # Validar formato de fecha
        try:
            datetime.strptime(fecha, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Error", "Formato de fecha incorrecto. Use YYYY-MM-DD")
            return
        
        # Validar formato de hora (acepta tanto 24h como AM/PM)
        hora_valida = False
        try:
            # Intentar formato 24 horas (HH:MM)
            datetime.strptime(hora, "%H:%M")
            hora_valida = True
        except ValueError:
            try:
                # Intentar formato 12 horas con AM/PM
                datetime.strptime(hora.upper(), "%I:%M %p")
                hora_valida = True
            except ValueError:
                pass
        
        if not hora_valida:
            messagebox.showerror("Error", "Formato de hora incorrecto. Use HH:MM o H:MM AM/PM\nEjemplos: 14:30, 2:30 PM, 4:00 AM")
            return
        
        index = self.tabla.index(seleccion[0])
        self.df.at[index, "Fecha"] = fecha
        self.df.at[index, "Hora"] = hora
        self.df.at[index, "Motivo"] = motivo if motivo else self.df.at[index, "Motivo"]
        self.df.at[index, "Estado"] = "Reprogramada"
        
        self.guardar_citas()
        self.actualizar_tabla()
        self.limpiar_formulario()
        messagebox.showinfo("Éxito", "Cita reprogramada correctamente")
    
    def eliminar_cita(self):
        """Eliminar cita seleccionada"""
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showwarning("Atención", "Seleccione una cita para eliminar")
            return
        
        respuesta = messagebox.askyesno("Confirmar", "¿Está seguro de eliminar esta cita?")
        if respuesta:
            index = self.tabla.index(seleccion[0])
            self.df = self.df.drop(self.df.index[index]).reset_index(drop=True)
            self.guardar_citas()
            self.actualizar_tabla()
            self.limpiar_formulario()
            messagebox.showinfo("Éxito", "Cita eliminada correctamente")
    
    def limpiar_formulario(self):
        """Limpiar campos del formulario"""
        self.entry_paciente.delete(0, tk.END)
        self.entry_fecha.delete(0, tk.END)
        self.entry_hora.delete(0, tk.END)
        self.entry_motivo.delete(0, tk.END)
        self.entry_fecha.insert(0, datetime.now().strftime("%Y-%m-%d"))
        # Restaurar placeholder en hora
        self.entry_hora.insert(0, "Ej: 4:00 PM")
        self.entry_hora.config(fg='gray')
    
    def guardar_citas(self):
        """Guardar citas en archivo Excel"""
        self.df.to_excel(self.archivo_citas, index=False)
    
    def actualizar_tabla(self):
        """Actualizar tabla con datos actuales"""
        for item in self.tabla.get_children():
            self.tabla.delete(item)
        
        for _, row in self.df.iterrows():
            # Agregar colores según el estado
            values = list(row)
            self.tabla.insert("", "end", values=values)
    
    def logout(self):
        """Cerrar sesión"""
        respuesta = messagebox.askyesno("Confirmar", "¿Desea cerrar sesión?")
        if respuesta:
            self.root.destroy()
            self.usuario_actual = None
            self.crear_ventana_login()

# Iniciar aplicación
if __name__ == "__main__":
    app = SistemaCitasMedicas()