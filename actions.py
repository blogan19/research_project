represcribeActions = {
    0: [('represcribe','B-Action')],
    1: [('re-prescribe','B-Action')],
    2: [('ammend','B-Action')],
    3: [('review','B-Action')],
    4: [('alter', 'B-Action')],
    5: [('change','B-Action')]

}
discontinueActions= {
    0: [('discontinue','B-Action')],
    1: [('stop','B-Action')],
    2: [('delete','B-Action')],
    3: [('remove','B-Action')],
    4: [('suspend','B-Action')],
    5: [('temporarily','B-Action'),('suspend','L-Action')]
}
discontinueActionPastTense = {
    0: [('discontinued','B-Action')],
    1: [('stopped','B-Action')],
    2: [('deleted','B-Action')],
    3: [('removed','B-Action')],
    4: [('suspended','B-Action')],
    5: [('temporarily','B-Action'),('suspended','L-Action')]
}
startActions= {
    0: [('start','B-Action')],
    1: [('resume','B-Action')],
    2: [('prescribe','B-Action')],
    3: [('add','B-Action'),('a','I-Action'),('prescription','I-Action'),('for','o')],
    4: [('generate','B-Action'),('an','I-Action'),('order','L-Action')],
}
startPastTense = {
    0: [('started','B-Action')],
    1: [('prescribed','B-Action')],
    2: [('commenced','B-Action')]
}

reduction_actions = {
        0: [('re-prescribe','B-Action'),('at','I-Action'),('a','I-Action'),('lower','I-Action'),('dose','L-Action')],
        1: [('ammend','B-Action'),('dose','L-Action')],
        2: [('decrease','B-Action'),('dose','L-Action')],
        3: [('reduce','B-Action'),('dose','L-Action')],
        4: [('re-prescribe','B-Action')],
        5: [('represcribe','B-Action')],
        6: [('change','B-Action'),('dose','L-Action')],
        7: [('review','B-Action'),('need','I-Action'),('to','I-Action'),('ammend','I-Action'),('the','I-Action'),('dose','L-Action')],
        8: [('lower','B-Action'),('the','I-Action'),('dose','L-Action')],
        9: [('decrease','B-Action'),('the','I-Action'),('dose','L-Action')]
    }

increase_actions = {
        0: [('re-prescribe','B-Action'),('at','I-Action'),('a','I-Action'),('lower','I-Action'),('dose','L-Action')],
        1: [('ammend','B-Action'),('dose','L-Action')],
        2: [('increase','B-Action'),('dose','L-Action')],
        3: [('re-prescribe','B-Action')],
        4: [('represcribe','B-Action')],
        5: [('change','B-Action'),('dose','L-Action')],
        6: [('review','B-Action'),('need','I-Action'),('to','I-Action'),('ammend','I-Action'),('the','I-Action'),('dose','L-Action')],
        7: [('increase','B-Action'),('the','I-Action'),('dose','L-Action')]
    }