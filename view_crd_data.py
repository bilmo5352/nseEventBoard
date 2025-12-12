"""
View Latest CRD (Credit Rating Database) Data
==============================================

Simple script to view the latest scraped CRD data.

Usage:
    python view_crd_data.py
"""

import json
import os
from datetime import datetime
from tabulate import tabulate


def load_latest_data():
    """Load the latest JSON data"""
    filepath = 'crd_data/latest.json'
    
    if not os.path.exists(filepath):
        print("❌ Error: No data found!")
        print(f"Expected file: {filepath}")
        print("\nPlease run the monitor first:")
        print("  python crd_monitor.py")
        return None
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    except Exception as e:
        print(f"❌ Error loading data: {e}")
        return None


def format_cell(value):
    """Format cell value for display"""
    if isinstance(value, dict):
        if 'text' in value:
            return value['text']
        return str(value)
    return str(value) if value else ''


def display_metadata(metadata):
    """Display metadata information"""
    print("\n" + "=" * 80)
    print("📊 NSE CRD (CREDIT RATING DATABASE) - LATEST DATA")
    print("=" * 80)
    
    try:
        timestamp = datetime.fromisoformat(metadata['scrape_timestamp'])
        time_str = timestamp.strftime("%B %d, %Y at %I:%M:%S %p")
    except:
        time_str = metadata['scrape_timestamp']
    
    print(f"\n⏰ Scraped: {time_str}")
    print(f"📈 Total Records: {metadata['total_records']}")
    print(f"📄 Total Pages: {metadata['total_pages']}")
    print(f"🔗 Source: {metadata['source_url']}")
    print()


def display_data_table(data, max_rows=None):
    """Display data in a formatted table"""
    if not data:
        print("No data to display")
        return
    
    headers = data[0].keys()
    
    table_data = []
    for i, row in enumerate(data):
        if max_rows and i >= max_rows:
            break
        
        row_data = [format_cell(row.get(h, '')) for h in headers]
        table_data.append(row_data)
    
    print(tabulate(table_data, headers=headers, tablefmt='grid', maxcolwidths=40))
    
    if max_rows and len(data) > max_rows:
        print(f"\n... showing {max_rows} of {len(data)} total records")


def filter_by_company(data, keyword):
    """Filter by company name"""
    filtered = []
    for record in data:
        company = record.get('COMPANY NAME', '')
        if isinstance(company, dict):
            company = company.get('text', '')
        if isinstance(company, str) and keyword.lower() in company.lower():
            filtered.append(record)
    return filtered


def filter_by_rating_agency(data, keyword):
    """Filter by rating agency"""
    filtered = []
    for record in data:
        agency = record.get('NAME OF CREDIT RATING AGENCY', '')
        if isinstance(agency, str) and keyword.lower() in agency.lower():
            filtered.append(record)
    return filtered


def filter_by_rating(data, rating):
    """Filter by credit rating"""
    filtered = []
    for record in data:
        credit_rating = record.get('CREDIT RATING', '')
        if isinstance(credit_rating, str) and rating.upper() in credit_rating.upper():
            filtered.append(record)
    return filtered


def get_statistics(data):
    """Get statistics from the data"""
    stats = {
        'total_records': len(data),
        'unique_companies': set(),
        'rating_agencies': {},
        'ratings': {},
        'rating_actions': {}
    }
    
    for record in data:
        # Company
        company = record.get('COMPANY NAME', '')
        if isinstance(company, dict):
            company = company.get('text', '')
        if company:
            stats['unique_companies'].add(company)
        
        # Rating Agency
        agency = record.get('NAME OF CREDIT RATING AGENCY', 'Unknown')
        stats['rating_agencies'][agency] = stats['rating_agencies'].get(agency, 0) + 1
        
        # Rating
        rating = record.get('CREDIT RATING', 'Unknown')
        stats['ratings'][rating] = stats['ratings'].get(rating, 0) + 1
        
        # Rating Action
        action = record.get('RATING ACTION', 'Unknown')
        stats['rating_actions'][action] = stats['rating_actions'].get(action, 0) + 1
    
    return stats


def display_statistics(stats):
    """Display statistics"""
    print("\n" + "=" * 80)
    print("📊 STATISTICS")
    print("=" * 80)
    
    print(f"\n🏢 Unique Companies: {len(stats['unique_companies'])}")
    print(f"📊 Total Records: {stats['total_records']}")
    
    print("\n📋 Top Rating Agencies:")
    sorted_agencies = sorted(stats['rating_agencies'].items(), key=lambda x: x[1], reverse=True)
    for agency, count in sorted_agencies[:10]:
        print(f"  {agency}: {count}")
    
    print("\n⭐ Top Credit Ratings:")
    sorted_ratings = sorted(stats['ratings'].items(), key=lambda x: x[1], reverse=True)
    for rating, count in sorted_ratings[:10]:
        print(f"  {rating}: {count}")
    
    print("\n🎯 Rating Actions:")
    sorted_actions = sorted(stats['rating_actions'].items(), key=lambda x: x[1], reverse=True)
    for action, count in sorted_actions:
        print(f"  {action}: {count}")


def interactive_menu(data_dict):
    """Interactive menu for viewing data"""
    while True:
        print("\n" + "=" * 80)
        print("📋 MENU")
        print("=" * 80)
        print("1. View All Records (first 20)")
        print("2. View All Records (complete)")
        print("3. Search by Company Name")
        print("4. Search by Rating Agency")
        print("5. Search by Credit Rating")
        print("6. View Statistics")
        print("7. Export to CSV")
        print("8. Show Metadata")
        print("0. Exit")
        print()
        
        choice = input("Enter your choice: ").strip()
        
        data = data_dict['data']
        metadata = data_dict['metadata']
        
        if choice == '1':
            print("\n" + "=" * 80)
            print("📊 FIRST 20 RECORDS")
            print("=" * 80)
            display_data_table(data, max_rows=20)
        
        elif choice == '2':
            print("\n" + "=" * 80)
            print("📊 ALL RECORDS")
            print("=" * 80)
            display_data_table(data)
        
        elif choice == '3':
            keyword = input("\nEnter company name: ").strip()
            filtered = filter_by_company(data, keyword)
            print(f"\nFound {len(filtered)} records for '{keyword}'")
            if filtered:
                display_data_table(filtered)
            else:
                print("❌ No records found")
        
        elif choice == '4':
            keyword = input("\nEnter rating agency name (e.g., CRISIL, ICRA): ").strip()
            filtered = filter_by_rating_agency(data, keyword)
            print(f"\nFound {len(filtered)} records for '{keyword}'")
            if filtered:
                display_data_table(filtered)
            else:
                print("❌ No records found")
        
        elif choice == '5':
            rating = input("\nEnter credit rating (e.g., AA, AAA): ").strip()
            filtered = filter_by_rating(data, rating)
            print(f"\nFound {len(filtered)} records with rating '{rating}'")
            if filtered:
                display_data_table(filtered)
            else:
                print("❌ No records found")
        
        elif choice == '6':
            stats = get_statistics(data)
            display_statistics(stats)
        
        elif choice == '7':
            try:
                import pandas as pd
                df = pd.DataFrame(data)
                # Flatten dict columns
                for col in df.columns:
                    if df[col].apply(lambda x: isinstance(x, dict)).any():
                        df[col] = df[col].apply(lambda x: x.get('text', x) if isinstance(x, dict) else x)
                
                filename = f"crd_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
                df.to_csv(filename, index=False, encoding='utf-8-sig')
                print(f"\n✅ Data exported to: {filename}")
            except ImportError:
                print("\n❌ Error: pandas not installed. Install it with: pip install pandas")
            except Exception as e:
                print(f"\n❌ Error exporting: {e}")
        
        elif choice == '8':
            display_metadata(metadata)
        
        elif choice == '0':
            print("\n👋 Goodbye!")
            break
        
        else:
            print("\n❌ Invalid choice. Please try again.")


def main():
    """Main function"""
    try:
        import tabulate as tab
    except ImportError:
        print("⚠️  Warning: 'tabulate' package not installed")
        print("For better formatting, install it with: pip install tabulate\n")
    
    print("Loading latest CRD data...")
    data_dict = load_latest_data()
    
    if not data_dict:
        return
    
    display_metadata(data_dict['metadata'])
    
    if not data_dict['data']:
        print("❌ No data found in the file")
        return
    
    print("=" * 80)
    print("📊 PREVIEW (First 10 Records)")
    print("=" * 80)
    try:
        display_data_table(data_dict['data'], max_rows=10)
    except Exception as e:
        print(f"Error displaying table: {e}")
        for i, record in enumerate(data_dict['data'][:10]):
            print(f"\nRecord {i+1}:")
            for key, value in record.items():
                print(f"  {key}: {format_cell(value)}")
    
    try:
        interactive_menu(data_dict)
    except KeyboardInterrupt:
        print("\n\n👋 Interrupted by user. Goodbye!")


if __name__ == "__main__":
    main()

