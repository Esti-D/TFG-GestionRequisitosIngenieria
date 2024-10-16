def cargar_documento(entry_archivo, proyecto_id, frame_visual):
    """Extrae el texto del PDF, organiza capítulos y divide requisitos basados en los puntos y aparte."""
    ruta_archivo = entry_archivo.get()

    titulo_documento = ruta_archivo.split("/")[-1]  # Obtener solo el nombre del archivo de la ruta

    if not ruta_archivo:
        messagebox.showerror("Error", "No se ha seleccionado ningún archivo.")
        return

    try:
        texto_pdf = extraer_texto_pdf(ruta_archivo)
        if not texto_pdf:
            messagebox.showerror("Error", "No se pudo extraer texto del PDF.")
            return

        limpiar_visualizador(frame_visual)

        capitulos = re.split(r'(?=\d+\.\s)', texto_pdf)
        contenido = ""

        for capitulo in capitulos:
            capitulo = capitulo.strip()
            if not capitulo:
                continue

            match_capitulo = re.match(r'^(\d+)\.\s+(.+)', capitulo, re.DOTALL)
            if match_capitulo:
                numero_capitulo = match_capitulo.group(1)
                texto_capitulo = match_capitulo.group(2)
                contenido += f"Capítulo {numero_capitulo}:\n"
                requisitos = re.split(r'(?<=\.)\s*\n(?=[A-Z])', texto_capitulo)
                id_requisito = 1

                for requisito in requisitos:
                    if requisito.strip():
                        contenido += f"Requisito {id_requisito}: {requisito.strip()}\n"
                        id_requisito += 1

            contenido += "\n"

        if contenido:
            texto_requisitos_visualizador = tk.Text(frame_visual, wrap="word", height=20)
            texto_requisitos_visualizador.insert(tk.END, contenido)
            texto_requisitos_visualizador.pack(pady=10, padx=10, fill="both", expand=True)
        else:
            messagebox.showerror("Error", "No se pudo encontrar ningún capítulo o requisito en el documento.")

        boton_guardar = tk.Button(frame_visual, text="Guardar", 
                                  command=lambda: guardar_requisitos_y_asociaciones(titulo_documento, 
                                                                                     texto_requisitos_visualizador.get("1.0", tk.END), 
                                                                                     ruta_archivo, proyecto_id, frame_visual))
        boton_guardar.pack(pady=10)

    except Exception as e:
        print(f"Error al cargar el documento: {e}")
        messagebox.showerror("Error", f"Error al cargar el documento: {e}")
