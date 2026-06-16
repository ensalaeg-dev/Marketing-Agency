import argparse
from crews.discovery_crew import DiscoveryCrew
from crews.content_crew import ContentCrew
from community_database.models import init_db
import os
from dotenv import load_dotenv

def main():
    load_dotenv()
    
    # Ensure DB is initialized
    db_url = os.getenv("DATABASE_URL", "sqlite:///community_database/growth_specialist.db")
    init_db(db_url)
    
    parser = argparse.ArgumentParser(description="Egyptian Omnichannel Community Growth Specialist CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available micro-crews")
    
    # Discovery Command
    discovery_parser = subparsers.add_parser("discover", help="Run the Discovery Crew to find new communities")
    discovery_parser.add_argument("--topic", type=str, required=True, help="Topic to search for (e.g., 'Real Estate', 'Wholesale Electronics')")
    discovery_parser.add_argument("--platform", type=str, required=True, help="Platform to focus on (e.g., 'Facebook Groups', 'WhatsApp')")
    
    # Content Command
    content_parser = subparsers.add_parser("generate", help="Run the Content Engine Crew to draft localized posts based on ERPNext campaigns")
    content_parser.add_argument("--governorate", type=str, required=True, help="Target governorate (e.g., 'Alexandria', 'Cairo')")
    content_parser.add_argument("--community_url", type=str, required=True, help="URL of the target community to draft the post for")
    
    args = parser.parse_args()
    
    if args.command == "discover":
        crew = DiscoveryCrew()
        result = crew.run(target_topic=args.topic, platform_focus=args.platform)
        print("\n=== Discovery Crew Finished ===")
        print(result)
        
    elif args.command == "generate":
        crew = ContentCrew()
        result = crew.run(governorate_focus=args.governorate, community_url=args.community_url)
        print("\n=== Content Crew Finished ===")
        print(result)
        
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
