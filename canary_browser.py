import argparse
import birdsong

class Canary_Browser:
    def __init__(self, canary_server: str, canary_username: str = None, canary_password: str = None):
        self.canary_server = canary_server
        self.canary_username = canary_username
        self.canary_password = canary_password

    def browse_node(self, path: str = None) -> list:
        with birdsong.CanaryView(host=self.canary_server, username=self.canary_username, password=self.canary_password) as view:
            canary_nodes = list(view.browseNodes(path=path))
            return canary_nodes

    def get_tag(self, tag: str) -> list:
        with birdsong.CanaryView(host=self.canary_server, username=self.canary_username, password=self.canary_password) as view:
            return list(view.getTagData(tags=tag))

    def search_tags(self, search: str) -> list:
        with birdsong.CanaryView(host=self.canary_server, username=self.canary_username, password=self.canary_password) as view:
            return list(view.browseTags(search=search, deep=True))

def display_nodes(nodes):
    for idx, node in enumerate(nodes):
        print(f"[{idx}] {node}")
    print("\n[999] Exit")
    print("[998] Back One Node")
    print("[997] Start Over")

def main():
    parser = argparse.ArgumentParser(description='CLI tool for browsing Canary nodes')
    parser.add_argument('canary_server', type=str, help='Canary server address')
    parser.add_argument('--username', type=str, help='Canary username', default=None)
    parser.add_argument('--password', type=str, help='Canary password', default=None)
    parser.add_argument('--path', type=str, help='Path to browse', default=None)

    args = parser.parse_args()

    browser = Canary_Browser(canary_server=args.canary_server, canary_username=args.username, canary_password=args.password)
    current_path = args.path
    path_history = []

    while True:
        print("\nOptions:")
        print("1. Explore the tag structure")
        print("2. Get tag data")
        print("3. Search tags")
        print("4. Exit")

        choice = input("Select an option: ")

        if choice == '1':
            nodes = browser.browse_node(path=current_path)
            while True:
                display_nodes(nodes)
                choice = input("Select an option: ")
                try:
                    choice = int(choice)
                    if choice == 999:
                        return
                    elif choice == 998:  # Back one node
                        if path_history:
                            current_path = path_history.pop()
                            nodes = browser.browse_node(path=current_path)
                        else:
                            print("No previous node to go back to.")
                    elif choice == 997:  # Start over
                        current_path = None
                        path_history.clear()
                        nodes = browser.browse_node(path=current_path)
                    elif 0 <= choice < len(nodes):
                        selected_node = nodes[choice]
                        path_history.append(current_path)
                        if current_path:
                            current_path = f"{current_path}.{selected_node}"
                        else:
                            current_path = selected_node
                        nodes = browser.browse_node(path=current_path)
                        if not nodes:  # If no nodes are returned, get the tag data
                            tag_data = browser.get_tag(tag=current_path)
                            print(f"Tag data for {current_path}: {tag_data}")
                            break
                    else:
                        print("Invalid choice. Please try again.")
                except ValueError:
                    print("Invalid input. Please enter a number.")

        elif choice == '2':
            tag = input("Enter the tag to search for: ")
            tag_data = browser.get_tag(tag=tag)
            print(f"Tag data for {tag}: {tag_data}")

        elif choice == '3':
            search = input("Enter search term for tags: ")
            tags = browser.search_tags(search=search)
            print(f"Tags found for search '{search}': {tags}")

        elif choice == '4':
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == '__main__':
    main()