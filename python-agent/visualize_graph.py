#!/usr/bin/env python3
"""Visualize the Narcissus LangGraph workflow."""

from src.narcissus.agent import create_agent


def main():
    """Generate and display the graph visualization."""
    agent = create_agent()

    # Generate the graph visualization
    print("Generating LangGraph visualization...")

    try:
        # This will generate a PNG image of the graph
        img = agent.get_graph().draw_mermaid_png()

        # Save to file
        with open("narcissus_graph.png", "wb") as f:
            f.write(img)

        print("Graph saved as 'narcissus_graph.png'")

    except Exception as e:
        print(f"Error generating PNG: {e}")
        print("Trying ASCII representation instead...")

        # Fallback to text representation
        try:
            print("\nGraph structure:")
            print(agent.get_graph().draw_ascii())
        except Exception as ascii_e:
            print(f"Error generating ASCII: {ascii_e}")

            # Final fallback - just print the graph info
            print("\nGraph nodes and edges:")
            graph = agent.get_graph()
            print(f"Nodes: {list(graph.nodes.keys())}")
            print("Edges:")
            for node, edges in graph.edges.items():
                for edge in edges:
                    print(f"  {node} -> {edge}")


if __name__ == "__main__":
    main()
