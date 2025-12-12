"""
View Latest Event Calendar Data
================================

Simple script to view the latest scraped event calendar data
in a formatted, human-readable way.

Usage:
    python view_latest_data.py
"""

import json
import os
from datetime import datetime
from tabulate import tabulate


def load_latest_data():
    """Load the latest JSON data"""
    filepath = 'event_calendar_data/latest.json'
    
    if not os.path.exists(filepath):
        print("❌ Error: No data found!")
        print(f"Expected file: {filepath}")
        print("\nPlease run the monitor first:")
        print("  python event_calendar_monitor.py")
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
        # Handle objects with text and link
        if 'text' in value:
            return value['text']
        return str(value)
    return str(value) if value else ''


def display_metadata(metadata):
    """Display metadata information"""
    print("\n" + "=" * 80)
    print("📊 NSE EVENT CALENDAR - LATEST DATA")
    print("=" * 80)
    
    # Parse timestamp
    try:
        timestamp = datetime.fromisoformat(metadata['scrape_timestamp'])
        time_str = timestamp.strftime("%B %d, %Y at %I:%M:%S %p")
    except:
        time_str = metadata['scrape_timestamp']
    
    print(f"\n⏰ Scraped: {time_str}")
    print(f"📈 Total Events: {metadata['total_records']}")
    print(f"📄 Total Pages: {metadata['total_pages']}")
    print(f"🔗 Source: {metadata['source_url']}")
    print()


def display_data_table(data, max_rows=None):
    """Display data in a formatted table"""
    if not data:
        print("No data to display")
        return
    
    headers = data[0].keys()
    
    # Prepare table data
    table_data = []
    for i, row in enumerate(data):
        if max_rows and i >= max_rows:
            break
        
        row_data = [format_cell(row.get(h, '')) for h in headers]
        table_data.append(row_data)
    
    # Display table
    print(tabulate(table_data, headers=headers, tablefmt='grid', maxcolwidths=50))
    
    # Show count info
    if max_rows and len(data) > max_rows:
        print(f"\n... showing {max_rows} of {len(data)} total events")


def filter_by_purpose(data, keyword):
    """Filter events by purpose keyword"""
    filtered = []
    for event in data:
        purpose = event.get('PURPOSE', '')
        if isinstance(purpose, str) and keyword.lower() in purpose.lower():
            filtered.append(event)
    return filtered


def filter_by_company(data, keyword):
    """Filter events by company name"""
    filtered = []
    for event in data:
        company = event.get('COMPANY', '')
        if isinstance(company, str) and keyword.lower() in company.lower():
            filtered.append(event)
    return filtered


def filter_by_date(data, date_str):
    """Filter events by date"""
    filtered = []
    for event in data:
        date = event.get('DATE', '')
        if isinstance(date, str) and date_str in date:
            filtered.append(event)
    return filtered


def get_statistics(data):
    """Get statistics from the data"""
    stats = {
        'total_events': len(data),
        'unique_companies': set(),
        'purposes': {},
        'dates': {}
    }
    
    for event in data:
        # Company
        company = event.get('COMPANY', '')
        if company:
            stats['unique_companies'].add(company)
        
        # Purpose
        purpose = event.get('PURPOSE', 'Unknown')
        stats['purposes'][purpose] = stats['purposes'].get(purpose, 0) + 1
        
        # Date
        date = event.get('DATE', 'Unknown')
        stats['dates'][date] = stats['dates'].get(date, 0) + 1
    
    return stats


def display_statistics(stats):
    """Display statistics"""
    print("\n" + "=" * 80)
    print("📊 STATISTICS")
    print("=" * 80)
    
    print(f"\n🏢 Unique Companies: {len(stats['unique_companies'])}")
    print(f"📅 Total Events: {stats['total_events']}")
    
    # Top purposes
    print("\n🎯 Top Event Purposes:")
    sorted_purposes = sorted(stats['purposes'].items(), key=lambda x: x[1], reverse=True)
    for purpose, count in sorted_purposes[:10]:
        print(f"  {purpose}: {count}")
    
    # Top dates
    print("\n📅 Events by Date (Top 10):")
    sorted_dates = sorted(stats['dates'].items(), key=lambda x: x[1], reverse=True)
    for date, count in sorted_dates[:10]:
        print(f"  {date}: {count} events")


def interactive_menu(data_dict):
    """Interactive menu for viewing data"""
    while True:
        print("\n" + "=" * 80)
        print("📋 MENU")
        print("=" * 80)
        print("1. View All Events (first 20)")
        print("2. View All Events (complete)")
        print("3. Search by Purpose (e.g., dividend, result, AGM)")
        print("4. Search by Company Name")
        print("5. Search by Date")
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
            print("📊 FIRST 20 EVENTS")
            print("=" * 80)
            display_data_table(data, max_rows=20)
        
        elif choice == '2':
            print("\n" + "=" * 80)
            print("📊 ALL EVENTS")
            print("=" * 80)
            display_data_table(data)
        
        elif choice == '3':
            keyword = input("\nEnter purpose keyword (e.g., dividend, result): ").strip()
            filtered = filter_by_purpose(data, keyword)
            print(f"\n Found {len(filtered)} events matching '{keyword}'")
            if filtered:
                display_data_table(filtered)
            else:
                print("❌ No events found")
        
        elif choice == '4':
            keyword = input("\nEnter company name or keyword: ").strip()
            filtered = filter_by_company(data, keyword)
            print(f"\nFound {len(filtered)} events for companies matching '{keyword}'")
            if filtered:
                display_data_table(filtered)
            else:
                print("❌ No events found")
        
        elif choice == '5':
            date_str = input("\nEnter date (e.g., 15-Dec-2025): ").strip()
            filtered = filter_by_date(data, date_str)
            print(f"\nFound {len(filtered)} events on '{date_str}'")
            if filtered:
                display_data_table(filtered)
            else:
                print("❌ No events found")
        
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
                
                filename = f"event_calendar_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
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
    # Check if tabulate is installed
    try:
        import tabulate as tab
    except ImportError:
        print("⚠️  Warning: 'tabulate' package not installed")
        print("For better formatting, install it with: pip install tabulate")
        print("\nContinuing with basic display...\n")
    
    # Load data
    print("Loading latest event calendar data...")
    data_dict = load_latest_data()
    
    if not data_dict:
        return
    
    # Display metadata
    display_metadata(data_dict['metadata'])
    
    # Check if data exists
    if not data_dict['data']:
        print("❌ No event data found in the file")
        return
    
    # Show first few events
    print("=" * 80)
    print("📊 PREVIEW (First 10 Events)")
    print("=" * 80)
    try:
        display_data_table(data_dict['data'], max_rows=10)
    except Exception as e:
        print(f"Error displaying table: {e}")
        # Fallback to simple display
        for i, event in enumerate(data_dict['data'][:10]):
            print(f"\nEvent {i+1}:")
            for key, value in event.items():
                print(f"  {key}: {format_cell(value)}")
    
    # Interactive menu
    try:
        interactive_menu(data_dict)
    except KeyboardInterrupt:
        print("\n\n👋 Interrupted by user. Goodbye!")


if __name__ == "__main__":
    main()

