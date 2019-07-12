# Kart Racing Challenge

> Repositório com a solução do desafio da corrida de Kart, que está descrito no [README.md](https://github.com/pedrox-hs/kart-racing-challenge/blob/master/README.md).

## Requisitos
* Python >= 3.4 (_opcional se possuir o Docker_)

_Foi testando apenas usando sistema operacional Linux_

## Instalação

### Clone

- Clone esse repositório para sua máquina local usando `https://github.com/pedrox-hs/kart-racing-challenge.git`

### Online

Se preferir é possível ver o resultado pelo link [https://www.onlinegdb.com/HkJusUIZH](https://www.onlinegdb.com/HkJusUIZH)

## Utilização

Acesse o diretório raíz do repositório

`$ cd kart-racing-challenge`

### Passando o caminho do arquivo de log por argumento

`$ python3 -m py3.src.read_log logs/kart-racing.log`

com Docker:

`$ docker run -v $(pwd):/app -w /app --rm python:3-alpine python3 -m py3.src.read_log logs/kart-racing.log`

[![asciicast demo](https://raw.githubusercontent.com/pedrox-hs/kart-racing-challenge/master/demo/demo.gif)](https://asciinema.org/a/257122)


### Utilizando a entrada padrão (stdin)

`$ cat logs/kart-racing.log | python3 -m py3.src.read_log`

com Docker:

`$ cat logs/kart-racing.log | docker run -v $(pwd):/app -w /app --rm -i python:3-alpine python3 -m py3.src.read_log`

[![asciicast demo stdin](https://raw.githubusercontent.com/pedrox-hs/kart-racing-challenge/master/demo/stdin.gif)](https://asciinema.org/a/257124)


## Testes

Para rodar os testes unitários use o seguinte comando:

`$ python3 -m py3.tests.read_log_test`

com Docker:

`$ docker run -v $(pwd):/app -w /app --rm -i python:3-alpine python3 -m py3.tests.read_log_test`

[![asciicast testing demo](https://raw.githubusercontent.com/pedrox-hs/kart-racing-challenge/master/demo/testing.gif)](https://asciinema.org/a/257129)
