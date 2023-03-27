class Telefone:
	def __init__(self):
		self.estado = "INICIO"
		self.saldo = 0
		self.moedas_validas = [5, 10, 20, 50, 100, 200]

	def get_estado(self):
		return self.estado

	def levantar(self):
		if self.estado == "INICIO":
			self.estado = "LEVANTADO"
			print("maq: Introduza moedas.")

	def pousar(self):
		if self.estado == "LEVANTADO" or self.estado == "DISCADO":
			troco = self.saldo
			self.saldo = 0
			print(f"maq: troco={troco}c; Volte sempre!")
			self.estado = "INICIO"

	def moeda(self, valores):
		if self.estado == "LEVANTADO":
			for valor in valores:
				if valor in self.moedas_validas:
					self.saldo += valor
				else:
					print(f"maq: {valor}c - moeda inválida;")
			print(f"saldo = {self.saldo}c")

	def discar(self, numero):
		if len(numero) != 9 and not numero.startswith("00"):
			print("maq: Número inválido. Queira discar novo número!")

		elif numero.startswith("601") or numero.startswith("641"):
			print("maq: Esse número não é permitido neste telefone. Queira discar novo número!")

		elif numero.startswith("00"):
			if self.saldo >= 150:
				custo_chamada = 150
				print(f"maq: saldo = {self.saldo - custo_chamada}c")
				self.estado = "DISCADO"
				return True
			else:
				print(
					f"maq: Saldo insuficiente para chamada internacional. Queira introduzir mais moedas ou discar novo número.")

		elif numero.startswith("2"):
			if self.saldo >= 25:
				custo_chamada = 25
				print(f"maq: saldo = {self.saldo - custo_chamada}c")
				self.estado = "DISCADO"
				return True
			else:
				print(
					f"maq: Saldo insuficiente para chamada nacional. Queira introduzir mais moedas ou discar novo número.")

		elif numero.startswith("800"):
			custo_chamada = 0
			print(f"maq: saldo = {self.saldo - custo_chamada}c")
			return True

		elif numero.startswith("808"):
			if self.saldo >= 10:
				custo_chamada = 10
				print(f"maq: saldo={self.saldo - custo_chamada}")
				return True

	def abortar(self):
		troco = self.saldo
		saldo = 0
		estado = "INICIO"


def main():
	telefone = Telefone()

	# LEVANTAR
	telefone.levantar()  # maq: "Introduza moedas."

	# MOEDA 10c, 30c, 50c, 2e.
	telefone.moeda([10, 30, 50, 200])  # maq: "30c - moeda inválida; saldo = 2e60c"

	# T=601181818
	telefone.discar("601181818")  # maq: "Esse número não é permitido neste telefone. Queira discar novo número!"

	# T=253604470
	telefone.discar("253604470")  # maq: "saldo = 2e35c"

	# POUSAR
	telefone.pousar()  # maq: "troco=2e35c; Volte sempre!"


if __name__ == '__main__':
	main()
