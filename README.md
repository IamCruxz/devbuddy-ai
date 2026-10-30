# DevBuddy AI

Assistente de estudos de programação em Python, feito para ajudar iniciantes a entender código, aprender conceitos e resolver erros.

> Projeto em desenvolvimento inicial, feito por um estudante como projeto de aprendizado.

## O que já funciona

Uma interface de linha de comando em que você cola um trecho de código e recebe uma explicação em português, escrita para iniciantes. O programa foi instruído a:

- explicar o que o código faz, passo a passo;
- explicar o raciocínio, e não só o resultado;
- apontar erros com gentileza e dar uma dica antes da solução;
- separar o que é certo do que é suposição.

O programa **não executa** o código que você cola. Ele apenas o envia ao modelo para ser explicado.

## O que ainda não existe

Estas funcionalidades estão apenas planejadas:

- explicação de conceitos com exemplos;
- geração de exercícios com níveis de dificuldade;
- histórico de conversas;
- testes automatizados;
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

## Limitações conhecidas

- **Plano gratuito:** usa o plano gratuito da API do Gemini, que tem limites de uso e pode responder com erro 503 (modelo sobrecarregado) em horários de muita demanda. Ainda não há retentativa automática nem modelo reserva.
- **Nome do modelo:** o modelo usado está na constante `MODELO` em `devbuddy.py`. Os nomes mudam com frequência, e pode ser preciso atualizá-lo.
- **Somente IPv4:** o código força conexões por IPv4, porque na rede do autor o IPv6 não funcionava. Em uma rede só com IPv6, isso pode impedir a conexão.
- **Pouco testado:** foi testado manualmente, em Windows com Python 3.14, com poucos exemplos. A qualidade das explicações ainda não foi avaliada de forma sistemática.
- **Respostas de IA podem errar:** confira as explicações antes de confiar nelas.

## Privacidade

O código que você cola é enviado à API do Google. **Não cole senhas, chaves de API, dados pessoais nem código privado.** Em planos gratuitos, o provedor pode usar o conteúdo enviado para melhorar seus produtos.

## Autor

Felipe Rodrigues Cruz, estudante de Engenharia de Software na UTFPR.