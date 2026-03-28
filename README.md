stateDiagram-v2
    [*] --> Init
    
    Init --> Bullish : ph_init 감지 + 첫 LRL 생성
    Init --> Bearish : pl_init 감지 + 첫 LRL 생성

    state Bullish {
        StateA_Bull --> StateB_Bull : cand_age >= 3
        StateB_Bull --> StateA_Bull : LRL 또는 HRL 돌파 확정
    }

    state Bearish {
        StateA_Bear --> StateB_Bear : cand_age >= 3
        StateB_Bear --> StateA_Bear : LRL 또는 HRL 돌파 확정
    }

    Bullish --> Bearish : HRL 터치 → Anchor 생성 → dir = -1
    Bearish --> Bullish : HRL 터치 → Anchor 생성 → dir = 1

    note right of Init : dir = 0
    note right of Bullish : dir = 1
    note right of Bearish : dir = -1
    note left of StateA_Bull : trigger_p == na
    note left of StateB_Bull : trigger_p != na
