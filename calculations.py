import sympy as sym
import copy


# Вернуть ключ по значению
def get_key(d, value):
    for k, v in d.items():
        for j in v:
            if j == value:
                return k


# Должен возвращать граф очищенный от фирм у которых отрицательный обьем
# (удалить  значение в  firms)
# Если в firms не осталось значений значит надо удалить вершину и и соеденить ее дочернюю и родительскую.
def CleaningNegativeVolume(graph, calculation):
    old_graph = copy.deepcopy(graph)
    old_calculation = copy.deepcopy(calculation)
    del_mass_map = []
    # поиск узлов и фирм с отрицательными обьемами
    for k in old_calculation:
        for i in reversed(range(len(old_calculation[k]["value"]))):
            if old_calculation[k]["value"][i] < 0:
                del_mass_map.append([k, i])
    # Удаление из глобального графа информации о фирмах с отрицательным объемом
    # Сохранение узлов без фирм
    reconstruction = []
    for elem in old_graph['nodes']:
        for x_mark in del_mass_map:
            if elem["name"] == x_mark[0]:
                elem["kwargs"]["firms"].pop(x_mark[1])
        if len(elem["kwargs"]["firms"]) < 1:
            reconstruction.append(elem["name"])

    # Если будет ошибка то наверное тут
    reconstruction = list(reversed(reconstruction))
    # Чтобы не трогать корневую вершины
    if 1 in reconstruction:
        reconstruction.remove(1)
    # Если нужно изенять структура(удалить одну вершины из рассмотерния)
    if reconstruction:
        # удаление пустой вершины и соединение с дочерей с родителями
        # (передача левел парйса родителю)
        for i in reconstruction:
            parent = -1
            child = []
            for edg in old_graph["edges"]:
                # Если наша вершина родитель
                if edg['source'] == i:
                    child.append(edg['dest'])
                    old_graph["edges"].remove(edg)
                elif edg['dest'] == i:
                    parent = edg['source']
                    old_graph["edges"].remove(edg)
            # Выстраивание связи
            if child:
                for ch in child:
                    old_graph["edges"].append({'source': parent, 'dest': ch, 'kwargs': {'width': 3}})
            # Удаление из основного графа вершины
            for nj in old_graph["nodes"]:
                if nj["name"] == i:
                    old_graph["nodes"].remove(nj)

            # Перенос цены за уровень (?????) кажется это ересь
            # low_level_node = None
            # for c in old_graph["nodes"]:
            #     if c["name"] == i:
            #         low_level_node = c
            # for c in old_graph["nodes"]:
            #     if c["name"] == parent:
            #         c['kwargs']["level_price"] = low_level_node['kwargs']["level_price"]
            # hiht_level_node
            # перенос долга
            # old_graph["edges"].append({parent:x})
    return old_graph


# Проверка на наличие отрицательных значений объемов
def isNegative(deci):
    for node in deci.values():
        if sum(1 for x in node["value"] if x < 0) > 0:
            return True
    return False


# Функция вставляющая новые значения в старую структуру (изначальную)
def OldButGold(old, new):
    skeleton = copy.deepcopy(old)
    for zero in skeleton.values():
        zero["profit"] = [0] * len(zero["value"])
        zero["value"] = [0] * len(zero["value"])
    for vice in new:
        for name in new[vice]["name_firm"]:
            skeleton_index = skeleton[vice]['name_firm'].index(name)
            new_index = new[vice]["name_firm"].index(name)
            skeleton[vice]["profit"][skeleton_index] = new[vice]["profit"][new_index]
            skeleton[vice]["value"][skeleton_index] = new[vice]["value"][new_index]
            skeleton[vice]["price"] = new[vice]["price"]
    return skeleton


def all_calculation_fun(graph):
    decision = CalculationForTheChain(graph)
    if isNegative(decision):
        print("отрицательные")
        pure_graph = CleaningNegativeVolume(graph, decision)
        new_decision = CalculationForTheChain(pure_graph)
        result = OldButGold(decision, new_decision)
        # return decision
        return result
    else:
        print("Нет отрицательные")
        return decision


def CalculationForTheChain(graph):
    cart_maps = daughters_map(graph["edges"])  # Связи
    stack = calculation_queue(cart_maps)  # очередь расчета
    cart_nodes = node_firm(graph["nodes"])  # ТАБЛИЦА ДАННЫЙ
    for nodes in stack:
        if nodes != 1:
            parent = get_key(cart_maps, nodes)
        else:
            parent = 1
        if nodes in cart_maps:
            cart_nodes[nodes]['price'] = price_function(cart_nodes, nodes, cart_maps)

        v1 = (volume_calculation(cart_nodes, nodes, parent, cart_maps))
        cart_nodes[nodes]['value'] = v1[0].args[0][:-1]
        cart_nodes[nodes]['profit'] = v1[1]

    revers_stack = stack[::-1]
    for new_result in revers_stack:
        q = sym.symbols(f"q{new_result}_1:{len(cart_nodes[new_result]['value']) + 1}")

        if new_result == 1:
            cart_nodes[new_result]['price'] = sum(cart_nodes[new_result]['value']) * -(
                cart_nodes[new_result]['price'][1]) + (cart_nodes[new_result]['price'][0])
            cart_nodes[new_result]['profit'] = [x.subs([(u, y) for u, y in zip(q, cart_nodes[new_result]['value'])]) for
                                                x in cart_nodes[new_result]['profit']]
        else:
            parent = get_key(cart_maps, new_result)
            p = sym.symbols(f'p{parent}')  # цена родителя
            cart_nodes[new_result]['value'] = [v.subs(p, cart_nodes[parent]['price']) for v in
                                               cart_nodes[new_result]['value']]

            cart_nodes[new_result]['price'] = sum(cart_nodes[new_result]['value']) * -(
                cart_nodes[new_result]['price'][1]) + (cart_nodes[new_result]['price'][0])

            cart_nodes[new_result]['profit'] = [
                x.subs([(u, y) for u, y in zip(q, cart_nodes[new_result]['value'])]).subs(p,
                                                                                          cart_nodes[parent]['price'])
                for
                x in cart_nodes[new_result]['profit']]

    return cart_nodes


# Функция расчет цены
def price_function(nf, name_node, maps):
    size_ = len(nf[name_node]['cost'])
    child_node = maps[name_node]
    q = sym.symbols(f'q{name_node}_1:{size_ + 1}')  # Объемы текущего узла для расчета цены
    value_child = [nf[x]['value'] for x in child_node]
    Q = sum(sum(i) for i in value_child)
    new_p = sym.solve(sum(q) - Q, f'p{name_node}')
    A = new_p[0].subs([(i, 0) for i in q])
    B = -((new_p[0].subs([(i, 1) for i in q]) - A) / size_)  # ТУТ ПОКА ПРОБЛЕМА СО ЗНАКОМ(УЖЕ НЕТ)
    return [A, B]


# Расчет обьемов (и прибыли)
def volume_calculation(nf, name_node, parent, cart_maps):
    size_ = len(nf[name_node]['cost'])
    q = sym.symbols(f'q{name_node}_1:{size_ + 1}')  # обьем
    p = sym.symbols(f'p{parent}')  # цена родителя
    c = nf[name_node]['cost']
    e = nf[name_node]['price']  # функция цены текущего узла
    switch = {
        1: [q[i] * (e[0] - e[1] * sum(q) - c[i]) for i in range(size_)],  # прибыль корневого уровня
        2: [q[i] * (e[0] - e[1] * sum(q) - p - c[i]) for i in range(size_)],  # прибыль промежуточного уровня
        3: [q[i] * ((e[0] - e[1] * sum(q)) - p - c[i]) for i in range(size_)]  # прибыль терминального уровня
    }
    P = switch.get(type_node(name_node, cart_maps))
    Pi = [sym.diff(P[i], q[i]) for i in range(size_)]
    return [sym.linsolve([*Pi], (*q, p)), P]


# проверить тип узла
def type_node(name, cart_maps):
    if name == 1:
        return 1  # корневая
    elif name in cart_maps:
        return 2  # промежуточная
    else:
        return 3  # терминальная


# Очередь расчета вершин
def calculation_queue(map1):
    stack = []
    for i in map1:
        if i not in stack:
            stack.insert(0, i)
            for x in map1.get(i):
                stack.insert(0, x)
        else:
            for q in map1.get(i):
                if q not in stack:
                    stack.insert(0, q)
    return stack


# Множество дочерних узлов
def daughters_map(edges):
    maps = {}
    for i in edges:
        if i['source'] in maps:
            (maps.get(i['source'])).append(i['dest'])
        else:
            maps.update({i['source']: [i['dest']]})
    return maps


# вся информация будет храниться тут
def node_firm(nodes):
    data = {}
    for i in nodes:
        data.update({i['name']:
            {
                'cost': [c['cost_firm'] for c in i['kwargs']['firms']],
                'price': i['kwargs']['level_price'],  # пускай будет массив из 2х значений А и Б тк p = a - b*SUM(value)
                'profit': [],
                'value': [],
                'name_firm': [c['name_firm'] for c in i['kwargs']['firms']],
            }
        })
    return data
