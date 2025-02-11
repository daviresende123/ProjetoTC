from fastapi import FastAPI, HTTPException
from automata.fa.dfa import DFA
from automata.pda.dpda import DPDA
from automata.tm.dtm import DTM
from pydantic import BaseModel
from typing import Dict, Set, Literal, Optional, Union
import uuid
from fastapi.responses import Response

app = FastAPI(title="Autômatos API")

# Dicionário para armazenar os autômatos criados
automatos_storage = {}

class AFDConfig(BaseModel):  # Renomeado de DFAConfig
    states: set[str]
    input_symbols: set[str]
    transitions: dict
    initial_state: str
    final_states: set[str]

class AFPConfig(BaseModel):  # Renomeado de PDAConfig
    states: Set[str]
    input_symbols: Set[str]
    stack_symbols: Set[str]
    transitions: Dict[str, Dict[str, Dict[str, tuple[str, str]]]]
    initial_state: str
    initial_stack_symbol: str
    final_states: Set[str]

class MTConfig(BaseModel):  # Renomeado de TMConfig
    states: Set[str]
    input_symbols: Set[str]
    tape_symbols: Set[str]
    transitions: Dict[str, Dict[str, tuple[str, str, Literal["L", "R", "N"]]]]
    initial_state: str
    final_states: Set[str]
    blank_symbol: str

def create_dot_string(automaton_type: str, config: Union[AFDConfig, AFPConfig, MTConfig]) -> str:
    dot_str = ['digraph {']
    
    # Configurações gerais do grafo
    dot_str.append('rankdir=LR;')
    dot_str.append('node [shape=circle];')
    
    # Adiciona estados
    for state in config.states:
        if state in config.final_states:
            dot_str.append(f'"{state}" [shape=doublecircle];')
        else:
            dot_str.append(f'"{state}" [shape=circle];')
    
    # Estado inicial
    dot_str.append(f'__start0 [label="", shape=none];')
    dot_str.append(f'__start0 -> "{config.initial_state}";')
    
    # Adiciona transições
    if automaton_type == "afd":
        for state, transitions in config.transitions.items():
            for symbol, next_state in transitions.items():
                dot_str.append(f'"{state}" -> "{next_state}" [label="{symbol}"];')
    elif automaton_type == "afp":
        for state, symbols in config.transitions.items():
            for input_symbol, stack_symbols in symbols.items():
                for stack_symbol, (next_state, push_symbol) in stack_symbols.items():
                    label = f"{input_symbol},{stack_symbol}/{push_symbol}"
                    dot_str.append(f'"{state}" -> "{next_state}" [label="{label}"];')
    elif automaton_type == "mt":
        for state, transitions in config.transitions.items():
            for symbol, (next_state, write_symbol, direction) in transitions.items():
                label = f"{symbol}/{write_symbol},{direction}"
                dot_str.append(f'"{state}" -> "{next_state}" [label="{label}"];')
    
    dot_str.append('}')
    return '\n'.join(dot_str)

@app.post("/afd/create")  # Renomeado de dfa
def create_afd(config: AFDConfig):
    try:
        afd = DFA(
            states=config.states,
            input_symbols=config.input_symbols,
            transitions=config.transitions,
            initial_state=config.initial_state,
            final_states=config.final_states
        )
        automato_id = str(uuid.uuid4())
        automatos_storage[automato_id] = {
            "type": "afd",
            "config": config,
            "automato": afd
        }
        return {"message": "AFD criado com sucesso", "automato_id": automato_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/afd/visualize")  # Renomeado de dfa
def visualize_afd(config: AFDConfig):
    try:
        dot_string = create_dot_string("afd", config)
        return Response(content=dot_string, media_type="text/plain")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/afd/test-string")  # Renomeado de dfa
def test_afd_string(config: AFDConfig, test_string: str):
    try:
        afd = DFA(
            states=config.states,
            input_symbols=config.input_symbols,
            transitions=config.transitions,
            initial_state=config.initial_state,
            final_states=config.final_states
        )
        is_accepted = afd.accepts_input(test_string)
        return {"string": test_string, "accepted": is_accepted}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/afp/create")  # Renomeado de pda
def create_afp(config: AFPConfig):
    try:
        afp = DPDA(
            states=config.states,
            input_symbols=config.input_symbols,
            stack_symbols=config.stack_symbols,
            transitions=config.transitions,
            initial_state=config.initial_state,
            initial_stack_symbol=config.initial_stack_symbol,
            final_states=config.final_states
        )
        automato_id = str(uuid.uuid4())
        automatos_storage[automato_id] = {
            "type": "afp",
            "config": config,
            "automato": afp
        }
        return {"message": "AFP criado com sucesso", "automato_id": automato_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/afp/visualize")  # Renomeado de pda
def visualize_afp(config: AFPConfig):
    try:
        dot_string = create_dot_string("afp", config)
        return Response(content=dot_string, media_type="text/plain")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/afp/test-string")  # Renomeado de pda
def test_afp_string(config: AFPConfig, test_string: str):
    try:
        afp = DPDA(
            states=config.states,
            input_symbols=config.input_symbols,
            stack_symbols=config.stack_symbols,
            transitions=config.transitions,
            initial_state=config.initial_state,
            initial_stack_symbol=config.initial_stack_symbol,
            final_states=config.final_states
        )
        is_accepted = afp.accepts_input(test_string)
        return {"string": test_string, "accepted": is_accepted}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/mt/create")  # Renomeado de tm
def create_mt(config: MTConfig):
    try:
        mt = DTM(
            states=config.states,
            input_symbols=config.input_symbols,
            tape_symbols=config.tape_symbols,
            transitions=config.transitions,
            initial_state=config.initial_state,
            final_states=config.final_states,
            blank_symbol=config.blank_symbol
        )
        automato_id = str(uuid.uuid4())
        automatos_storage[automato_id] = {
            "type": "mt",
            "config": config,
            "automato": mt
        }
        return {"message": "MT criada com sucesso", "automato_id": automato_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/mt/visualize")  # Renomeado de tm
def visualize_mt(config: MTConfig):
    try:
        dot_string = create_dot_string("mt", config)
        return Response(content=dot_string, media_type="text/plain")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/mt/run")  # Renomeado de tm
def run_mt(config: MTConfig, input_string: str):
    try:
        mt = DTM(
            states=config.states,
            input_symbols=config.input_symbols,
            tape_symbols=config.tape_symbols,
            transitions=config.transitions,
            initial_state=config.initial_state,
            final_states=config.final_states,
            blank_symbol=config.blank_symbol
        )
        result = mt.run_input(input_string)
        return {"input": input_string, "result": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Novo endpoint para recuperar informações do autômato
@app.get("/automato/{automato_id}")
def get_automato_info(automato_id: str):
    if automato_id not in automatos_storage:
        raise HTTPException(status_code=404, detail="Autômato não encontrado")
    
    automato_data = automatos_storage[automato_id]
    config = automato_data["config"]
    
    return {
        "type": automato_data["type"],
        "states": list(config.states),
        "input_symbols": list(config.input_symbols),
        "transitions": config.transitions,
        "initial_state": config.initial_state,
        "final_states": list(config.final_states),
        "additional_info": {
            "stack_symbols": list(config.stack_symbols) if hasattr(config, "stack_symbols") else None,
            "initial_stack_symbol": config.initial_stack_symbol if hasattr(config, "initial_stack_symbol") else None,
            "tape_symbols": list(config.tape_symbols) if hasattr(config, "tape_symbols") else None,
            "blank_symbol": config.blank_symbol if hasattr(config, "blank_symbol") else None
        }
    }