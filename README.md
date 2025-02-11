# API de Autômatos

## Configuração

1. Crie um ambiente virtual
2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Execute a API:
```bash
uvicorn main:app --reload
```

## Endpoints

- `POST /dfa/create`: Criar um Autômato Finito Determinístico (AFD)
- `POST /dfa/test-string`: Testar uma string em um AFD

## Exemplo de Uso

### Criar DFA
```json
{
  "states": ["q0", "q1"],
  "input_symbols": ["0", "1"],
  "transitions": {
    "q0": {"0": "q1", "1": "q0"},
    "q1": {"0": "q0", "1": "q1"}
  },
  "initial_state": "q0",
  "final_states": ["q1"]
}
```

### Testar String
Envie a mesma configuração do DFA junto com a string de teste.
