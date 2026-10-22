class RegexPatterns:
    # DADOS DO ATENDIMENTO
    DATA_SOLICITACAO = r'Data Solicitação:</b></font></td>\s*<td[^>]*>\s*([^<]+)\s*</td>'
    NUMERO_PROTOCOLO = r'Nº Protocolo:</b></font></td>\s*<td[^>]*>\s*([^<]+)\s*</td>'
    SOLICITACAO = r'(?<!Data )Solicitação:</b></font></td>\s*<td[^>]*>\s*([^<]+)\s*</td>'
    TIPO_SOLICITANTE = r'Tipo Solicitante:</b></font></td>\s*<td[^>]*>\s*([^<]+)\s*</td>'
    
    # DADOS DO SERVIDOR
    CPF_SERVIDOR = r'CPF Servidor:</b></font></td>\s*<td[^>]*>\s*([^<]+)\s*</td>'
    # O nome está dentro de uma tag <b> no HTML, então capturamos o conteúdo dela
    NOME_SERVIDOR = r'Nome:</b></font></td>\s*<td[^>]*>\s*<b>([^<]+)</b>'
    SEXO = r'Sexo:</b></font></td>\s*<td[^>]*>\s*([^<]+)\s*</td>'
    DATA_NASCIMENTO = r'Data Nascimento:</b></font></td>\s*<td[^>]*>\s*([^<]+)\s*</td>'
    # A matrícula está num input hidden, é mais seguro pegar o value dele
    MATRICULA = r'<input type="hidden" name="matriculaServidor" value="([^"]+)"'
    # A função tem um link (<a>) depois, então cortamos no <
    FUNCAO = r'Função:</b></font></td>\s*<td[^>]*>\s*([^<]+)'
    DATA_INGRESSO = r'Data Ingresso Serviço Público:</b></font></td>\s*<td[^>]*>\s*([^<]+)\s*</td>'
    DATA_OBITO = r'Data Óbito/Ausência[^<]*</b></font></td>\s*<td[^>]*>\s*<font[^>]*>\s*([^<]+)\s*</font>' 
    # ou, se não tiver a tag font no valor:
    # DATA_OBITO = r'Data Óbito/Ausência[^<]*</b></font></td>\s*<td[^>]*>\s*([^<]+)\s*</td>'
    
    PRAZO_RETROATIVO = r'Prazo para Pagamento Retroativo:</b></font></td>\s*<td[^>]*>\s*([^<]+)\s*</td>'