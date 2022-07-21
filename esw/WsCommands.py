from dataclasses import dataclass

from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class QueryFinal:
    runId: str
    timeout: int
    _type: str = 'QueryFinal'


@dataclass_json
@dataclass
class SubscribeSequencerState:
    _type: str = 'SubscribeSequencerState'
