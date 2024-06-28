## Canary Browser CLI Tool

The Canary Browser CLI Tool is a command-line interface for interacting with a Canary server. It allows users to explore the tag structure, retrieve tag data, and search for tags within the node path. The tool provides a user-friendly way to navigate through nodes and perform various actions related to tag data management.

#### Features:

1. **Explore the Tag Structure**:
   - Navigate through nodes.
   - Display nodes with options to select, go back one node, or start over.
   - Retrieve and display tag data when the end of a path is reached.

2. **Get Tag Data**:
   - Directly search for and retrieve data for a specific tag.

3. **Search Tags**:
   - Search for tags within the node path using a search term.

4. **Navigation Options**:
   - Go back one node in the navigation history.
   - Start over from the root path.
   - Exit the tool.

#### Usage:

To use the tool, run the script with the necessary arguments:

```bash
python canary_browser_cli.py canary_server_address --username your_username --password your_password --path initial_path
```

Upon running, the tool will present an interactive menu with options to explore the tag structure, get tag data, search for tags, or exit. Navigate through nodes, retrieve tag data, or search for tags as needed.

