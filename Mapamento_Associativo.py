import collections

class CacheAssociativo:
    def __init__(self, tamanho_cache, politica):
        self.tamanho_cache = tamanho_cache
        self.politica = politica
        self.cache = collections.OrderedDict()  # Cache como dicionário ordenado
        self.frequencia = {}  # Para rastrear a frequência no LFU

    def verificar_cache(self, endereco):
        if endereco in self.cache:
            print(f"Cache Hit: {endereco} encontrado.")
            if self.politica == 'LRU':
                # Move para o final para indicar uso recente
                self.cache.move_to_end(endereco)
            if self.politica == 'LFU':
                self.frequencia[endereco] += 1
            return True
        else:
            print(f"Cache Miss: {endereco} não encontrado.")
            self.atualizar_cache(endereco)
            return False

    def atualizar_cache(self, endereco):
        if len(self.cache) >= self.tamanho_cache:
            self.substituir_cache()
        self.cache[endereco] = f"Dado_{endereco}"
        if self.politica == 'LFU':
            self.frequencia[endereco] = 1

    def substituir_cache(self):
        if self.politica == 'LRU' or self.politica == 'FIFO':
            # Remove o primeiro item (FIFO e LRU)
            endereco_removido, _ = self.cache.popitem(last=False)
        elif self.politica == 'LFU':
            # Remove o item com a menor frequência
            endereco_removido = min(self.frequencia, key=self.frequencia.get)
            del self.cache[endereco_removido]
            del self.frequencia[endereco_removido]

        print(f"Substituindo: {endereco_removido} removido do cache.")

    def exibir_cache(self):
        print("Estado atual do cache:")
        for endereco, dado in self.cache.items():
            print(f"{endereco}: {dado}")


def main():
    print("Políticas disponíveis: LRU, LFU, FIFO")
    politica = input("Escolha a política de substituição: ").strip().upper()

    if politica not in ['LRU', 'LFU', 'FIFO']:
        print("Política inválida. Escolha entre LRU, LFU ou FIFO.")
        return

    tamanho_cache = int(input("Informe o tamanho do cache: "))
    cache = CacheAssociativo(tamanho_cache, politica)

    while True:
        endereco = input("Digite o endereço de memória (ou 'sair' para encerrar): ").strip()
        if endereco.lower() == 'sair':
            break
        cache.verificar_cache(endereco)
        cache.exibir_cache()

if __name__ == '__main__':
    main()
