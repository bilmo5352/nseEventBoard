"""
View Latest Credit Rating Regulation 30 Data
=============================================

Simple script to view the latest scraped credit rating data.

Usage:
    python view_credit_rating_data.py
"""

import json
import os
import glob
from datetime import datetime
from tabulate import tabulate


def list_available_files():
    """List all available JSON files"""
    files = glob.glob('credit_rating_data/latest_*.json')
    return sorted(files)


def load_data(filepath):
    """Load JSON data from file"""
    if not os.path.exists(filepath):
        print(f"❌ Error: File not found: {filepath}")
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
    print("⭐ NSE CREDIT RATING REGULATION 30 - LATEST DATA")
    print("=" * 80)
    
    try:
        timestamp = datetime.fromisoformat(metadata['scrape_timestamp'])
        time_str = timestamp.strftime("%B %d, %Y at %I:%M:%S %p")
    except:
        time_str = metadata['scrape_timestamp']
    
    print(f"\n⏰ Scraped: {time_str}")
    print(f"📊 Market Type: {metadata.get('market_type', 'N/A')}")
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
    
    print(tabulate(table_data, headers=headers, tablefmt='grid', maxcolwidths=30))
    
    if max_rows and len(data) > max_rows:
        print(f"\n... showing {max_rows} of {len(data)} total records")


def filter_by_company(data, keyword):
    """Filter by company name or symbol"""
    filtered = []
    for record in data:
        company = record.get('COMPANY NAME', '')
        symbol = record.get('SYMBOL', '')
        
        if isinstance(symbol, dict):
            symbol = symbol.get('text', '')
        
        if (isinstance(company, str) and keyword.lower() in company.lower()) or \
           (isinstance(symbol, str) and keyword.lower() in symbol.lower()):
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


def filter_by_action(data, action):
    """Filter by current action"""
    filtered = []
    for record in data:
        current_action = record.get('CURRENT ACTION', '')
        if isinstance(current_action, str) and action.lower() in current_action.lower():
            filtered.append(record)
    return filtered


def get_statistics(data):
    """Get statistics from the data"""
    stats = {
        'total_records': len(data),
        'unique_companies': set(),
        'ratings': {},
        'actions': {},
        'rating_types': {}
    }
    
    for record in data:
        # Company
        company = record.get('COMPANY NAME', '')
        if company:
            stats['unique_companies'].add(company)
        
        # Rating
        rating = record.get('CREDIT RATING', 'Unknown')
        stats['ratings'][rating] = stats['ratings'].get(rating, 0) + 1
        
        # Action
        action = record.get('CURRENT ACTION', 'Unknown')
        stats['actions'][action] = stats['actions'].get(action, 0) + 1
        
        # Rating Type
        rating_type = record.get('CREDIT TYPE', 'Unknown')
        stats['rating_types'][rating_type] = stats['rating_types'].get(rating_type, 0) + 1
    
    return stats


def display_statistics(stats):
    """Display statistics"""
    print("\n" + "=" * 80)
    print("📊 STATISTICS")
    print("=" * 80)
    
    print(f"\n🏢 Unique Companies: {len(stats['unique_companies'])}")
    print(f"📊 Total Records: {stats['total_records']}")
    
    print("\n⭐ Top Credit Ratings:")
    sorted_ratings = sorted(stats['ratings'].items(), key=lambda x: x[1], reverse=True)
    for rating, count in sorted_ratings[:15]:
        print(f"  {rating}: {count}")
    
    print("\n🎯 Current Actions:")
    sorted_actions = sorted(stats['actions'].items(), key=lambda x: x[1], reverse=True)
    for action, count in sorted_actions[:10]:
        print(f"  {action}: {count}")
    
    print("\n📋 Rating Types:")
    sorted_types = sorted(stats['rating_types'].items(), key=lambda x: x[1], reverse=True)
    for rtype, count in sorted_types:
        print(f"  {rtype}: {count}")


def interactive_menu(data_dict):
    """Interactive menu for viewing data"""
    while True:
        print("\n" + "=" * 80)
        print("📋 MENU")
        print("=" * 80)
        print("1. View All Records (first 20)")
        print("2. View All Records (complete)")
        print("3. Search by Company/Symbol")
        print("4. Search by Credit Rating")
        print("5. Search by Action (e.g., Reaffirm, Upgrade)")
        print("6. View Statistics")
        print("7. Export to CSV")
        print("8. Show Metadata")
        print("9. Switch File")
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
            keyword = input("\nEnter company name or symbol: ").strip()
            filtered = filter_by_company(data, keyword)
            print(f"\nFound {len(filtered)} records for '{keyword}'")
            if filtered:
                display_data_table(filtered)
            else:
                print("❌ No records found")
        
        elif choice == '4':
            rating = input("\nEnter credit rating (e.g., AA, AAA, A+): ").strip()
            filtered = filter_by_rating(data, rating)
            print(f"\nFound {len(filtered)} records with rating '{rating}'")
            if filtered:
                display_data_table(filtered)
            else:
                print("❌ No records found")
        
        elif choice == '5':
            action = input("\nEnter action (e.g., Reaffirm, Upgrade): ").strip()
            filtered = filter_by_action(data, action)
            print(f"\nFound {len(filtered)} records with action '{action}'")
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
                for col in df.columns:
                    if df[col].apply(lambda x: isinstance(x, dict)).any():
                        df[col] = df[col].apply(lambda x: x.get('text', x) if isinstance(x, dict) else x)
                
                market = metadata.get('market_type', 'unknown').lower()
                filename = f"credit_rating_{market}_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
                df.to_csv(filename, index=False, encoding='utf-8-sig')
                print(f"\n✅ Data exported to: {filename}")
            except ImportError:
                print("\n❌ Error: pandas not installed. Install it with: pip install pandas")
            except Exception as e:
                print(f"\n❌ Error exporting: {e}")
        
        elif choice == '8':
            display_metadata(metadata)
        
        elif choice == '9':
            return 'switch'
        
        elif choice == '0':
            print("\n👋 Goodbye!")
            return 'exit'
        
        else:
            print("\n❌ Invalid choice. Please try again.")


def select_file():
    """Select which market type file to view"""
    files = list_available_files()
    
    if not files:
        print("\n❌ No data files found!")
        print("Expected files in: credit_rating_data/latest_*.json")
        print("\nPlease run the monitor first:")
        print("  python credit_rating_monitor.py")
        return None
    
    print("\n" + "=" * 80)
    print("📂 AVAILABLE DATA FILES")
    print("=" * 80)
    
    for i, file in enumerate(files, 1):
        basename = os.path.basename(file)
        market = basename.replace('latest_', '').replace('.json', '')
        
        try:
            size = os.path.getsize(file) / 1024
            mtime = datetime.fromtimestamp(os.path.getmtime(file))
            time_str = mtime.strftime("%Y-%m-%d %H:%M:%S")
            print(f"{i}. {market.upper()} - {size:.1f} KB (Modified: {time_str})")
        except:
            print(f"{i}. {market.upper()}")
    
    print("0. Exit")
    
    choice = input(f"\nSelect file to view (1-{len(files)}): ").strip()
    
    if choice == '0':
        return None
    
    try:
        idx = int(choice) - 1
        if 0 <= idx < len(files):
            return files[idx]
        else:
            print("❌ Invalid choice")
            return None
    except ValueError:
        print("❌ Invalid input")
        return None


def main():
    """Main function"""
    try:
        import tabulate as tab
    except ImportError:
        print("⚠️  Warning: 'tabulate' package not installed")
        print("For better formatting, install it with: pip install tabulate\n")
    
    while True:
        filepath = select_file()
        
        if not filepath:
            print("\n👋 Goodbye!")
            break
        
        print(f"\nLoading data from: {filepath}")
        data_dict = load_data(filepath)
        
        if not data_dict:
            continue
        
        display_metadata(data_dict['metadata'])
        
        if not data_dict['data']:
            print("❌ No data found in the file")
            continue
        
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
            result = interactive_menu(data_dict)
            if result == 'exit':
                break
        except KeyboardInterrupt:
            print("\n\n👋 Interrupted by user. Goodbye!")
            break


if __name__ == "__main__":
    main()

