# Flappy

Este é um clone simples de Flappy Bird feito em *python3* através da biblioteca *pygame*.

Contribuidores: [Ítalo](https://github.com/italodoarbusto) e [YohananDiamond](https://github.com/YohananDiamond)

## Rodando o código

Esse clone atualmente não tem um método de instalação formado, por isso a maneira recomendada é rodar o arquivo `src/main.py`.

Primeiro, antes de tudo, é necessário instalar o pygame, geralmente através do pip.

```bash
pip install pygame
```

Depois disso, basta clonar o repositório e rodar o arquivo `main.py`, localizado na pasta `src`.
```bash
git clone https://github.com/italodoarbusto/Flappy
cd Flappy
cd src
./main.py
```

<!-- ## Convenções Locais de Código

### 1. Sets para situações de `if x in {...}`

Neste projeto, o seguinte bloco é muito mais usado:

```python
if 'foo' in {'foo', 'bar', 'baz'}: ...
```

Do que um dos seguintes:

```python
if 'foo' in ('foo', 'bar', 'baz'): ...
if 'foo' in ['foo', 'bar', 'baz']: ...
```

Foi decidido fazer isso por causa desse texto [desta página](https://wiki.python.org/moin/PythonSpeed):

> Membership testing with sets and dictionaries is much faster, O(1), than searching sequences, O(n). When testing "a in b", b should be a set or dictionary instead of a list or tuple.  -->
