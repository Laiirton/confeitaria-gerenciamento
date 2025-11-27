def calcular_custos(massa, recheio, cobertura, topper, valor_hora, custo_fixo, margem):
	custo_ingredientes = massa + recheio + cobertura + topper
	custo_trabalho = valor_hora
	custo_total = custo_ingredientes + custo_trabalho + custo_fixo
	preco_venda = custo_total * (1 + margem / 100.0)
	lucro = preco_venda - custo_total
	return {
		"custo_ingredientes": custo_ingredientes,
		"custo_total": custo_total,
		"preco_venda": preco_venda,
		"lucro": lucro,
	}

