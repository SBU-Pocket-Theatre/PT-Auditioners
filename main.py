import networkx as nx
import pygraphviz
import tkinter as tk
from tkinter import filedialog
from pathlib import Path
from platformdirs import user_data_dir

def run(role_list, data):
    # # This expects a CSV, with NO HEADER. The first column is a person's name, and each following column contains a SINGLE role.
    # data_path = Path(filedialog.askopenfilename(
    #     initialdir="/",
    #     title="Select CSV name and role data",
    #     filetypes=[("Casting Data", "*.csv")]
    # ))

    # f = open(data_path, encoding='utf-8-sig').readlines()

    # data = {}
    # for line in f:
    #     line_data = line.split(",")
    #     name = line_data[0]
    #     roles = line_data[1::1]
    #     data[line_data[0]] = [role.strip() for role in roles if role.strip() != ""]
    # role_list = ["Cat", "Horton", "Jojo", "Gertrude", "Mayzie", "Mr. Mayor", "General", "Sour Kangaroo", "Mrs. Mayor", "Wickershams", "Bird Girls", "Ensemble"]


    print(data)

    flipped_data = {}
    for k in data.keys():
        for r in data[k]:
            if (r not in flipped_data.keys()):
                flipped_data[r] = []
            flipped_data[r].append(k)

    print(flipped_data)
    print("Loaded data!")
    print("\n")
    print("Sanity check (counts per role):")
    for role in flipped_data.keys():
        print(f"{role}: {len(flipped_data[role])}")
    print("\n")
    print("Sanity check (counts per person):")
    for person in data.keys():
        print(f"{person}: {len(data[person])}")
    G = nx.Graph()
    nodelist = set()
    for role in flipped_data.keys(): # quick sanity check
        try:
            assert(role in role_list)
            nodelist.add(role)
            G.add_node(role)
        except:
            raise Exception(f"{role} not in role list")
    nodelist = list(nodelist)
    for person in data.keys():
        roles = data[person]
        for i in range(0, len(roles)):
            for j in range(i, len(roles)):
                G.add_edge(roles[i], roles[j])
            
    while(True):
        # clear graph coloring between runs
        for node in nodelist:
            G.add_node(node, color="#00a825", fontcolor="#00a825")
        pt_name = input("Enter PT member's name (or exit to end): ")
        if (pt_name.lower() == "exit"):
            break
        if (pt_name not in data.keys()):
            print("Invalid name, please try again")
            continue
        start_nodes = data[pt_name]
        print(f'{pt_name} is called back for {", ".join(start_nodes)}')
        conflicting_roles = set()
        # start nodes are ALWAYS conflicting
        for role in start_nodes:
            conflicting_roles.add(role)
        for start_node in start_nodes:
            target_nodes = nodelist.copy()
            target_nodes.remove(start_node)
            for target_node in target_nodes:
                if not nx.has_path(G, start_node, target_node):
                    target_nodes.remove(target_node)
            all_paths_to_target = list(nx.all_simple_edge_paths(G, source=start_node, target=target_nodes, cutoff=1))
            for path in all_paths_to_target:
                for edge in path:
                    G.add_node(edge[0], color="red", fontcolor="red")
                    G.add_node(edge[1], color="red", fontcolor="red")
                    conflicting_roles.add(edge[0])
                    conflicting_roles.add(edge[1])
        for start_node in start_nodes:
            G.add_node(start_node, color="#980000", fontcolor="#980000")

        print(f'{pt_name} CANNOT see the following roles: {", ".join(list(conflicting_roles))}')
        print(f'{pt_name} CAN see the following roles: {", ".join(list(set.difference(set(role_list), conflicting_roles)))}')
        see_reasoning = ""
        while (see_reasoning != "Y" and see_reasoning != "N"):
            see_reasoning = input("See reasoning? (Y/N): ")
            if (see_reasoning != "Y" and see_reasoning != "N"):
                print("Please respond with Y or N.")
        if (see_reasoning == "Y"):
            reasoning_dict = {role: [] for role in flipped_data.keys()}
            for role in data[pt_name]:
                reasoning_dict[role].append(f"{pt_name} cannot see {role} because they are called back for it.")
            for role in set.symmetric_difference(set(data[pt_name]), set(conflicting_roles)):
                reasoning = set()
                for pt_role in data[pt_name]:
                    reasoning = set.intersection(set(flipped_data[role]), set(flipped_data[pt_role]))
                    reasoning = list(reasoning)
                    if (len(reasoning) > 0):
                        reasoning_dict[role].append(f'{pt_name} cannot see {role} because {reasoning[0] if len(reasoning) == 1 else ", ".join(reasoning[0:-1:1]) + " and " + reasoning[-1]} {"is" if len(reasoning) == 1 else "are"} called back for {pt_role} (which {pt_name} is called back for) and {role}.')

            for key in reasoning_dict.keys():
                for r in reasoning_dict[key]:
                    print(r)

        save_graph = ""
        while (save_graph != "Y" and save_graph != "N"):
            save_graph = input("Save this graph? (Y/N): ")
            if (save_graph != "Y" and save_graph != "N"):
                print("Please respond with Y or N.")
        if (save_graph == "Y"):
            app_data_path = Path(user_data_dir("PTAuditioners", "MichaelBorczuk"))
            app_data_path.mkdir(parents=True, exist_ok=True)
            graph_path = app_data_path / f"{pt_name}.png"
            A = nx.nx_agraph.to_agraph(G)
            A.layout(prog='dot')
            A.draw(graph_path)
            print(f"Graph saved to {graph_path}")


        
