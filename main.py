from services.protocol_service import ProtocoloService
from utils.validators import validar_protocolo


def main():
    try:
        with open("protocolos.txt", "r", encoding="utf-8") as f:
            protocolos_brutos = [linha.strip() for linha in f if linha.strip()]
    except FileNotFoundError:
        print("❌ Arquivo 'protocolos.txt' não encontrado.")
        return

    if not protocolos_brutos:
        print("❌ Nenhum protocolo encontrado no arquivo.")
        return

    # Normaliza (com padding de zeros) antes de mandar pro serviço
    protocolos = []
    for numero in protocolos_brutos:
        try:
            protocolos.append(validar_protocolo(numero))
        except ValueError as e:
            print(f"⚠️  Ignorando protocolo inválido '{numero}': {e}")

    print(f"📋 {len(protocolos)} protocolos válidos para processar.\n")

    service = ProtocoloService()

    try:
        resultados = service.processar_lote(protocolos)
    except Exception as e:
        print(f"\n❌ Erro fatal durante o processamento: {e}")
        return

    # Resumo final
    print("\n" + "=" * 60)
    print("📊 RESUMO FINAL")
    print("=" * 60)
    sucessos = [r for r in resultados if "erro" not in r]
    falhas = [r for r in resultados if "erro" in r]

    print(f"✅ Sucessos: {len(sucessos)}")
    print(f"❌ Falhas:   {len(falhas)}")

    if falhas:
        print("\nProtocolos com erro:")
        for r in falhas:
            print(f"  - {r['numero_protocolo']}: {r['erro']}")


if __name__ == "__main__":
    main()