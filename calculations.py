# Множество дочерних узлов
def daughters_map(edges):
    maps = {}
    for i in edges:
        if i['source'] in maps:
            (maps.get(i['source'])).append(i['dest'])
            #maps.update( {i['source']:(maps.get(i['source'])).append(i['dest'])})
        else:
            maps.update({i['source']:[i['dest']]})
    print(f"cheeee ={maps}")
    return maps

