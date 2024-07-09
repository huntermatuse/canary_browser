import argparse
import birdsong
import csv
from datetime import datetime, timedelta

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

    def download_tag_data(self, tag: str, start_date: datetime, end_date: datetime) -> list:
        with birdsong.CanaryView(host=self.canary_server, username=self.canary_username, password=self.canary_password) as view:
            data = list(view.getTagData(tags=tag, start=start_date, end=end_date))
            return [(item.timestamp, item.value) for item in data]

    def export_tag_list(self, filename: str):
        with birdsong.CanaryView(host=self.canary_server, username=self.canary_username, password=self.canary_password) as view:
            tags = list(view.browseTags(deep=True))
            with open(filename, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['Tag'])
                for tag in tags:
                    writer.writerow([tag])
        print(f"Tag list exported to {filename}")

def display_nodes(nodes):
    for idx, node in enumerate(nodes):
        print(f"[{idx}] {node}")
    print("\n[999] Exit")
    print("[998] Back One Node")
    print("[997] Start Over")

def export_to_csv(data, filename):
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Tag', 'Timestamp', 'Value'])  # Header
        for tag, values in data.items():
            for timestamp, value in values:
                writer.writerow([tag, timestamp, value])
    print(f"Data exported to {filename}")

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
        print("4. Download tag data")
        print("5. Export tag list")
        print("6. Download data for multiple tags")
        print("7. Exit")

        choice = input("Select an option: ")

        if choice == '1':
            nodes = browser.browse_node(path=current_path)
            while True:
                display_nodes(nodes)
                choice = input("Select an option: ")
                try:
                    choice = int(choice)
                    if choice == 999:
                        break
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
            tag = input("Enter the tag to download data for: ")
            date_range = input("Enter 'week' for last week's data, or 'custom' for a custom date range: ")

            if date_range.lower() == 'week':
                end_date = datetime.now()
                start_date = end_date - timedelta(days=7)
            elif date_range.lower() == 'custom':
                start_date = input("Enter start date (YYYY-MM-DD): ")
                end_date = input("Enter end date (YYYY-MM-DD): ")
                start_date = datetime.strptime(start_date, "%Y-%m-%d")
                end_date = datetime.strptime(end_date, "%Y-%m-%d")
            else:
                print("Invalid input. Please try again.")
                continue

            tag_data = browser.download_tag_data(tag=tag, start_date=start_date, end_date=end_date)
            filename = f"{tag.replace('.', '_')}_{start_date.date()}_{end_date.date()}.csv"
            export_to_csv({tag: tag_data}, filename)

        elif choice == '5':
            filename = input("Enter the filename to export the tag list (e.g., tag_list.csv): ")
            browser.export_tag_list(filename)

        elif choice == '6':
            tag_list_file = input("Enter the filename of the tag list CSV: ")
            date_range = input("Enter 'week' for last week's data, or 'custom' for a custom date range: ")

            if date_range.lower() == 'week':
                end_date = datetime.now()
                start_date = end_date - timedelta(days=7)
            elif date_range.lower() == 'custom':
                start_date = input("Enter start date (YYYY-MM-DD): ")
                end_date = input("Enter end date (YYYY-MM-DD): ")
                start_date = datetime.strptime(start_date, "%Y-%m-%d")
                end_date = datetime.strptime(end_date, "%Y-%m-%d")
            else:
                print("Invalid input. Please try again.")
                continue

            all_tag_data = {}
            with open(tag_list_file, 'r') as csvfile:
                reader = csv.reader(csvfile)
                next(reader)  # Skip header
                for row in reader:
                    tag = row[0]
                    print(f"Downloading data for tag: {tag}")
                    tag_data = browser.download_tag_data(tag=tag, start_date=start_date, end_date=end_date)
                    all_tag_data[tag] = tag_data

            filename = f"multi_tag_data_{start_date.date()}_{end_date.date()}.csv"
            export_to_csv(all_tag_data, filename)

        elif choice == '7':
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == '__main__':
    main()