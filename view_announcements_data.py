"""
View Latest Announcements Data
===============================

Simple script to view the latest scraped announcements data
in a formatted, human-readable way.

Usage:
    python view_announcements_data.py
"""

import json
import os
import glob
from datetime import datetime
from tabulate import tabulate


def list_available_files():
    """List all available JSON files"""
    files = glob.glob('announcements_data/latest_*.json')
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
        # Handle objects with text and link
        if 'text' in value:
            text = value['text']
            if value.get('type') == 'pdf':
                return f"{text} [PDF]"
            elif value.get('type') == 'xbrl':
                return f"{text} [XBRL]"
            else:
                return text
        return str(value)
    return str(value) if value else ''


def display_metadata(metadata):
    """Display metadata information"""
    print("\n" + "=" * 80)
    print("📢 NSE ANNOUNCEMENTS - LATEST DATA")
    print("=" * 80)
    
    # Parse timestamp
    try:
        timestamp = datetime.fromisoformat(metadata['scrape_timestamp'])
        time_str = timestamp.strftime("%B %d, %Y at %I:%M:%S %p")
    except:
        time_str = metadata['scrape_timestamp']
    
    print(f"\n⏰ Scraped: {time_str}")
    print(f"📊 Market Type: {metadata.get('market_type', 'N/A')}")
    print(f"📈 Total Announcements: {metadata['total_records']}")
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
    print(tabulate(table_data, headers=headers, tablefmt='grid', maxcolwidths=40))
    
    # Show count info
    if max_rows and len(data) > max_rows:
        print(f"\n... showing {max_rows} of {len(data)} total announcements")


def filter_by_subject(data, keyword):
    """Filter announcements by subject keyword"""
    filtered = []
    for announcement in data:
        subject = announcement.get('SUBJECT', '')
        if isinstance(subject, str) and keyword.lower() in subject.lower():
            filtered.append(announcement)
    return filtered


def filter_by_company(data, keyword):
    """Filter announcements by company name or symbol"""
    filtered = []
    for announcement in data:
        company = announcement.get('COMPANY NAME', '')
        symbol = announcement.get('SYMBOL', '')
        
        # Handle symbol if it's an object
        if isinstance(symbol, dict):
            symbol = symbol.get('text', '')
        
        if (isinstance(company, str) and keyword.lower() in company.lower()) or \
           (isinstance(symbol, str) and keyword.lower() in symbol.lower()):
            filtered.append(announcement)
    return filtered


def filter_by_date(data, date_str):
    """Filter announcements by date"""
    filtered = []
    for announcement in data:
        date = announcement.get('BROADCAST DATE/TIME', '')
        if isinstance(date, str) and date_str in date:
            filtered.append(announcement)
    return filtered


def get_statistics(data):
    """Get statistics from the data"""
    stats = {
        'total_announcements': len(data),
        'unique_companies': set(),
        'subjects': {},
        'has_pdf': 0,
        'has_xbrl': 0
    }
    
    for announcement in data:
        # Company
        company = announcement.get('COMPANY NAME', '')
        if company:
            stats['unique_companies'].add(company)
        
        # Subject
        subject = announcement.get('SUBJECT', 'Unknown')
        stats['subjects'][subject] = stats['subjects'].get(subject, 0) + 1
        
        # Attachments
        attachment = announcement.get('ATTACHMENT', '')
        if isinstance(attachment, dict) and attachment.get('type') == 'pdf':
            stats['has_pdf'] += 1
        
        xbrl = announcement.get('XBRL', '')
        if isinstance(xbrl, dict) and xbrl.get('type') == 'xbrl':
            stats['has_xbrl'] += 1
    
    return stats


def display_statistics(stats):
    """Display statistics"""
    print("\n" + "=" * 80)
    print("📊 STATISTICS")
    print("=" * 80)
    
    print(f"\n🏢 Unique Companies: {len(stats['unique_companies'])}")
    print(f"📢 Total Announcements: {stats['total_announcements']}")
    print(f"📎 With PDF: {stats['has_pdf']}")
    print(f"📊 With XBRL: {stats['has_xbrl']}")
    
    # Top subjects
    print("\n📋 Top Announcement Subjects:")
    sorted_subjects = sorted(stats['subjects'].items(), key=lambda x: x[1], reverse=True)
    for subject, count in sorted_subjects[:15]:
        print(f"  {subject}: {count}")


def interactive_menu(data_dict):
    """Interactive menu for viewing data"""
    while True:
        print("\n" + "=" * 80)
        print("📋 MENU")
        print("=" * 80)
        print("1. View All Announcements (first 20)")
        print("2. View All Announcements (complete)")
        print("3. Search by Subject (e.g., dividend, result, merger)")
        print("4. Search by Company/Symbol")
        print("5. Search by Date")
        print("6. View Statistics")
        print("7. Filter by Financial Results")
        print("8. Filter by Dividend")
        print("9. Export to CSV")
        print("10. Show Metadata")
        print("11. Switch File")
        print("0. Exit")
        print()
        
        choice = input("Enter your choice: ").strip()
        
        data = data_dict['data']
        metadata = data_dict['metadata']
        
        if choice == '1':
            print("\n" + "=" * 80)
            print("📢 FIRST 20 ANNOUNCEMENTS")
            print("=" * 80)
            display_data_table(data, max_rows=20)
        
        elif choice == '2':
            print("\n" + "=" * 80)
            print("📢 ALL ANNOUNCEMENTS")
            print("=" * 80)
            display_data_table(data)
        
        elif choice == '3':
            keyword = input("\nEnter subject keyword (e.g., result, dividend): ").strip()
            filtered = filter_by_subject(data, keyword)
            print(f"\nFound {len(filtered)} announcements matching '{keyword}'")
            if filtered:
                display_data_table(filtered)
            else:
                print("❌ No announcements found")
        
        elif choice == '4':
            keyword = input("\nEnter company name or symbol: ").strip()
            filtered = filter_by_company(data, keyword)
            print(f"\nFound {len(filtered)} announcements for '{keyword}'")
            if filtered:
                display_data_table(filtered)
            else:
                print("❌ No announcements found")
        
        elif choice == '5':
            date_str = input("\nEnter date (e.g., 12-Dec-2025): ").strip()
            filtered = filter_by_date(data, date_str)
            print(f"\nFound {len(filtered)} announcements on '{date_str}'")
            if filtered:
                display_data_table(filtered)
            else:
                print("❌ No announcements found")
        
        elif choice == '6':
            stats = get_statistics(data)
            display_statistics(stats)
        
        elif choice == '7':
            filtered = filter_by_subject(data, 'result')
            print(f"\nFound {len(filtered)} financial results announcements")
            if filtered:
                display_data_table(filtered, max_rows=20)
            else:
                print("❌ No announcements found")
        
        elif choice == '8':
            filtered = filter_by_subject(data, 'dividend')
            print(f"\nFound {len(filtered)} dividend announcements")
            if filtered:
                display_data_table(filtered, max_rows=20)
            else:
                print("❌ No announcements found")
        
        elif choice == '9':
            try:
                import pandas as pd
                df = pd.DataFrame(data)
                # Flatten dict columns
                for col in df.columns:
                    if df[col].apply(lambda x: isinstance(x, dict)).any():
                        df[col] = df[col].apply(lambda x: x.get('text', x) if isinstance(x, dict) else x)
                
                market = metadata.get('market_type', 'unknown').lower()
                filename = f"announcements_{market}_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
                df.to_csv(filename, index=False, encoding='utf-8-sig')
                print(f"\n✅ Data exported to: {filename}")
            except ImportError:
                print("\n❌ Error: pandas not installed. Install it with: pip install pandas")
            except Exception as e:
                print(f"\n❌ Error exporting: {e}")
        
        elif choice == '10':
            display_metadata(metadata)
        
        elif choice == '11':
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
        print("Expected files in: announcements_data/latest_*.json")
        print("\nPlease run the monitor first:")
        print("  python announcements_monitor.py")
        return None
    
    print("\n" + "=" * 80)
    print("📂 AVAILABLE DATA FILES")
    print("=" * 80)
    
    for i, file in enumerate(files, 1):
        # Extract market type from filename
        basename = os.path.basename(file)
        market = basename.replace('latest_', '').replace('.json', '')
        
        # Get file size and modification time
        try:
            size = os.path.getsize(file) / 1024  # KB
            mtime = datetime.fromtimestamp(os.path.getmtime(file))
            time_str = mtime.strftime("%Y-%m-%d %H:%M:%S")
            print(f"{i}. {market.upper()} - {size:.1f} KB (Modified: {time_str})")
        except:
            print(f"{i}. {market.upper()}")
    
    print("0. Exit")
    
    choice = input("\nSelect file to view (1-{}): ".format(len(files))).strip()
    
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
    # Check if tabulate is installed
    try:
        import tabulate as tab
    except ImportError:
        print("⚠️  Warning: 'tabulate' package not installed")
        print("For better formatting, install it with: pip install tabulate")
        print("\nContinuing with basic display...\n")
    
    while True:
        # Select file to view
        filepath = select_file()
        
        if not filepath:
            print("\n👋 Goodbye!")
            break
        
        # Load data
        print(f"\nLoading data from: {filepath}")
        data_dict = load_data(filepath)
        
        if not data_dict:
            continue
        
        # Display metadata
        display_metadata(data_dict['metadata'])
        
        # Check if data exists
        if not data_dict['data']:
            print("❌ No announcement data found in the file")
            continue
        
        # Show first few announcements
        print("=" * 80)
        print("📢 PREVIEW (First 10 Announcements)")
        print("=" * 80)
        try:
            display_data_table(data_dict['data'], max_rows=10)
        except Exception as e:
            print(f"Error displaying table: {e}")
            # Fallback to simple display
            for i, announcement in enumerate(data_dict['data'][:10]):
                print(f"\nAnnouncement {i+1}:")
                for key, value in announcement.items():
                    print(f"  {key}: {format_cell(value)}")
        
        # Interactive menu
        try:
            result = interactive_menu(data_dict)
            if result == 'exit':
                break
            # If 'switch', loop continues and asks for file again
        except KeyboardInterrupt:
            print("\n\n👋 Interrupted by user. Goodbye!")
            break


if __name__ == "__main__":
    main()

