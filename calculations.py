import sympy as sym


def all_calculation_fun(graph):
    end1 = [5000, 0.25]
    end2 = [6000, 0.19]

    cart_maps = daughters_map(graph["edges"])
    print(f'cart_maps={cart_maps}')

    stack = calculation_queue(cart_maps)
    print(f'stack={stack}')

    cart_nodes = node_firm(graph["nodes"])
    print(f'cart_nodes={cart_nodes}')

    volume_calculation(cart_nodes, 2, 1,cart_maps)




# ЖОПИСАТЬ ФУНКЦИЮ А ЕЩЕ СДЕЛАТЬ ДОБАВЛЕНИЕ А И Б ДЛЯ ТЕРМИНАЛЬНЫХ УЗЛОВ
def volume_calculation(nf, name_node, parent,cart_maps):
    size_ = len(nf[name_node]['cost'])
    print(f"size = {size_}")
    q = sym.symbols(f'q{name_node}_1:{size_ + 1}')  # обьес
    p = sym.symbols(f'p{parent}')  # цена родителя
    print(f'p = {p}')
    print(f'q = {q}')

    c = nf[name_node]['cost']
    e = nf[name_node]['price'] # функция цены текущего ущла
    print(f'c= {c}')
    print(f'e = {e}')

    switch = {
        1: [q[i] * (e[0] - e[1] * sum(q) - c[i]) for i in range(size_)], # прибыль корневого уровня
        2: [q[i] * (e[0] - e[1] * sum(q) - p - c[i]) for i in range(size_)],# прибыль промежуточного уровня
        3: [q[i] * ((e[0] - e[1] * sum(q))-p-c[i]) for i in range(size_)]# прибыль терминального уровня
    }

    P = switch.get(type_node(name_node, cart_maps))
    Pi = [sym.diff(P[i], q[i]) for i in range(size_)]
    symiy = sym.linsolve([*Pi], (*q,p))
    print(f'symiy = {symiy}')
    return symiy


# проверить тип узла
def type_node(name, cart_maps):
    if name == 1:
        return 1  # корневая
    elif name in cart_maps:
        return 2  # промежуточная
    else:
        return 3  # терминальная


# Очеред расчета вершин
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
            # maps.update( {i['source']:(maps.get(i['source'])).append(i['dest'])})
        else:
            maps.update({i['source']: [i['dest']]})
    return maps


# вся информация будет храниться тут
def node_firm(nodes):
    data = {}
    for i in nodes:
        # cost.update({i['name']: [c['cost_firm'] for c in i['kwargs']['firms']]})
        data.update({i['name']:
            {
                'cost': [c['cost_firm'] for c in i['kwargs']['firms']],
                'price': i['kwargs']['level_price'],  # пускай будет массив из 2х значений А и Б тк p = a - b*SUM(value)
                'profit': [],
                'value': []
            }
        })
    return data
