import tomllib  # Built-in from Python 3.11+
from pathlib import Path

def load_info_sources(file_path: str = "info_sources.toml"):
    with open(file_path, "rb") as f:
        return tomllib.load(f)

def display_data(config):
    print(f"Config Title: {config['title']}")
    print(f"Version: {config['version']}")
    print(f"Last Updated: {config['last_updated']}\n")
    
    subjects = config.get("subjects", {})
    for subject, details in subjects.items():
        print(f"Subject: {subject.capitalize()}")
        print(f"Description: {details.get('description')}")
        
        # Loop through each data type if present
        for data_type in ["youtube_channels", "rss_feeds", "websites", "podcasts"]:
            sources = details.get(data_type, [])
            if sources:
                print(f"\n  {data_type.replace('_', ' ').title()}:")
                for source in sources:
                    print(f"    - {source['name']} ({source['url']})")
                    # Print extra metadata if available
                    extra_info = {k: v for k, v in source.items() if k not in ['name', 'url']}
                    if extra_info:
                        for key, value in extra_info.items():
                            print(f"       {key}: {value}")
        print("\n" + "-" * 50 + "\n")

if __name__ == "__main__":
    config = load_info_sources()
    display_data(config)
