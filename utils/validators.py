import re

def validar_protocolo(numero: str) -> str:
    """
    Valida e normaliza o número do protocolo.
    - Se o protocolo tiver menos de 10 dígitos, completa com zeros à esquerda.
    - Se tiver mais de 10, retorna erro (para não mascarar problemas).
    """
    if not numero or not numero.strip():
        raise ValueError("O número do protocolo não pode estar vazio.")
    
    # Remove espaços extras
    numero_limpo = numero.strip()
    
    # Verifica se contém apenas números
    if not numero_limpo.isdigit():
        raise ValueError("O protocolo deve conter apenas números.")
    
    # Se tem mais de 10, é erro (não deve ser truncado)
    if len(numero_limpo) > 10:
        raise ValueError(f"O protocolo '{numero_limpo}' tem {len(numero_limpo)} dígitos, mas o máximo permitido é 10.")
    
    # Completa com zeros à esquerda até 10 dígitos
    numero_padronizado = numero_limpo.zfill(10)
    
    if numero_padronizado != numero_limpo:
        print(f"ℹ️  Protocolo normalizado: '{numero_limpo}' → '{numero_padronizado}'")
    
    return numero_padronizado