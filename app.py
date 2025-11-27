import tkinter as tk
from tkinter import ttk


class App(tk.Tk):
	def __init__(self):
		super().__init__()
		self.title("Calculadora de Custo de Bolos")
		self.geometry("980x680")
		self.resizable(True, True)
		style = ttk.Style()
		style.theme_use("clam")
		style.configure("TFrame", background="#f5f5fa")
		style.configure("TLabelframe", background="#f5f5fa", borderwidth=1, relief="solid")
		style.configure("TLabelframe.Label", background="#f5f5fa", foreground="#333333")
		style.configure("TLabel", background="#f5f5fa", foreground="#333333")
		style.configure("TButton", background="#4e73df", foreground="white", padding=6)
		style.map("TButton", background=[("active", "#2e59d9")])
		self._build_widgets()
		self.after(100, self._centralizar_janela)

	def _build_widgets(self):
		container = ttk.Frame(self)
		container.pack(fill=tk.BOTH, expand=True)

		self.canvas = tk.Canvas(container, background="#f5f5fa", highlightthickness=0)
		scrollbar = ttk.Scrollbar(container, orient="vertical", command=self.canvas.yview)
		self.canvas.configure(yscrollcommand=scrollbar.set)

		scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
		self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

		main = ttk.Frame(self.canvas, padding=16)
		self.canvas.create_window((0, 0), window=main, anchor="nw")

		def on_configure(event):
			self.canvas.configure(scrollregion=self.canvas.bbox("all"))

		main.bind("<Configure>", on_configure)

		def _on_mousewheel(event):
			if event.num == 5 or event.delta < 0:
				self.canvas.yview_scroll(1, "units")
			elif event.num == 4 or event.delta > 0:
				self.canvas.yview_scroll(-1, "units")

		self.canvas.bind_all("<MouseWheel>", _on_mousewheel)
		self.canvas.bind_all("<Button-4>", _on_mousewheel)
		self.canvas.bind_all("<Button-5>", _on_mousewheel)

		self.vars = {}

		titulo = ttk.Label(main, text="Calculadora de Custo de Bolos", font=("Segoe UI", 16, "bold"))
		titulo.grid(row=0, column=0, columnspan=3, sticky="w", pady=(0, 10))

		bloco_ingredientes = ttk.LabelFrame(main, text="Ingredientes")
		bloco_ingredientes.grid(row=1, column=0, columnspan=3, sticky="nsew", pady=(0, 12))

		self._build_ingrediente_section(bloco_ingredientes, "Massa", "massa")
		self._build_ingrediente_section(bloco_ingredientes, "Recheio", "recheio")
		self._build_ingrediente_section(bloco_ingredientes, "Cobertura", "cobertura")

		bloco_resumo = ttk.LabelFrame(main, text="Resumo e Venda")
		bloco_resumo.grid(row=2, column=0, columnspan=3, sticky="nsew")

		campos_resumo = [
			("Topper", "topper"),
			("Mão de obra (V.hora)", "hora"),
			("Custo fixo", "fixo"),
			("Margem lucro %", "margem"),
		]

		for i, (label, key) in enumerate(campos_resumo):
			ttk.Label(bloco_resumo, text=label).grid(row=i, column=0, sticky=tk.W, pady=4, padx=(4, 8))
			var = tk.StringVar()
			entry = ttk.Entry(bloco_resumo, textvariable=var, width=18)
			entry.grid(row=i, column=1, sticky=tk.W, pady=4)
			self.vars[key] = var

		botao_calcular = ttk.Button(bloco_resumo, text="Calcular", command=self.calcular)
		botao_calcular.grid(row=len(campos_resumo), column=0, columnspan=2, pady=10, sticky=tk.EW, padx=4)

		sep = ttk.Separator(bloco_resumo, orient=tk.HORIZONTAL)
		sep.grid(row=len(campos_resumo) + 1, column=0, columnspan=3, sticky="ew", pady=5)

		self.result_custo = tk.StringVar()
		self.result_valor_bolo = tk.StringVar()
		self.result_preco_venda = tk.StringVar()
		self.result_lucro = tk.StringVar()

		ttk.Label(bloco_resumo, text="Custo ingredientes + fixos:").grid(
			row=len(campos_resumo) + 2, column=0, sticky=tk.W, pady=3
		)
		ttk.Label(bloco_resumo, textvariable=self.result_custo).grid(
			row=len(campos_resumo) + 2, column=1, sticky=tk.W
		)

		ttk.Label(bloco_resumo, text="Valor bolo (custo total):").grid(
			row=len(campos_resumo) + 3, column=0, sticky=tk.W, pady=3
		)
		ttk.Label(bloco_resumo, textvariable=self.result_valor_bolo).grid(
			row=len(campos_resumo) + 3, column=1, sticky=tk.W
		)

		ttk.Label(bloco_resumo, text="Preço de venda sugerido:").grid(
			row=len(campos_resumo) + 4, column=0, sticky=tk.W, pady=3
		)
		ttk.Label(bloco_resumo, textvariable=self.result_preco_venda).grid(
			row=len(campos_resumo) + 4, column=1, sticky=tk.W
		)

		ttk.Label(bloco_resumo, text="Lucro estimado:").grid(
			row=len(campos_resumo) + 5, column=0, sticky=tk.W, pady=3
		)
		ttk.Label(bloco_resumo, textvariable=self.result_lucro).grid(
			row=len(campos_resumo) + 5, column=1, sticky=tk.W
		)

	def _centralizar_janela(self):
		self.update_idletasks()
		largura = self.winfo_width()
		altura = self.winfo_height()
		x = (self.winfo_screenwidth() // 2) - (largura // 2)
		y = (self.winfo_screenheight() // 2) - (altura // 2)
		self.geometry(f"{largura}x{altura}+{x}+{y}")

	def _build_ingrediente_section(self, parent, titulo, prefixo):
		frame = ttk.LabelFrame(parent, text=titulo)
		if prefixo == "massa":
			linha = 0
			coluna = 0
		elif prefixo == "recheio":
			linha = 0
			coluna = 1
		else:
			linha = 0
			coluna = 2
		frame.grid(row=linha, column=coluna, padx=6, pady=6, sticky="nsew")

		ttk.Label(frame, text="Ingrediente").grid(row=0, column=0, padx=4, pady=(0, 2))
		ttk.Label(frame, text="Valor").grid(row=0, column=1, padx=4, pady=(0, 2))
		ttk.Label(frame, text="").grid(row=0, column=2, padx=4, pady=(0, 2))
		self.vars[f"{prefixo}_frame"] = frame
		self.vars[f"{prefixo}_itens"] = []
		self.vars[f"{prefixo}_linha"] = 1

		botao_add = ttk.Button(frame, text="+", width=2,
			       command=lambda p=prefixo: self._add_item(p))
		botao_add.grid(row=0, column=3, padx=2)

		total_var = tk.StringVar()
		self.vars[prefixo] = total_var
		ttk.Label(frame, text="Total").grid(row=100, column=0, sticky=tk.E, pady=(4, 0))
		ttk.Label(frame, textvariable=total_var).grid(row=100, column=1, sticky=tk.W, pady=(4, 0))

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

		custo_ingredientes = massa + recheio + cobertura + topper
		custo_trabalho = valor_hora
		custo_total = custo_ingredientes + custo_trabalho + custo_fixo

		preco_venda = custo_total * (1 + margem / 100.0)
		lucro = preco_venda - custo_total

		self.vars["massa"].set(f"R$ {massa:.2f}")
		self.vars["recheio"].set(f"R$ {recheio:.2f}")
		self.vars["cobertura"].set(f"R$ {cobertura:.2f}")

		self.result_custo.set(f"R$ {custo_ingredientes + custo_fixo:.2f}")
		self.result_valor_bolo.set(f"R$ {custo_total:.2f}")
		self.result_preco_venda.set(f"R$ {preco_venda:.2f}")
		self.result_lucro.set(f"R$ {lucro:.2f}")

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
		linha = self.vars.get(f"{prefixo}_linha", 1)
		if frame is None:
			return
		nome_var = tk.StringVar()
		valor_var = tk.StringVar()
		entry_nome = ttk.Entry(frame, textvariable=nome_var, width=18)
		entry_nome.grid(row=linha, column=0, pady=2, padx=2)
		entry_valor = ttk.Entry(frame, textvariable=valor_var, width=10)
		entry_valor.grid(row=linha, column=1, pady=2, padx=2)
		entry_valor.bind("<KeyRelease>", lambda e, p=prefixo: self._atualiza_total_secao(p))
		botao_del = ttk.Button(frame, text="X", width=2,
							   command=lambda p=prefixo, l=linha: self._remove_item(p, l))
		botao_del.grid(row=linha, column=2, padx=2)

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


if __name__ == "__main__":
	app = App()
	app.mainloop()

