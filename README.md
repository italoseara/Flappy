# Flappy

Um repositório contendo um clone de Flappy Bird feito usando pygame.

```bash
pip install pygame
```

## Convenções Locais de Código

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

> Membership testing with sets and dictionaries is much faster, O(1), than searching sequences, O(n). When testing "a in b", b should be a set or dictionary instead of a list or tuple. 
