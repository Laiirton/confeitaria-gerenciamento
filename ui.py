import customtkinter as ctk

from core import calcular_custos


class App(ctk.CTk):
	def __init__(self):
		super().__init__()
		ctk.set_appearance_mode("dark")
		ctk.set_default_color_theme("blue")
		self.title("Calculadora de Custo de Bolos")
		self.geometry("1100x720")
		self.resizable(True, True)
		self._build_widgets()
		self.after(100, self._centralizar_janela)

	def _build_widgets(self):
		container = ctk.CTkFrame(self, corner_radius=0, fg_color="#020617")
		container.pack(fill="both", expand=True)

		self.canvas = ctk.CTkCanvas(container, bg="#020617", highlightthickness=0)
		scrollbar = ctk.CTkScrollbar(container, orientation="vertical", command=self.canvas.yview)
		self.canvas.configure(yscrollcommand=scrollbar.set)

		scrollbar.pack(side="right", fill="y")
		self.canvas.pack(side="left", fill="both", expand=True)

		main = ctk.CTkFrame(self.canvas, corner_radius=0, fg_color="#020617")
		self.canvas.create_window((0, 0), window=main, anchor="nw")
		main.grid_columnconfigure(0, weight=3)
		main.grid_columnconfigure(1, weight=2)

		def on_configure(event):
			self.canvas.configure(scrollregion=self.canvas.bbox("all"))

		main.bind("<Configure>", on_configure)

		def _on_mousewheel(event):
			if event.num == 5 or event.delta < 0:
				self.canvas.yview_scroll(1, "units")
			elif event.num == 4 or event.delta > 0:
				self.canvas.yview_scroll(-1, "units")

		self.canvas.bind("<MouseWheel>", _on_mousewheel)
		self.canvas.bind("<Button-4>", _on_mousewheel)
		self.canvas.bind("<Button-5>", _on_mousewheel)

		self.vars = {}

		titulo = ctk.CTkLabel(main, text="Calculadora de Custo de Bolos", font=("Segoe UI", 22, "bold"))
		titulo.grid(row=0, column=0, columnspan=2, sticky="w", pady=(20, 10), padx=24)

		descricao = ctk.CTkLabel(main, text="Organize ingredientes e veja custo, preço e lucro do bolo.",
				       font=("Segoe UI", 12))
		descricao.grid(row=1, column=0, columnspan=2, sticky="w", padx=24, pady=(0, 20))

		bloco_ingredientes = ctk.CTkFrame(main, corner_radius=16, fg_color="#0b1220")
		bloco_ingredientes.grid(row=2, column=0, sticky="nsew", pady=(0, 16), padx=(24, 12))
		bloco_ingredientes.grid_columnconfigure(0, weight=1)
		bloco_ingredientes.grid_columnconfigure(1, weight=1)
		bloco_ingredientes.grid_columnconfigure(2, weight=1)

		self._build_ingrediente_section(bloco_ingredientes, "Massa", "massa")
		self._build_ingrediente_section(bloco_ingredientes, "Recheio", "recheio")
		self._build_ingrediente_section(bloco_ingredientes, "Cobertura", "cobertura")

		bloco_resumo = ctk.CTkFrame(main, corner_radius=16, fg_color="#0b1220")
		bloco_resumo.grid(row=2, column=1, sticky="nsew", padx=(12, 24), pady=(0, 16))

		resumo_titulo = ctk.CTkLabel(bloco_resumo, text="Resumo e Venda", font=("Segoe UI", 16, "bold"))
		resumo_titulo.grid(row=0, column=0, columnspan=2, sticky="w", pady=(16, 8), padx=16)

		campos_resumo = [
			("Topper", "topper"),
			("Mão de obra (V.hora)", "hora"),
			("Custo fixo", "fixo"),
			("Margem lucro %", "margem"),
		]

		for i, (label, key) in enumerate(campos_resumo, start=1):
			ctk.CTkLabel(bloco_resumo, text=label).grid(row=i, column=0, sticky="w", pady=6, padx=16)
			var = ctk.StringVar()
			entry = ctk.CTkEntry(bloco_resumo, textvariable=var, width=200)
			entry.grid(row=i, column=1, sticky="w", pady=6, padx=(0, 16))
			self.vars[key] = var

		botao_calcular = ctk.CTkButton(bloco_resumo, text="Calcular", command=self.calcular,
					      height=40)
		botao_calcular.grid(row=len(campos_resumo) + 1, column=0, columnspan=2, pady=14, padx=16, sticky="ew")

		self.result_custo = ctk.StringVar()
		self.result_valor_bolo = ctk.StringVar()
		self.result_preco_venda = ctk.StringVar()
		self.result_lucro = ctk.StringVar()

		row_base = len(campos_resumo) + 2
		ctk.CTkLabel(bloco_resumo, text="Custo ingredientes + fixos:").grid(
			row=row_base, column=0, sticky="w", pady=4, padx=16
		)
		ctk.CTkLabel(bloco_resumo, textvariable=self.result_custo).grid(
			row=row_base, column=1, sticky="w"
		)

		ctk.CTkLabel(bloco_resumo, text="Valor bolo (custo total):").grid(
			row=row_base + 1, column=0, sticky="w", pady=4, padx=16
		)
		ctk.CTkLabel(bloco_resumo, textvariable=self.result_valor_bolo).grid(
			row=row_base + 1, column=1, sticky="w"
		)

		ctk.CTkLabel(bloco_resumo, text="Preço de venda sugerido:").grid(
			row=row_base + 2, column=0, sticky="w", pady=4, padx=16
		)
		ctk.CTkLabel(bloco_resumo, textvariable=self.result_preco_venda).grid(
			row=row_base + 2, column=1, sticky="w"
		)

		ctk.CTkLabel(bloco_resumo, text="Lucro estimado:").grid(
			row=row_base + 3, column=0, sticky="w", pady=4, padx=16
		)
		ctk.CTkLabel(bloco_resumo, textvariable=self.result_lucro).grid(
			row=row_base + 3, column=1, sticky="w"
		)

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

		titulo_label = ctk.CTkLabel(frame, text=titulo, font=("Segoe UI", 14, "bold"))
		titulo_label.grid(row=0, column=0, columnspan=3, sticky="w", pady=(10, 4), padx=12)

		ctk.CTkLabel(frame, text="Ingrediente").grid(row=1, column=0, padx=12, pady=(0, 2))
		ctk.CTkLabel(frame, text="Valor").grid(row=1, column=1, padx=12, pady=(0, 2))
		ctk.CTkLabel(frame, text="").grid(row=1, column=2, padx=4, pady=(0, 2))
		self.vars[f"{prefixo}_frame"] = frame
		self.vars[f"{prefixo}_itens"] = []
		self.vars[f"{prefixo}_linha"] = 2

		botao_add = ctk.CTkButton(frame, text="+", width=32,
			       command=lambda p=prefixo: self._add_item(p))
		botao_add.grid(row=1, column=3, padx=8)

		total_var = ctk.StringVar()
		self.vars[prefixo] = total_var
		ctk.CTkLabel(frame, text="Total").grid(row=100, column=0, sticky="e", pady=(4, 10), padx=12)
		ctk.CTkLabel(frame, textvariable=total_var).grid(row=100, column=1, sticky="w", pady=(4, 10))

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
		nome_var = ctk.StringVar()
		valor_var = ctk.StringVar()
		entry_nome = ctk.CTkEntry(frame, textvariable=nome_var, width=180)
		entry_nome.grid(row=linha, column=0, pady=3, padx=12)
		entry_valor = ctk.CTkEntry(frame, textvariable=valor_var, width=90)
		entry_valor.grid(row=linha, column=1, pady=3, padx=12)
		entry_valor.bind("<KeyRelease>", lambda e, p=prefixo: self._atualiza_total_secao(p))
		botao_del = ctk.CTkButton(frame, text="X", width=32,
					   command=lambda p=prefixo, l=linha: self._remove_item(p, l))
		botao_del.grid(row=linha, column=2, padx=4)

		self.vars[f"{prefixo}_itens"].append((linha, nome_var, valor_var))
		self.vars[f"{prefixo}_linha"] = linha + 1
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

