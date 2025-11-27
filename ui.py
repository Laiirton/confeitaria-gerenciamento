import customtkinter as ctk

from core import calcular_custos


class App(ctk.CTk):
	def __init__(self):
		super().__init__()
		ctk.set_appearance_mode("dark")
		ctk.set_default_color_theme("blue")
		self.title("Calculadora de Custo de Bolos")
		self.geometry("1100x720")
		self.minsize(900, 600)
		self.resizable(True, True)
		self._build_widgets()
		self.after(100, self._centralizar_janela)

	def _build_widgets(self):
		main = ctk.CTkFrame(self, corner_radius=0, fg_color="#020617")
		main.pack(fill="both", expand=True)
		main.grid_columnconfigure(0, weight=3)
		main.grid_columnconfigure(1, weight=1)
		main.grid_rowconfigure(2, weight=1)

		self.vars = {}

		# Estilos
		font_title = ("Segoe UI", 24, "bold")
		font_subtitle = ("Segoe UI", 14)
		font_section = ("Segoe UI", 18, "bold")
		font_label = ("Segoe UI", 14)
		font_value = ("Segoe UI", 14)
		font_result_label = ("Segoe UI", 14)
		font_result_value = ("Segoe UI", 16, "bold")

		titulo = ctk.CTkLabel(main, text="Calculadora de Custo de Bolos", font=font_title)
		titulo.grid(row=0, column=0, columnspan=2, sticky="w", pady=(20, 5), padx=24)

		descricao = ctk.CTkLabel(main, text="Organize ingredientes e veja custo, preço e lucro do bolo.",
				       font=font_subtitle, text_color="gray70")
		descricao.grid(row=1, column=0, columnspan=2, sticky="w", padx=24, pady=(0, 20))

		container_ingredientes = ctk.CTkFrame(main, corner_radius=16, fg_color="#0b1220")
		container_ingredientes.grid(row=2, column=0, sticky="nsew", pady=(0, 16), padx=(24, 12))
		container_ingredientes.grid_rowconfigure(0, weight=1)
		container_ingredientes.grid_columnconfigure(0, weight=1)
		
		canvas = ctk.CTkCanvas(container_ingredientes, highlightthickness=0, bg="#0b1220")
		canvas.grid(row=0, column=0, sticky="nsew")
		
		barra_scroll = ctk.CTkScrollbar(container_ingredientes, orientation="vertical", command=canvas.yview)
		barra_scroll.grid(row=0, column=1, sticky="ns")
		canvas.configure(yscrollcommand=barra_scroll.set)
		
		bloco_ingredientes = ctk.CTkFrame(canvas, corner_radius=16, fg_color="#0b1220")
		canvas.create_window((0, 0), window=bloco_ingredientes, anchor="nw")
		bloco_ingredientes.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
		
		def _on_mousewheel(ev):
			canvas.yview_scroll(int(-1 * (ev.delta / 120)), "units")
		canvas.bind_all("<MouseWheel>", _on_mousewheel)
		
		bloco_ingredientes.grid_columnconfigure(0, weight=1)
		bloco_ingredientes.grid_columnconfigure(1, weight=1)
		bloco_ingredientes.grid_columnconfigure(2, weight=1)

		self._build_ingrediente_section(bloco_ingredientes, "Massa", "massa")
		self._build_ingrediente_section(bloco_ingredientes, "Recheio", "recheio")
		self._build_ingrediente_section(bloco_ingredientes, "Cobertura", "cobertura")

		bloco_resumo = ctk.CTkFrame(main, corner_radius=16, fg_color="#0b1220")
		bloco_resumo.grid(row=2, column=1, sticky="nsew", padx=(12, 24), pady=(0, 16))
		bloco_resumo.grid_columnconfigure(1, weight=1)

		resumo_titulo = ctk.CTkLabel(bloco_resumo, text="Resumo e Venda", font=font_section)
		resumo_titulo.grid(row=0, column=0, columnspan=2, sticky="w", pady=(20, 15), padx=20)

		campos_resumo = [
			("Topper", "topper", "R$ 0.00"),
			("Mão de obra (V.hora)", "hora", "R$ 0.00"),
			("Custo fixo", "fixo", "R$ 0.00"),
			("Margem lucro %", "margem", "50%"),
		]

		for i, (label, key, placeholder) in enumerate(campos_resumo, start=1):
			ctk.CTkLabel(bloco_resumo, text=label, font=font_label).grid(row=i, column=0, sticky="w", pady=8, padx=20)
			var = ctk.StringVar()
			entry = ctk.CTkEntry(bloco_resumo, textvariable=var, placeholder_text=placeholder, font=font_value)
			entry.grid(row=i, column=1, sticky="ew", pady=8, padx=(0, 20))
			self.vars[key] = var

		botao_calcular = ctk.CTkButton(bloco_resumo, text="CALCULAR", command=self.calcular,
					      height=45, font=("Segoe UI", 15, "bold"), fg_color="#2563eb", hover_color="#1d4ed8")
		botao_calcular.grid(row=len(campos_resumo) + 1, column=0, columnspan=2, pady=25, padx=20, sticky="ew")

		self.result_custo = ctk.StringVar(value="R$ 0.00")
		self.result_valor_bolo = ctk.StringVar(value="R$ 0.00")
		self.result_preco_venda = ctk.StringVar(value="R$ 0.00")
		self.result_lucro = ctk.StringVar(value="R$ 0.00")

		row_base = len(campos_resumo) + 2
		
		# Separator
		ctk.CTkFrame(bloco_resumo, height=2, fg_color="gray30").grid(row=row_base, column=0, columnspan=2, sticky="ew", padx=20, pady=(0, 15))
		row_base += 1

		def add_result_row(label_text, var, row, highlight=False):
			font_l = font_result_label
			font_v = font_result_value
			color = "white"
			if highlight:
				font_l = ("Segoe UI", 15, "bold")
				font_v = ("Segoe UI", 18, "bold")
				color = "#4ade80" # Greenish

			ctk.CTkLabel(bloco_resumo, text=label_text, font=font_l).grid(
				row=row, column=0, sticky="w", pady=4, padx=20
			)
			ctk.CTkLabel(bloco_resumo, textvariable=var, font=font_v, text_color=color).grid(
				row=row, column=1, sticky="e", padx=20
			)

		add_result_row("Custo ingredientes + fixos:", self.result_custo, row_base)
		add_result_row("Valor bolo (custo total):", self.result_valor_bolo, row_base + 1)
		add_result_row("Preço de venda sugerido:", self.result_preco_venda, row_base + 2, highlight=True)
		add_result_row("Lucro estimado:", self.result_lucro, row_base + 3, highlight=True)

	def _centralizar_janela(self):
		self.update_idletasks()
		largura = self.winfo_width()
		altura = self.winfo_height()
		x = (self.winfo_screenwidth() // 2) - (largura // 2)
		y = (self.winfo_screenheight() // 2) - (altura // 2)
		self.geometry(f"{largura}x{altura}+{x}+{y}")

	def _build_ingrediente_section(self, parent, titulo, prefixo):
		frame = ctk.CTkFrame(parent, corner_radius=12, fg_color="#020617")
		if prefixo == "massa":
			linha = 0
			coluna = 0
		elif prefixo == "recheio":
			linha = 1
			coluna = 0
		else:
			linha = 2
			coluna = 0
		frame.grid(row=linha, column=coluna, padx=12, pady=8, sticky="nsew")

		titulo_label = ctk.CTkLabel(frame, text=titulo, font=("Segoe UI", 16, "bold"))
		titulo_label.grid(row=0, column=0, columnspan=3, sticky="w", pady=(10, 4), padx=12)

		ctk.CTkLabel(frame, text="Ingrediente", font=("Segoe UI", 12)).grid(row=1, column=0, sticky="w", padx=12, pady=(0, 2))
		ctk.CTkLabel(frame, text="Valor (R$)", font=("Segoe UI", 12)).grid(row=1, column=1, sticky="w", padx=12, pady=(0, 2))
		
		self.vars[f"{prefixo}_frame"] = frame
		self.vars[f"{prefixo}_itens"] = []
		self.vars[f"{prefixo}_linha"] = 2

		total_var = ctk.StringVar(value="R$ 0.00")
		self.vars[prefixo] = total_var
		ctk.CTkLabel(frame, text="Total", font=("Segoe UI", 12, "bold")).grid(row=100, column=0, sticky="e", pady=(8, 10), padx=12)
		ctk.CTkLabel(frame, textvariable=total_var, font=("Segoe UI", 12, "bold"), text_color="#4ade80").grid(row=100, column=1, sticky="w", pady=(8, 10), padx=12)

		for _ in range(4):
			self._add_item(prefixo)

	def _get_float(self, key, default=0.0):
		value = self.vars[key].get().replace(",", ".").strip()
		if not value:
			return default
		try:
			return float(value)
		except ValueError:
			return default

	def calcular(self):
		massa = self._soma_itens("massa")
		recheio = self._soma_itens("recheio")
		cobertura = self._soma_itens("cobertura")
		topper = self._get_float("topper")
		valor_hora = self._get_float("hora")
		custo_fixo = self._get_float("fixo")
		margem = self._get_float("margem", 50.0)

		resultado = calcular_custos(massa, recheio, cobertura, topper, valor_hora, custo_fixo, margem)

		self.vars["massa"].set(f"R$ {massa:.2f}")
		self.vars["recheio"].set(f"R$ {recheio:.2f}")
		self.vars["cobertura"].set(f"R$ {cobertura:.2f}")

		self.result_custo.set(f"R$ {resultado['custo_ingredientes'] + custo_fixo:.2f}")
		self.result_valor_bolo.set(f"R$ {resultado['custo_total']:.2f}")
		self.result_preco_venda.set(f"R$ {resultado['preco_venda']:.2f}")
		self.result_lucro.set(f"R$ {resultado['lucro']:.2f}")

	def _soma_itens(self, prefixo):
		itens = self.vars.get(f"{prefixo}_itens", [])
		total = 0.0
		for _, _, valor_var in itens:
			valor = valor_var.get().replace(",", ".").strip()
			if not valor:
				continue
			try:
				total += float(valor)
			except ValueError:
				continue
		return total

	def _add_item(self, prefixo):
		frame = self.vars.get(f"{prefixo}_frame")
		linha = self.vars.get(f"{prefixo}_linha", 2)
		if frame is None:
			return
		for widget in frame.grid_slaves(row=linha):
			if isinstance(widget, ctk.CTkButton) and widget.cget("text") == "+":
				widget.destroy()
		nome_var = ctk.StringVar()
		valor_var = ctk.StringVar()
		
		entry_nome = ctk.CTkEntry(frame, textvariable=nome_var, width=280, placeholder_text="Nome do ingrediente")
		entry_nome.grid(row=linha, column=0, pady=3, padx=12, sticky="ew")
		
		entry_valor = ctk.CTkEntry(frame, textvariable=valor_var, width=100, placeholder_text="0.00")
		entry_valor.grid(row=linha, column=1, pady=3, padx=12)
		entry_valor.bind("<KeyRelease>", lambda e, p=prefixo: self._atualiza_total_secao(p))
		
		botao_del = ctk.CTkButton(frame, text="X", width=32, fg_color="#ef4444", hover_color="#dc2626",
					   command=lambda p=prefixo, l=linha: self._remove_item(p, l))
		botao_del.grid(row=linha, column=2, padx=4)

		self.vars[f"{prefixo}_itens"].append((linha, nome_var, valor_var))
		self.vars[f"{prefixo}_linha"] = linha + 1
		proxima_linha = self.vars[f"{prefixo}_linha"]
		botao_add = ctk.CTkButton(frame, text="+", width=32, fg_color="#3b82f6", hover_color="#2563eb",
			       command=lambda p=prefixo: self._add_item(p))
		botao_add.grid(row=proxima_linha, column=2, padx=4, pady=(4, 0))
		self._atualiza_total_secao(prefixo)

	def _atualiza_total_secao(self, prefixo):
		total = self._soma_itens(prefixo)
		if prefixo in self.vars:
			self.vars[prefixo].set(f"R$ {total:.2f}")

	def _remove_item(self, prefixo, linha):
		frame = self.vars.get(f"{prefixo}_frame")
		if frame is None:
			return
		itens = self.vars.get(f"{prefixo}_itens", [])
		novos_itens = []
		for l, nome_var, valor_var in itens:
			if l == linha:
				for widget in frame.grid_slaves(row=l):
					widget.destroy()
			else:
				novos_itens.append((l, nome_var, valor_var))
		self.vars[f"{prefixo}_itens"] = novos_itens
		self._atualiza_total_secao(prefixo)


def main():
	app = App()
	app.mainloop()

