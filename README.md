# DevBuddy AI

Assistente de estudos de programação em Python, feito para ajudar iniciantes a entender código, aprender conceitos e resolver erros.

> Projeto em desenvolvimento inicial, feito por um estudante como projeto de aprendizado.

## O que já funciona

Uma interface de linha de comando em que você cola um trecho de código e recebe uma explicação em português, escrita para iniciantes. O programa foi instruído a:

- explicar o que o código faz, passo a passo, e o raciocínio por trás;
- simular a execução e dizer o que seria exibido, inclusive antes de um erro;
- dizer o nome exato do erro, como aparece no terminal;
- dar dicas em forma de pergunta, sem escrever a correção, a não ser que você peça;
- separar o que é certo do que é suposição.

O programa **não executa** o código que você cola. Ele apenas o envia ao modelo para ser explicado.

### Retentativas e modelo reserva

As chamadas à API passam por um pequeno módulo (`chamadas.py`) que:

- tenta de novo, com espera crescente e aleatória, nos erros temporários (429, 500, 502, 503, 504, 529) e em falhas de rede;
- passa para o próximo modelo da lista quando as tentativas de um modelo acabam, ou quando um modelo não é encontrado (404);
- não tenta de novo nos erros 400, 401 e 403, porque repetir não resolve;
- registra no terminal qual modelo respondeu, sem registrar a chave nem o código enviado.

A lista de modelos fica em `MODELOS`, no início de `chamadas.py`.

## O que ainda não existe

Estas funcionalidades estão apenas planejadas:

- explicação de conceitos com exemplos;
- geração de exercícios com níveis de dificuldade;
- histórico de conversas;
- avaliação sistemática da qualidade das explicações;
- interface gráfica ou web.

## Como instalar e rodar (Windows)

Pré-requisitos: Python 3 e Git instalados, e uma chave de API do Google Gemini (gratuita, em https://aistudio.google.com).

```powershell
git clone https://github.com/IamCruxz/devbuddy-ai.git
cd devbuddy-ai
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Depois, crie na pasta do projeto um arquivo chamado `.env` com este conteúdo, trocando pelo valor da sua chave:

```
GEMINI_API_KEY=sua_chave_aqui
```

O arquivo `.env` está no `.gitignore` e **nunca deve ser enviado ao GitHub**.

Para rodar:

```powershell
python devbuddy.py
```

Cole o código, digite `FIM` em uma linha nova e aperte Enter. A explicação gerada varia a cada execução.

## Testes

```powershell
pip install -r requirements-dev.txt
python -m pytest -v
```

Os testes cobrem **apenas** a lógica de retentativas e de modelo reserva (`chamadas.py`), usando erros simulados: nenhuma chamada real é feita à API. Eles **não** avaliam a qualidade das explicações do tutor.

## Limitações conhecidas

- **Plano gratuito:** usa o plano gratuito da API do Gemini, que tem limites de uso e pode responder com erro 503 em horários de muita demanda. Nesse caso o programa tenta de novo e usa o modelo reserva, mas pode ainda assim falhar.
- **Retentativas só testadas com erros simulados:** não foi verificado como o SDK se comporta em todas as falhas reais, em especial nas falhas de rede. O cabeçalho `retry-after` do servidor ainda não é respeitado.
- **Tempo de espera:** em uma falha de rede prolongada, o programa pode levar vários minutos para desistir.
- **Nomes de modelos mudam:** se um modelo da lista deixar de existir, o programa pula para o próximo, mas a lista precisa ser atualizada de vez em quando.
- **Somente IPv4:** o código força conexões por IPv4, porque na rede do autor o IPv6 não funcionava. Em uma rede só com IPv6, isso pode impedir a conexão.
- **Pouco testado manualmente:** a qualidade das explicações foi observada em poucos exemplos, em Windows com Python 3.14.
- **Respostas de IA podem errar:** confira as explicações antes de confiar nelas.

## Privacidade

O código que você cola é enviado à API do Google. **Não cole senhas, chaves de API, dados pessoais nem código privado.** Em planos gratuitos, o provedor pode usar o conteúdo enviado para melhorar seus produtos.

## Autor

Felipe Rodrigues Cruz, estudante de Engenharia de Software na UTFPR.